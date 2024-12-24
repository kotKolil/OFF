import logging
import json
import os

from app.classes.other.tools import *


class ConsoleLog(object):

    @staticmethod
    def log(text, level="info"):

        color_codes = {
            "info": "\033[92m",
            "warning": "\033[93m",
            "error": "\033[91m",
        }

        reset_code = "\033[0m"

        if level in color_codes:
            print("{} {} [{}]: {}{}".format(color_codes[level], get_current_time(), level, text, reset_code))
        else:
            print(text)


class TxtLog(object):

    def __init__(self, filename, path):
        self.filename = filename
        self.path = path

    def log(self, text, level):
        with open(os.path.join(os.getcwd(), self.filename), 'a') as file:
            file.write("{} [{}]: {} \n".format(str(get_current_time()), level, text))
            return 1


class JsonLog(object):

    def __init__(self, filename, path):
        self.filename = filename
        self.path = path

        """initializing logger object"""
        self.logger = logging.getLogger('js_logger')
        self.logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler('{}.json'.format(self.filename))
        file_handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(file_handler)

    def log(self, text, level):
        data = {
            "level": level,
            'message': text,
            "time": str(get_current_time()),
        }

        if level == "info":
            self.logger.error(json.dumps(data))
        elif level == "warning":
            self.logger.warning(json.dumps(data))
        elif level == "error":
            self.logger.error(json.dumps(data))
        else:
            raise TypeError("Unknown type of debug level")


class Logger(object):

    def __init__(self, logger_type="console", name_of_file=""):

        self.NameOfFile = name_of_file

        if logger_type == "":
            self.LoggerClass = ConsoleLog()
        elif logger_type == "console":
            self.LoggerClass = ConsoleLog()
        elif logger_type == "txt":
            self.LoggerClass = TxtLog(filename=self.NameOfFile, path=os.getcwd())
        elif logger_type == "json":
            self.LoggerClass = JsonLog(filename=self.NameOfFile, path=os.getcwd())
        else:
            raise TypeError("Unknown type of logger")

    def info(self, text):
        self.LoggerClass.log(text, level="info")

    def warning(self, text):
        self.LoggerClass.log(text, level="warning")

    def error(self, text):
        self.LoggerClass.log(text, level="error")
