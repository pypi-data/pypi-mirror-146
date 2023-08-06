import argparse
import logging
from datetime import datetime


class ArgParser:
    """ Class that specifies arguments that can be passed
            when launching an application """

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader',
                                              prog='rss-reader')

        self.set_cli_arg_options()

    def set_cli_arg_options(self):
        """ Set all positional and optional arguments """

        self.parser.add_argument('source', help='RSS URL', nargs='?')

        self.parser.add_argument('--version', action='version', version='%(prog)s 1.3', help='Print version info')

        self.parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')

        self.parser.add_argument('--verbose', action='store_const', dest='loglevel',
                                 const=logging.INFO, help='Outputs verbose status messages')
        self.parser.add_argument('--limit', metavar='', type=int, nargs='?',
                                 help='Limit news topics if this parameter provided')
        self.parser.add_argument('--date', metavar='', nargs='?', type=self.validate_date,
                                 help='Published date of news in format YYYYMMDD')
        self.parser.add_argument('--clear-cache', help='Clears all news from cache', action='store_true')
        self.cli_args = self.parser.parse_args()

    @staticmethod
    def validate_date(date):
        try:
            return datetime.strptime(date, '%Y%m%d')
        except ValueError:
            msg = "not a valid date: {0!r}. Type -h for more info".format(date)
            raise argparse.ArgumentTypeError(msg)

