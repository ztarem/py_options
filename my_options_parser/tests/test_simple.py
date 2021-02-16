import logging
import os

from my_options_parser import OptionsParserBase


def strip_log(text: str) -> str:
    return '\n'.join([s[24:] for s in text.split('\n')])


def test_help():
    os.environ["COLUMNS"] = "132"
    parser = OptionsParserBase(prog="test_simple.py", description="Test OptionsParserBase")
    expected = """
usage: test_simple.py [-h] [-v] [-q] [--log [FILE]]

Test OptionsParserBase

optional arguments:
  -h, --help     show this help message and exit

Logging options:
  -v, --verbose  write debug messages to the log (default: False)
  -q, --quiet    write only warning and error messages to the log (default: False)
  --log [FILE]   log file name (default: None)
"""
    actual = parser.format_help()
    # print(f"actual=\n{actual}")
    assert actual.strip() == expected.strip()


def test_default(capsys):
    parser = OptionsParserBase(prog="test_simple.py", description="Test OptionsParserBase")
    parser.parse_args([])
    capsys.readouterr()
    parser.log_headers()
    logging.debug("This is a debug message")
    logging.warning("This is a warning message")
    expected = """
INFO    test_simple.py - Test OptionsParserBase
WARNING This is a warning message
"""
    actual = strip_log(capsys.readouterr().out)
    # print(f"actual=\n{actual}")
    assert actual.strip() == expected.strip()


def test_verbose(capsys):
    parser = OptionsParserBase(prog="test_simple.py", description="Test OptionsParserBase")
    parser.parse_args(["-v"])
    capsys.readouterr()
    parser.log_headers()
    logging.debug("This is a debug message")
    logging.warning("This is a warning message")
    expected = """
INFO    test_simple.py - Test OptionsParserBase
INFO      Command: -v
DEBUG   This is a debug message
WARNING This is a warning message
"""
    actual = strip_log(capsys.readouterr().out)
    # print(f"actual=\n{actual}")
    assert actual.strip() == expected.strip()


def test_quiet(capsys):
    parser = OptionsParserBase(prog="test_simple.py", description="Test OptionsParserBase")
    parser.parse_args(["-q"])
    capsys.readouterr()
    parser.log_headers()
    logging.debug("This is a debug message")
    logging.warning("This is a warning message")
    expected = """
WARNING This is a warning message
"""
    actual = strip_log(capsys.readouterr().out)
    # print(f"actual=\n{actual}")
    assert actual.strip() == expected.strip()


def test_verbose_logfile(capsys, tmp_path):
    log_path = tmp_path / "test_simple.log"
    parser = OptionsParserBase(prog="test_simple.py", description="Test OptionsParserBase")
    parser.parse_args(["-v", "--log", str(log_path)])
    capsys.readouterr()
    parser.log_headers()
    logging.debug("This is a debug message")
    logging.warning("This is a warning message")
    assert log_path.open().read() == capsys.readouterr().out
