"""
from .tools import *
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


        db.excute_query(f"INSERT INTO topic VALUES ( '{time_of_creation}',
                            '{theme}', '{author}', '{about}', '{sb_id}'
                            )")




    # structure of table topic time_of_creation|theme|author|about|sb_id



    @staticmethod
    def all_(db:object):
        return db.excute_query("SELECT * FROM topic")

    @staticmethod
    def get(db:object, sub_id):
        return db.excute_query(f"SELECT * FROM topic WHERE sb_id = '{sub_id}' ")
    
    @staticmethod
    def delete(db, mess_id):
        return db.excute_query(f"DELETE FROM topic WHERE sb_id = '{mess_id}'")

    @staticmethod
    def update(db,id_thd,text):

        # structure of table topic: id_thread, message_id, author, text, time_of_publication
        return db.excute_query(f"UPDATE topic SET text='{text}' , 
                                    time_of_publication='{get_current_time()}'  WHERE id_topic='{id_thd}")

"""

from .tools import *
from .TableMetaClass import *

class messages(TableMetaClass):

    def get(self, MessageId):
        super().get(self)

        return DBworker(f"SELECT * FROM messages WHERE MessageId = {MessageId}")

    def all_(self):
        super().get(self)

        return DBworker("SELECT * FROM messages")

    def delete(self, MessageId):
        super().get(self)
        return DBworker(f"DELETE * from messages WHERE MessageId = {MessageId}")

    def create(self, time_of_creation, theme, author, about, sb_id):
        # time_of_creation|theme|author|about|sb_id
        super().create(self)
        
        try:
            self.DBworker(f"INSERT INTO messages VALUES '{get_current_time()}', '{theme}', '{author}', '{about}', '{get_current_time()}'")
            return 1
        except:
            return 0