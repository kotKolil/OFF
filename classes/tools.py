from random import *
import datetime
import hashlib
import os
import time

from .settings import *


sample= '1h9K8L9h5d5v5Z4q7'



def allowed_file(filename):
    #function of checking file
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_token(s1:str="vasya228", s2:str="12345"):
    token = hashlib.sha256(s1.encode()+s2.encode()).hexdigest()
    return token

def get_current_time():
    t = time.localtime()
    return time.strftime("%D.%H:%M:%S", t)


def generate_id():
    lst = "qwertyuiopasdfghjklzxcvbnm1234567890"
    Result = ""
    for i in range(len(lst)):
        Result += lst[choice(range(1, len(lst)))]

    return Result

def error_decorator(self,func):
    print("error_decorator")
    def wrapper(*args, **kwargs):
        try:
            resultat = func(*args, **kwargs)
            return resultat
        except Exception as e:
            self.class_logger.log_message(str(e))
            return str(e)
    return wrapper


def InitDB(DBWorker:object):
        # structure of table user: email,  UserId, IsAdmin, IsBanned, LogoPath, citate, time, token

        DBWorker("""
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
                IsActivated INTEGER
            );
        """)

                

        # structure of table topic time|theme|author|about|TopicId


        DBWorker("""
            CREATE TABLE IF NOT EXISTS topic(
                time TEXT,
                theme TEXT, 
                author TEXT REFERENCES user(UserId),
                about TEXT,
                TopicId TEXT NOT NULL UNIQUE


            );
                  
                  
                  
                  """)

                
        # creating table messages, which represents the message class
        # structure of table messages: TopicId, MessageId, author, text, time

        DBWorker("""
            CREATE TABLE IF NOT EXISTS messages (
                TopicId TEXT REFERENCES topic(TopicId),
                MessageId TEXT UNIQUE PRIMARY KEY,
                author TEXT REFERENCES user(UserId),
                text TEXT,
                time TEXT
            );
        """)