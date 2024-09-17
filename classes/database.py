import sqlite3
import psycopg2 as psql

from .tools import *

from .user import *
from .message import *
from .topic import *

class sqlite3():

    def __init__(self, path):
        self.path = path

    def work(self, query):
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.commit()

        return data
    
    def DBInit(self):
        DBIinit(self.work)

class postgres():

    def __init__(self, host, port, name, user, password):
        self.host = host
        self.port = port
        self.name = name
        self.user = user
        self.password = password

    def work(self, query):
        conn = psql.connect(dbname=self.name, user=self.user, password=self.password, host=self.host, port=self.port)
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        return data
    
    def DBInit(self):
        DBIinit(self.work)

class DB:

    def __init__(self, DBType="sqlite3", path="", host="", port="", name="", user="", paassword=""):

        match DBType:
            case "sqlite3":
                self.db = sqlite3(path)
            case "postgres":
                self.db = postgres(host, port, name, user, password)
            case _:
                raise TypeError("Unkwon type of DB")
            

    def DBIinit(self):
        self.db.DBInit()

    def User(self):
        return User(self.db.work)

    def Topic(self):
        return Topic(self.db.work)

    def Message(self):
        return Message(self.db.work)

    

    


