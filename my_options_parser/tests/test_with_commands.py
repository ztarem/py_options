import logging
import os
from argparse import Namespace

from my_options_parser import OptionsParserBase


def first_command(options: Namespace):
    logging.debug(f"first_command(first={options.f})")


def second_command(options: Namespace):
    logging.debug(f"second_command(second={options.s})")


def strip_log(text: str) -> str:
    return '\n'.join([s[24:] for s in text.split('\n')])


class OptionsParser(OptionsParserBase):
    def __init__(self, **kwargs):
        kwargs.update(description="Demonstrate a derived options parser with commands", commands=True)
        super().__init__(**kwargs)
        kwargs.pop("commands")
        self.first_parser = self.subparsers.add_parser("first", formatter_class=self.formatter_class,
                                                       parents=[self.log_parser])
        self.first_parser.add_argument("-f", type=int, default=1, help="first argument")
        self.first_parser.set_defaults(func=first_command)
        self.second_parser = self.subparsers.add_parser("second", formatter_class=self.formatter_class,
                                                        parents=[self.log_parser])
        self.second_parser.add_argument("-s", action="store_true", help="second argument")
        self.second_parser.set_defaults(func=second_command)

    def _post_parse(self):
        if self.options.command == "first":
            self.add_header("First", self.options.f)
        if self.options.command == "second":
            self.add_header("Second", self.options.s)


def test_help():
    os.environ["COLUMNS"] = "132"
    parser = OptionsParser(prog="test_with_commands.py")
    expected = """
usage: test_with_commands.py [-h] {first,second} ...

Demonstrate a derived options parser with commands

positional arguments:
  {first,second}

optional arguments:
  -h, --help      show this help message and exit
"""
    actual = parser.format_help()
    # print(f"actual=\n{actual}")
    assert actual.strip() == expected.strip()


def test_first_help():
    os.environ["COLUMNS"] = "132"
    parser = OptionsParser(prog="test_with_commands.py")
    expected = """
usage: test_with_commands.py first [-h] [-v] [-q] [--log [FILE]] [-f F]

optional arguments:
  -h, --help     show this help message and exit
  -f F           first argument (default: 1)

Logging options:
  -v, --verbose  write debug messages to the log (default: False)
  -q, --quiet    write only warning and error messages to the log (default: False)
  --log [FILE]   log file name (default: None)
"""
    actual = parser.first_parser.format_help()
    # print(f"actual=\n{actual}")
    assert actual.strip() == expected.strip()


def test_first(capsys):
    parser = OptionsParser(prog="test_with_commands.py")
    options = parser.parse_args(["first"])
    capsys.readouterr()
    parser.log_headers()
    options.func(options)

    expected = """
INFO    test_with_commands.py - Demonstrate a derived options parser with commands
INFO      Command: first
INFO      First:   1
"""
    actual = strip_log(capsys.readouterr().out)
    # print(f"actual=\n{actual}")
    assert actual.strip() == expected.strip()


def test_second_help():
    os.environ["COLUMNS"] = "132"
    parser = OptionsParser(prog="test_with_commands.py")
    expected = """
usage: test_with_commands.py second [-h] [-v] [-q] [--log [FILE]] [-s]

optional arguments:
  -h, --help     show this help message and exit
  -s             second argument (default: False)

Logging options:
  -v, --verbose  write debug messages to the log (default: False)
  -q, --quiet    write only warning and error messages to the log (default: False)
  --log [FILE]   log file name (default: None)
"""
    actual = parser.second_parser.format_help()
    # print(f"actual=\n{actual}")
    assert actual.strip() == expected.strip()


def test_second(capsys):
    parser = OptionsParser(prog="test_with_commands.py")
    options = parser.parse_args(["second"])
    capsys.readouterr()
    parser.log_headers()
    options.func(options)

    expected = """
INFO    test_with_commands.py - Demonstrate a derived options parser with commands
INFO      Command: second
INFO      Second:  False
"""
    actual = strip_log(capsys.readouterr().out)
    # print(f"actual=\n{actual}")
    assert actual.strip() == expected.strip()
