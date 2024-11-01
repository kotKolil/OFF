from mailbox import Message
import sqlite3
import psycopg2 as psql

from .user import user
from .message import *
from .topic import *
from .user import user
from .tools import *


def InitDB(DBWorker: object):
    # structure of table user: email,  UserId, IsAdmin, IsBanned, LogoPath, citate, time, token

    DBWorker(query="""
        CREATE TABLE IF NOT EXISTS user (
            email TEXT NOT NULL UNIQUE,
            UserId TEXT UNIQUE,
            IsAdmin BOOLEAN,
            IsBanned BOOLEAN,
            LogoPath TEXT,
            citate TEXT,
            time TEXT,
            token TEXT UNIQUE NOT NULL,
            ActiveNum INTEGER UNIQUE NOT NULL,
            IsActivated INTEGER,
            NumOfPosts INTEGER
        );
    """, param=())

    # structure of table topic time|theme|author|about|TopicId

    DBWorker(query="""
        CREATE TABLE IF NOT EXISTS topic(
            time TEXT,
            theme TEXT, 
            author TEXT REFERENCES user(UserId),
            about TEXT,
            TopicId TEXT NOT NULL UNIQUE


        );



              """, param=())

    # creating table messages, which represents the message class
    # structure of table messages: TopicId, MessageId, author, text, time

    DBWorker(query="""
        CREATE TABLE IF NOT EXISTS messages (
            TopicId TEXT REFERENCES topic(TopicId),
            MessageId TEXT UNIQUE PRIMARY KEY,
            author TEXT REFERENCES user(UserId),
            text TEXT,
            time TEXT
        );
    """, param=())


class SQLite3:

    def __init__(self, path):
        self.path = path

    def work(self, query, param=("",)):


        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        cursor.execute(query, param)
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

    def work(self, query, param = ("",)):


        conn = psql.connect(dbname=self.name, user=self.user, password=self.password, host=self.host, port=self.port)
        cursor = conn.cursor()
        cursor.execute(query,param)
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

    

    


