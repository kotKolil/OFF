from mailbox import Message
import sqlite3
import psycopg2 as psql
from py_find_injection import find_injection

from .user import user
from .message import *
from .topic import *
from .user import user
from .tools import *

class SQLite3:

    def __init__(self, path):
        self.path = path

    def work(self, query):

        if find_injection(query):
            raise TypeError("SQL Injection detected")

        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        con.commit()

        return data
    
    def DBInit(self):
        InitDB(self.work)

class postgres():

    def __init__(self, host, port, name, user, password):
        self.host = host
        self.port = port
        self.name = name
        self.user = user
        self.password = password

    def work(self, query):

        if find_injection(query):
            raise TypeError("SQL Injection detected")

        conn = psql.connect(dbname=self.name, user=self.user, password=self.password, host=self.host, port=self.port)
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        return data
    
    def DBInit(self):
        InitDB(self.work)


class DB:

    def __init__(self, DBType="sqlite3", path="", host="", port="", name="", user="", password=""):

        match DBType:
            case "sqlite3":
                self.db = SQLite3(path)
            case "postgres":
                self.db = postgres(host, port, name, user, password)
            case _:
                raise TypeError("Unkwon type of DB")
            

    def DBInit(self):
        self.db.DBInit()

    def User(self):
        return user(self.db.work)

    def Topic(self):
        return topic(self.db.work)

    def Message(self):
        return messages(self.db.work)

    

    


