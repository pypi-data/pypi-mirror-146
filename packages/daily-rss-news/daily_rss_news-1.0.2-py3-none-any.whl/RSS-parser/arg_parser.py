import argparse
import logging


class ArgParser:
    """ Class that specifies arguments that can be passed
            when launching an application """

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader',
                                              prog='rss-reader')

        self.set_cli_arg_options()

    def set_cli_arg_options(self):
        """ Set all positional and optional arguments """

        self.parser.add_argument('source', help='RSS URL')

        self.parser.add_argument('--version', action='version', version='%(prog)s 1.0', help='Print version info')

        self.parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')

        self.parser.add_argument('--verbose', action='store_const', dest='loglevel',
                                 const=logging.INFO, help='Outputs verbose status messages')
        self.parser.add_argument('--limit', metavar='', type=int, nargs='?',
                                 help='Limit news topics if this parameter provided')
        self.cli_args = self.parser.parse_args()
