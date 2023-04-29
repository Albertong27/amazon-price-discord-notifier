# Basic Daily Logger module
# By: Albert O
# 2023-04-28
# logger>>logger_module
# This module create a log in specific folder
import logging, datetime, os

class logger_module:
    def __init__(self, dir, format='%(asctime)s - %(levelname)s - %(message)s'):
        self.dir = dir
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        self.logd = logging.getLogger()
        self.formatter = format
        self.set_log_file()
        
    def set_log_file(self, date=None):
        if not date:
            date = datetime.date.today()

        self.today = date
        self.log_file = f"{self.dir}{self.today.strftime('%Y-%m-%d')}.log"
        
        for handler in self.logd.handlers:
            if isinstance(handler, logging.FileHandler):
                self.logd.removeHandler(handler)
                handler.close()

        formatter = logging.Formatter(self.formatter)
        file_handler = logging.FileHandler(self.log_file, mode='a')
        file_handler.setFormatter(formatter)
        self.logd.addHandler(file_handler)
        self.logd.setLevel(logging.DEBUG)
    
    def log(self, level, message):
        self.set_log_file()
        getattr(self.logd, level)(message)

    def debug(self, message):
        self.logd.log('debug', message)

    def info(self, message):
        self.logd.log('info', message)

    def warning(self, message):
        self.logd.log('warning', message)

    def error(self, message):
        self.logd.log('error', message)

    def critical(self, message):
        self.logd.log('critical', message)