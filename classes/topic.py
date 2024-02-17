from .tools import *
from .inter import *
import zope.interface


#place, where user write message

class topic():

    
    
    def __init__(self, time_of_creation, theme,author,about, sb_id, db:object):
        self.time_of_creation = time_of_creation
        self.theme = theme
        self.author = author
        self.about = about
        self.sb_id = sb_id

        db.excute_query(f"""INSERT INTO user VALUES ( '{time_of_creation}',
                        '{theme}', '{author}', '{about}', '{sb_id}'
                        )""")


    # structure of table topic time_of_creation|theme|author|about|sb_id

    zope.interface.implementer(IModelMethod)

    @staticmethod
    def all(db:object):
        return db.execute_query("SELECT * FROM messages")

    def get(self, mess_id):
        return self.db.execute_query(f"SELECT FROM messages WHERE id_thd = '{mess_id} ORDER BY time_sending' ")
    
    def delete(self, mess_id):
        return self.db.execute_query(F"DELETE FROM messages WHERE id_thd = '{mess_id}'")

    def update(self,id_thd,text):

        # structure of table messages: id_thread, message_id, author, text, time_of_publication
        return self.db.excute_query(f"""UPDATE messages SET text='{text}' , 
                                    time_of_publication='{get_current_time()}'  WHERE id_thread='{id_thd}'""")
