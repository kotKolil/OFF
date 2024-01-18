from abc import *
import logging
import json
import datetime
from .tools import *
from .abstract import *


class txt_log(abc_log):
    
    def __init__(self, filename,p4th):
        super().__init__(filename,p4th)

    def log_message(self, text):
        try:
            with open(self.__p4th + self.__filename, "r") as file:
                file.write(f"[{get_current_time}] text \n")
                file.close()

            return 1
        except Exception as e:
            return [str(e), 0]
        
class json_log(abc_log):

    def __init__(self,filename, p4th):
        super().__init__(filename, p4th)

        """initializing logger object"""
        self.__logger = logging.getLogger('js_logger')
        self.__logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(f'{self.__filename}.json')
        file_handler.setFormatter(logging.Formatter('%(message)s'))
        self.__logger.addHandler(file_handler)
        
    def log_message(text, self):
        data = {
        'message':text,
        "time":get_current_time(),
        }       
        self.__logger.error(json.dumps(data))
        