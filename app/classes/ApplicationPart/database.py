import psycopg2 as psql
import sqlite3  # Added import for sqlite3

from app.classes.models.message import *
from app.classes.models.topic import *
from app.classes.models.user import user


def init_db(DBWorker: object):
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
        CREATE TABLE IF NOT EXISTS topic (
            time DATETIME,
            theme TEXT, 
            author TEXT REFERENCES user(UserId),
            about TEXT,
            TopicId TEXT PRIMARY KEY,
            Protected BOOLEAN,
            image TEXT
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
            time TEXT,
            image TEXT
        );
    """, param=())


class SQLite3:

    def __init__(self, path):
        self.path = path

    def work(self, query, param=("",)):
        con = sqlite3.connect(self.path, timeout=7)
        cursor = con.cursor()
        try:
            cursor.execute(query, param)
            data = cursor.fetchall()
            con.commit()
            return data
        except Exception as e:
            print("Error executing query: {}".format(e))
            con.rollback()  # Rollback if there's an error
            return None
        finally:
            cursor.close()  # Close cursor
            con.close()  # Close connection

    def db_init(self):
        init_db(self.work)


class postgres:

    def __init__(self, host, port, name, user, password):
        self.host = host
        self.port = port
        self.name = name
        self.user = user
        self.password = password

    def work(self, query, param=("",)):
        conn = psql.connect(dbname=self.name, user=self.user, password=self.password, host=self.host, port=self.port)
        cursor = conn.cursor()
        try:
            cursor.execute(query, param)
            data = cursor.fetchall()
            conn.commit()
            return data
        except Exception as e:
            print("Error executing query: {}".format(e))
            conn.rollback()  # Rollback if there's an error
            return None
        finally:
            cursor.close()  # Close cursor
            conn.close()  # Close connection

    def db_init(self):
        InitDB(self.work)


class DB:

    def __init__(self, DBType="", host="", port="", name="", user="", password=""):
        if DBType == "":
            self.db = SQLite3("main.db")
        elif DBType == "sqlite3":
            self.db = SQLite3(name)
        elif DBType == "postgres":
            self.db = postgres(host, port, name, user, password)
        else:
            raise TypeError("Unknown type of DB")

    def db_init(self) -> object:
        self.db.db_init()

    def user(self):
        return user(self.db.work)

    def topic(self):
        return topic(self.db.work)

    def message(self):
        return messages(self.db.work)
