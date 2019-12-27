import logging
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any, List, NamedTuple

OptionDisplay = NamedTuple("OptionDisplay", [("label", str), ("value", Any)])


class OptionsParserBase(ArgumentParser):
    """
    Enhanced version of the standard ArgumentParser.

    Adds initialization of the logging system, a standard 'verbose' flag, and a nicely formatted header that derived
    classes can populate.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.options = Namespace()
        self.options_display: List[OptionDisplay] = []
        self.add_argument("-v", "--verbose", action="store_true", help="write debug messages to the log")
        logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)-7s %(message)s")

    def parse(self, args=None, cmdline=True) -> Namespace:
        """
        Parse commandline options, optionally add a "Command Line" option display, and allow derived classes to validate
        and process the options.
        """
        if args is None:
            args = sys.argv[1:]
        self.parse_args(args, self.options)
        if cmdline and args:
            self.add_option_display("Command Line", ' '.join(args))
        self._post_parse()
        return self.options

    def add_option_display(self, label: str, value: Any):
        """
        Add an option display for logging.

        An option display consists of a *label* and a *value*.
        """
        self.options_display.append(OptionDisplay(label + ":", value))

    def log_header(self):
        """Print header and option displays to the log"""
        logging.info(f"{self.prog} - {self.description}")
        if self.options_display:
            label_width = max(len(option_display.label) for option_display in self.options_display)
            for option_display in self.options_display:
                logging.info(f"  {option_display.label:{label_width}} {option_display.value}")

    def _post_parse(self):
        """Hook for validating and processing the options object."""
        if self.options.verbose:
            logging.getLogger().setLevel(logging.DEBUG)


if __name__ == '__main__':
    class OptionsParser(OptionsParserBase):
        def __init__(self, **kwargs):
            kwargs.update(description="Demonstrate a derived options parser")
            super().__init__(**kwargs)
            self.add_argument("-f", "--first", type=int, metavar="NUM", default=42,
                              help="first argument (limit: 50, default: %(default)s)")

        def _post_parse(self):
            super()._post_parse()
            if self.options.first > 50:
                self.error(f"Argument 'first' is {self.options.first}, which is greater than 50")
            self.add_option_display("First", self.options.first)


    def main():
        parser = OptionsParser(prog=Path(__file__).stem + ".main")
        parser.parse()
        parser.log_header()
        logging.debug("Log level set to DEBUG")


    sys.exit(main())
