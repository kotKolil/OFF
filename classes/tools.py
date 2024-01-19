from random import *
import datetime
from .loggers import *
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
            self.class_logger.log_message(str(e))
            return str(e)
    return wrapper


def initialise_database(db:object):



    if db.__class__ == sql_lite3_db:

        # sqlite3 didn't handle date type, so date_of_creation and other similar variables must be like YYYY-MM-DD HH:MM:SS.SSS
        #creating table, which represents the forum class
        #structure of table forum : name;date_of_creasting;id

        #structure of table user password|user|is_admin|is_banned|logo_path|citate|time_of_join

        db.excute_query(""" 

                CREATE TABLE IF NOT EXISTS user (
                    password TEXT,
                    user TEXT UNIQUE,
                    is_admin BOOLEAN,
                    is_banned BOOLEAN,
                    logo_path TEXT,
                    citate TEXT,
                    time_of_join TEXT
                )
                         
                         
                         """)

        db.excute_query("""

    CREATE TABLE IF NOT EXISTS forum (
        name TEXT,
        date_of_creation TEXT,
        id TEXT
    )

                        """)
        
        #creating table threads, which represents the thread class
        #structure of table: id_forum|id_thread|name|time_of_creation|author|decrpt (description)

        db.excute_query("""
                        
    CREATE TABLE IF NOT EXISTS thread (
        id_forum TEXT REFERENCES forum(id),
        id_thread TEXT UNIQUE PRIMARY KEY,
        time_of_creation TEXT,
        author TEXT REFERENCES user(user),
        decrpt TEXT
    )

                        
""")


        #creating table messages, which represents the messages class
        #structure of table messages : |id_thd|mess_id|author|text|time_of_publication

        db.excute_query(""" 
                        
    CREATE TABLE IF NOT EXISTS messages (
        id_thd TEXT REFERENCES thread(id_thread),
        mess_id TEXT UNIQUE PRIMARY KEY,
        author TEXT REFERENCES user(user),
        text_of_publication TEXT,
        time_of_publication TEXT
    )


                        """)



        
    elif db.__class__ == postgres_db:

        pass



    else:
        raise TypeError('object must be in databases classes, not in other')
    


