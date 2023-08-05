import logging


class SystemLog:
    """ Logger class to log if --verbose option provided to command line """

    def __init__(self, format_=None):
        self.logger = logging.getLogger(__name__)
        self.stream_handler = logging.StreamHandler()
        if format_ is None:
            format_ = '%(asctime)s : %(levelname)s : %(message)s'
        self.set_format(format_)

    def set_format(self, format_):
        """ Set format for logger """

        formatter = logging.Formatter(format_)
        self.stream_handler.setFormatter(formatter)
        self.logger.addHandler(self.stream_handler)

    def set_level(self, level):
        """ Set log level for logger """

        self.logger.setLevel(level=level)
