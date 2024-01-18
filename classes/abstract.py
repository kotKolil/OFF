from abc import *
from flask import *
from .loggers import *

class abc_db:

    __metaclass__ = ABCMeta

    def __init__(self, port=5432, password="admin", user="admin", name="", host="127.0.0.1"):
        self.__port = port
        self.__password = password
        self.__user = user
        self.__name = name
    
    @abstractclassmethod
    def excute_expression(self, query):
        #logic of sending SQL script to Database
        pass

class abc_log:

    __metaclass__ = ABCMeta

    def __init__(self, filename,p4th):
        self.__p4th = p4th
        self.__filename = filename

    @abstractmethod
    def log_message(text):
        pass



        


        
    def runserver(self):
        try:
            self.__server.run(port = self.__porT, debug = self.__dbG)
            print(f"server started on {self.__hosT}:{self.__porT}. Debug mode is {self.__dbG}")
        except Exception as e:
            print(f"Server not started with error {str(e)}")