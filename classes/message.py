import zope.interface
from .inter import *

class messages:

    zope.interface.implements(IModelMethod)


    def __init__(self, TimeOfCreation, Text, UserId, ThreadId, MessageId, Text):

        self.TimeOfCreation = TimeOfCreation
        self.Text = Text
        self.UserId = UserId
        self.ThreadId = ThreadId
        self.MessageId = MessageId
        self.Text = Text

    @staticmethod     
    def get(MessageId, db:object):

        return db.execute_query(f"SELECT * FROM messages WHERE id_thread = '{ThreadId}' ")

    @staticmethod
    def all(ThreadId, db:object):
        return db.execute_query(f"SELECT * FROM messages WHERE id_thread = '{ThreadId}' ")

    @staticmethod
    def delete(ThreadId, db:object):
        try:
            db.execute_query(f"DELETE FROM messages WHERE id_thd = '{mess_id}'")
            return 1
        except Exception as e:
            return 0, str(e)
a
        
        