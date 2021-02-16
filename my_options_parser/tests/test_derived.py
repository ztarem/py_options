import logging
import os

from my_options_parser import OptionsParserBase


class OptionsParser(OptionsParserBase):
    def __init__(self, **kwargs):
        kwargs.update(description="Demonstrate a derived options parser")
        super().__init__(**kwargs)
        self.add_argument("-f", "--first", type=int, metavar="NUM", default=1,
                          help="first argument (limit: 50)")

    def _post_parse(self):
        super()._post_parse()
        if self.options.first > 50:
            self.error(f"Argument 'first' is {self.options.first}, which is greater than 50")
        self.add_header("First", self.options.first)


def strip_log(text: str) -> str:
    return '\n'.join([s[24:] for s in text.split('\n')])


def test_help():
    os.environ["COLUMNS"] = "132"
    parser = OptionsParser(prog="test_derived.py")
    expected = """
usage: test_derived.py [-h] [-v] [-q] [--log [FILE]] [-f NUM]

Demonstrate a derived options parser

optional arguments:
  -h, --help           show this help message and exit
  -f NUM, --first NUM  first argument (limit: 50) (default: 1)

Logging options:
  -v, --verbose        write debug messages to the log (default: False)
  -q, --quiet          write only warning and error messages to the log (default: False)
  --log [FILE]         log file name (default: None)
"""
    actual = parser.format_help()
    # print(f"actual=\n{actual}")
    assert actual.strip() == expected.strip()


def test_with_arg(capsys):
    parser = OptionsParser(prog="test_derived.py")
    parser.parse_args(["-v", "-f", "42"])
    capsys.readouterr()
    parser.log_headers()
    expected = """
INFO    test_derived.py - Demonstrate a derived options parser
INFO      Command: -v -f 42
INFO      First:   42
"""
    actual = strip_log(capsys.readouterr().out)
    # print(f"actual=\n{actual}")
    assert actual.strip() == expected.strip()
