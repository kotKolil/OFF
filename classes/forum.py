from .database import *
from .loggers import *
from .tools import *
from .abstract import *
from flask import *


class forum:

    def __init__(self, db=sql_lite3_db("db.db"), name="forum"):

        self.__db  = db()
        self.__id_forum = generate_id()
        self.__name = name

        #creating table in database, which related with forum with SQL script
        #structure of table forum : name;date_of_creasting;id
        db.execute_query(f"INSERT INTO forums VALUES ({self._name}, {get_current_time()}, {generate_id}) ")


    #threads methods
        
    def all(self):
        return self.__db.execute_query("SELECT * FROM threads WHERE forum_name = '{self.__name}'")
    
    #methods for single thread
    #getting thread from table threads 
    def create(self, id_thd):
        #structure of table: id_forum|id_thread|name|time_of_creation|author|decrpt
        self.__db.excute_query(f"""INSERT INTO threads VALUES ('{self.__id_forum}', 
                              '{self.__th_id}', '{self.__name}','{self.__toc}',
                              '{self.__author}', {self.decrpt})""")
    def get(self,id_thd):
        return self.__db.execute_query(f'SELECT * FROM threads WHERE id={id_thd}')
    
    def delete(self, id_thd):
        return self.__db.excute_query(f"DELETE FROM threads WHERE id={id_thd}")
    
    def change(self,id_thd,name, decrpt):
        return self.__db.excute_query("UPDATE FROM threads WHERE id={id_thd} ({name}, {decrpt})")

    #methods with messages
    #structure of table messages : |id_thd|mess_id|author|text|time_of_publication

    def get_thread_messages(self, id_thd):
        return self.__db.execute_query(f"SELECT FROM messages WHERE id_thd = '{id_thd} ORDER BY time_sending' ")
    
    def delete_thread_message(self, mess_id):
        return self.__db.execute_query(F"DELETE FROM messages WHERE id_thd = '{mess_id}'")
