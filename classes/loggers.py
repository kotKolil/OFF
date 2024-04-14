from abc import *
import logging
import json
import datetime
from .tools import *



class txt_log():
    
    def __init__(self, filename,path):
        self.filename = filename
        self.path = path
        

    def log_message(self, text):
        try:
            with open(self.__p4th + self.__filename, "r") as file:
                file.write(f"[{get_current_time}] text \n")
                file.close()

            return 1
        except Exception as e:
            return [str(e), 0]
        
class json_log():

    def __init__(self,filename, path):
        self.filename = filename
        self.path = path
        

        """initializing logger object"""
        self.logger = logging.getLogger('js_logger')
        self.logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(f'{self.__filename}.json')
        file_handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(file_handler)
        
    def log_message(text, self):
        data = {
        'message':text,
        "time":get_current_time(),
        }       
        self.logger.error(json.dumps(data))
        