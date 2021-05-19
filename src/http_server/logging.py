from logging import DEBUG, INFO, ERROR
import logging
import sys


class Log:
    def __init__(self, Name, Format="%(asctime)s | %(levelname)s | %(message)s ", level=INFO):
        #Logger configuration
        self.console_formater = logging.Formatter(Format)
        self.console_logger = logging.StreamHandler(sys.stdout)
        self.console_logger.setFormatter(self.console_formater)
        #Complete logging config.
        self.logger = logging.getLogger(name=Name)
        self.logger.setLevel(level)
        self.logger.addHandler(self.console_logger)

    def info(self,messages):
        self.logger.info(messages)

    def warning(self,messages):
        self.logger.warning(messages)
    
    def error(self,messages):
        self.logger.error(messages)

    def critical(self,messages):
        self.logger.critical(messages)
