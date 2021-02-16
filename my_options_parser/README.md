# Package OptionsParserBase

Enhanced version of the standard ArgumentParser.

Adds initialization of the logging system, standard 'verbose' and 'quiet' flags, and a nicely formatted header that derived classes can populate.

## Usage Instructions

Define a class derived from `OptionsBaseDriver`, and override the following methods:

`__init__(**kwargs)`

- Call the base method with the provided arguments. A common practice is to override `kwargs["description"]`.
- Define command-line arguments using the usual `argparse` syntax.

_post_parse()

- Call the vase method
- Test the validity of self.options. call self.error if anything is wrong.
- call `self.add_display_option()` for everything you want to show in the log header.

In your main program:
- Instantiate your new class
- Call `parser.parse()`
- call `parser.log_headers()`
- Use `parser.options`

## Example:

`main.py`

    class OptionsParser(OptionsParserBase):
        def __init__(self, **kwargs):
            kwargs.update(description="Demonstrate a derived options parser")
            super().__init__(**kwargs)
            self.add_argument("-f", "--first", type=int, metavar="NUM", default=1,
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
        
Run `python main.py -h`

    usage: options_parser_base.main [-h] [-v | -q] [-f NUM]
    
    Demonstrate a derived options parser
    
    optional arguments:
      -h, --help           show this help message and exit
      -v, --verbose        write debug messages to the log (default: False)
      -q, --quiet          write only warning and error messages to the log
                           (default: False)
      -f NUM, --first NUM  first argument (limit: 50) (default: 1)

Run `python main.py`

    2020-04-25 17:42:07,556 INFO    options_parser_base.main - Demonstrate a derived options parser
    2020-04-25 17:42:07,557 INFO      First: 1

Run `python mmain.py -f 42 -v`

    2020-04-25 17:44:15,390 INFO    options_parser_base.main - Demonstrate a derived options parser
    2020-04-25 17:44:15,390 INFO      Command: -f 42 -v
    2020-04-25 17:44:15,391 INFO      First:   42
    2020-04-25 17:44:15,391 DEBUG   Log level set to DEBUG

Run `python mmain.py -f 52 -v`

    usage: options_parser_base.main [-h] [-v | -q] [-f NUM]
    options_parser_base.main: error: Argument 'first' is 52, which is greater than 50
