from .tools import *
from .inter import *
import zope.interface
from .tools import *

#place, where user write topic


#code 1 - sucefull
#code 0 - fault

class topic():

    def __init__(self, time_of_creation, theme,author,about, sb_id, db:object):
        
        self.time_of_creation = time_of_creation
        self.theme = theme
        self.author = author
        self.about = about
        self.sb_id = sb_id


        db.excute_query(f"""INSERT INTO topic VALUES ( '{time_of_creation}',
                            '{theme}', '{author}', '{about}', '{sb_id}'
                            )""")





    @staticmethod
    def all(db:object):
        return db.excute_query("SELECT * FROM topic")

    @staticmethod
    def get(db:object, sub_id):
        return db.excute_query(f"SELECT * FROM topic WHERE sb_id = '{sub_id}' ")
    
    def delete(self, mess_id):
        return self.db.excute_query(F"DELETE FROM topic WHERE id_topic = '{mess_id}'")

    def update(self,id_thd,text):

        # structure of table topic: id_thread, message_id, author, text, time_of_publication
        return self.db.excute_query(f"""UPDATE topic SET text='{text}' , 
                                    time_of_publication='{get_current_time()}'  WHERE id_topic='{id_thd}'""")
