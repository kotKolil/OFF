from .database import *
from .loggers import *
from .tools import *
from .abcd_classes import *
from flask import *
from .inter import *


class forum:

    def __init__(self, db=sql_lite3_db("db.db"), name="forum"):

        self.db  = db
        self.id_forum = generate_id()
        self.name = name

        #creating table in database, which related with forum with SQL script
        #structure of table forum : name;date_of_creasting;id
        db.excute_query(f"INSERT INTO forum VALUES ('{self.name}', '{get_current_time()}', '{generate_id()}') ")


        
    #structure of table: id_forum|id_thread|name|time_of_creation|author|decrpt

    
    def all(self):
        return self.db.excute_query("SELECT * FROM thread WHERE id_forum = '{self.id_forum}'")
    
    def create(self, name, decrypt, author:object):
        
        # structure of table thread: id_forum, id_thread, name, time_of_creation, author, decrypt (description)
        self.db.excute_query(f"""INSERT INTO thread VALUES ('{self.id_forum}', 
                              '{generate_id()}', '{name}',
                              '{get_current_time()}', {author.user_id},  {self.decrpt})""")
        
    def get(self,id_thd):
        return self.db.excute_query(f"SELECT * FROM thread WHERE id_forum='{id_thd}'")
    
    def delete(self, id_thd):
        return self.db.excute_query(f"DELETE FROM thread WHERE id_forum={id_thd}")
    
    def update(self,id_thd,name, decrpt):
        return self.db.excute_query("UPDATE FROM threadS WHERE id_forum={id_thd} ({name}, {decrpt})")

