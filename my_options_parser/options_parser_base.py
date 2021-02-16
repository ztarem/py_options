import logging
import logging.config
import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
from pathlib import Path
from typing import Any, List, NamedTuple, Optional, Text, Tuple


class OptionsParserBase:
    """
    Enhanced version of the standard ArgumentParser.

    Adds initialization of the logging system, a standard 'verbose' flag, and a nicely formatted header that derived
    classes can populate.
    """

    Header = NamedTuple("Header", [("label", str), ("value", Any)])
    Headers = List[Header]

    def __init__(self, **kwargs):
        self.subparsers = None
        self.default_log_name = Path(sys.argv[0]).with_suffix(".log").name
        self.log_parser = ArgumentParser(add_help=False)
        log_group = self.log_parser.add_argument_group("Logging options")
        log_group.add_argument("-v", "--verbose", action="store_true", help="write debug messages to the log")
        log_group.add_argument("-q", "--quiet", action="store_true",
                               help="write only warning and error messages to the log")
        log_group.add_argument("--log", metavar="FILE", nargs="?", const=self.default_log_name, default="None",
                               help="log file name")

        commands = kwargs.pop("commands", False)
        kwargs.setdefault("prog", str(Path(sys.argv[0]).name))
        self.formatter_class = kwargs.setdefault("formatter_class", ArgumentDefaultsHelpFormatter)
        if not commands:
            kwargs.setdefault("parents", []).insert(0, self.log_parser)
        self.parser = ArgumentParser(**kwargs)
        if commands:
            self.subparsers = self.parser.add_subparsers(dest="command")
        self.options = Namespace()
        self.headers: OptionsParserBase.Headers = []

    def parse_args(self, args: Optional[List[Text]] = None) -> Namespace:
        """
        Parse commandline options, optionally add a "Command Line" option display, and allow derived classes to validate
        and process the options.
        """
        if args is None:
            args = sys.argv[1:]
        self.parser.parse_args(args, self.options)
        if args:
            self.add_header("Command", ' '.join(args))
        self._configure_logging()
        self._post_parse()
        return self.options

    def format_help(self):
        return self.parser.format_help()

    def add_argument(self, *args, **kwargs):
        return self.parser.add_argument(*args, **kwargs)

    def error(self, *args, **kwargs):
        return self.parser.error(*args, **kwargs)

    def add_header(self, label: str, value: Any):
        """
        Add an option display for logging.

        An option display consists of a *label* and a *value*.
        """
        self.headers.append(OptionsParserBase.Header(label + ":", value))

    def log_headers(self):
        """Print header and option displays to the log"""
        logging.info(f"{self.parser.prog} - {self.parser.description}")
        if self.headers:
            label_width = max(len(header.label) for header in self.headers)
            for header in self.headers:
                logging.info(f"  {header.label:{label_width}} {header.value}")

    def _configure_logging(self):
        """Hook for validating and processing the options object."""
        file_config = {
            "class": "logging.FileHandler",
            "formatter": "simple",
            "filename": self.default_log_name,
            "mode": "w",
        }
        log_config = {
            "version": 1,
            "formatters": {
                "simple": {
                    "format": "%(asctime)s %(levelname)-7s %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "simple",
                    "stream": sys.stdout,
                },
            },
            "root": {
                "level": "DEBUG" if self.options.verbose else ("WARN" if self.options.quiet else "INFO"),
                "handlers": ["console"],
            },
        }
        if self.options.log != "None":
            file_config.update(filename=self.options.log)
            log_config["handlers"]["file"] = file_config
            log_config["root"]["handlers"].append("file")
        logging.config.dictConfig(log_config)

    def _post_parse(self):
        pass


if __name__ == '__main__':
    class OptionsParser(OptionsParserBase):
        def __init__(self, **kwargs):
            kwargs.update(description="Demonstrate a derived options parser")
            super().__init__(**kwargs)
            self.add_argument("-f", "--first", type=int, metavar="NUM", default=1,
                              help="first argument (limit: 50)")

        def _post_parse(self):
            super()._post_parse()
            if self.options.first > 50:
                self.parser.error(f"Argument 'first' is {self.options.first}, which is greater than 50")
            self.add_header("First", self.options.first)


    def main():
        parser = OptionsParser(prog=Path(__file__).with_suffix(".main").name)
        parser.parse_args()
        parser.log_headers()
        logging.debug("This is a debug message")
        logging.warning("This is a warning message")


    sys.exit(main())
