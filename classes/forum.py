from .database import *
from .loggers import *
from .tools import *
from .abcd_classes import *
from flask import *


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
        return self.db.execute_query("SELECT * FROM threads WHERE forum_name = '{self.name}'")
    
    def create(self, id_thd):
        
        self.db.excute_query(f"""INSERT INTO threads VALUES ('{self.id_forum}', 
                              '{self.th_id}', '{self.name}','{self.toc}',
                              '{self.author}', {self.decrpt})""")
        
    def get(self,id_thd):
        return self.db.execute_query(f'SELECT * FROM threads WHERE id={id_thd}')
    
    def delete(self, id_thd):
        return self.db.excute_query(f"DELETE FROM threads WHERE id={id_thd}")
    
    def change(self,id_thd,name, decrpt):
        return self.db.excute_query("UPDATE FROM threads WHERE id={id_thd} ({name}, {decrpt})")

