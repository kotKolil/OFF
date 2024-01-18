from random import *
import datetime
from .database import *

def get_current_time():
    tim = str(datetime.datetime.now())
    return tim


def generate_id():
    lst = "qwertyuiopasdfghjklzxcvbnm1234567890"
    for i in range(str(lst)):
        lst += lst[random.choice(range(1, len(lst)))]

    return lst


def error_decorator(self,func):
    print("error_decorator")
    def wrapper(*args, **kwargs):
        try:
            resultat = func(*args, **kwargs)
            return resultat
        except Exception as e:
            self.__class_logger.log_message(str(e))
            return str(e)
    return wrapper


def initialise_database(db:object = sql_lite3_db("db.db")):



    if db.__class__ == sql_lite3_db:

        # sqlite3 didn't handle date type, so date_of_creation and other similar variables must be like YYYY-MM-DD HH:MM:SS.SSS
        #creating table, which represents the forum class
        #structure of table forum : name;date_of_creasting;id

        db.excute_query("""CREATE TABLE IF NOT EXISTS forums (
                
                name text, 
                date_of_creation text,
                forum_id text UNIQUE PRIMARY KEY,
                                                            )
                        """)
        
        #creating table threads, which represents the thread class
        #structure of table: id_forum|id_thread|name|time_of_creation|author|decrpt (description)

        db.excute_query("""CREATE TABLE IF NOT EXISTS thread (
        
        id_forum text REFERENCES forums.forum_id, 
        id_thread text UNIQUE PRIMARY KEY,
        time_of_creation text,
        author text REFRENCES user.user,
        decrpt text,
                                                            )
                        """)


        #creating table messages, which represents the messages class
        #structure of table messages : |id_thd|mess_id|author|text|time_of_publication

        db.excute_query(""" CREATE TABLE IF NOT EXISTS messages (
                        
                        id_thd text REFERENCES thread.id_thread,
                        mess_id text UNIQUE PRIMARY KEY,
                        author text REFRENCES user.user,
                        text_of_publication text,
                        time_of_publication text,


                                                                )
                        

                        """)

        #structure of table user password|user|is_admin|is_banned|logo_path|citate|time_of_join
        db.execute_query(""" CREATE user (
                         password text,
                         user UNIQUE FOREIGN KEY ,
                         is_admin boolean,
                         is_banned boolean,
                         logo_path TEXT,
                         citate text,
                         time_of_join text,


                                        )
                         
                         
                         """)

        
    elif db.__class__ == postgres_db:

        #creating table, which represents the forum class
        #structure of table forum : name;date_of_creasting;id

        db.excute_query("""CREATE TABLE IF NOT EXISTS forums (
                
                name text, 
                date_of_creation date,
                forum_id text UNIQUE PRIMARY KEY,
                                                            )
                        """)
        
        #creating table threads, which represents the thread class
        #structure of table: id_forum|id_thread|name|time_of_creation|author|decrpt (description)

        db.excute_query("""CREATE TABLE IF NOT EXISTS thread (
        
        id_forum text REFERENCES forums.forum_id, 
        id_thread text UNIQUE PRIMARY KEY,
        time_of_creation date,
        author text REFRENCES user.user,
        decrpt text,
                                                            )
                        """)


        #creating table messages, which represents the messages class
        #structure of table messages : |id_thd|mess_id|author|text|time_of_publication

        db.excute_query(""" CREATE TABLE IF NOT EXISTS messages (
                        
                        id_thd text REFERENCES thread.id_thread,
                        mess_id text UNIQUE PRIMARY KEY,
                        author text REFRENCES user.user,
                        text_of_publication text,
                        time_of_publication date,


                                                                )
                        
                        """)
        
        #structure of table user password|user|is_admin|is_banned|logo_path|citate|time_of_join
        db.execute_query(""" CREATE user (
                         password text,
                         user UNIQUE FOREIGN KEY ,
                         is_admin boolean,
                         is_banned boolean,
                         logo_path TEXT,
                         citate text,
                         time_of_join date,


                                        )
                         
                         
                         """)



    else:
        raise TypeError('object must be in databases classes, not in other')
    


