import zope.interface
from .inter import *
from .tools import *

class messages:

    zope.interface.implementer(IModelMethod)


    def __init__(self, TimeOfCreation, Text, UserId, ThreadId, MessageId, db:object):

        self.TimeOfCreation = TimeOfCreation
        self.Text = Text
        self.UserId = UserId
        self.ThreadId = ThreadId
        self.MessageId = MessageId
        self.Text = Text

        db.excute_query(f"""INSERT INTO messages VALUES ({ThreadId},
{MessageId}, {UserId}, {Text}, {TimeOfCreation}) """)
        

    @staticmethod     
    def get(MessageId, db:object):

        return db.execute_query(f"SELECT * FROM messages WHERE id_topic = '{ThreadId}' ")

    @staticmethod
    def all_(ThreadId, db:object):
        return db.excute_query(f"SELECT * FROM messages WHERE id_topic = '{ThreadId}' ")

    @staticmethod
    def delete(ThreadId, db:object):
        try:
            db.execute_query(f"DELETE FROM messages WHERE id_topic = '{mess_id}'")
            return 1
        except Exception as e:
            return 0, str(e)

        
        
