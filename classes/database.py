from abc import *
import sqlite3

class abc_db(ABCMeta):

    @abstractclassmethod
    def __init__(self, port=5432, password="admin", user="admin"):
        self.__port = port
        self.__password = password
        self.__user = user
    
    @abstractclassmethod
    def excute_expression(self, query):
        #logic of sending SQL script to Database
        pass


class sql_lite3_db(abc_db):

    def __init__(self, filename="db.db"):
        self.__filename = filename

    def excute_query(self, query):
        connection = sqlite3.connect(self.__filename)
        cursor = connection.cursor()
        cursor.commit()
        cursor.close()
        

