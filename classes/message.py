from .tools import *
from .TableMetaClass import *
from .storage import *

class messages(TableMetaClass):

    def __init__(self, DBworker):
        super().__init__(self, DBworker)

    def get(self, MessageId):
        super().get(self)

        return MessagesStorage(self.DBworker(f"SELECT * FROM messages WHERE MessageId = {MessageId}"))

    def all_(self):
        super().get(self)

        return [MessagesStorage(i) for i in self.DBworker("SELECT * FROM messages")]

    def delete(self, MessageId):
        super().get(self)
        self.DBworker(f"DELETE * from messages WHERE MessageId = {MessageId}")

    def create(self, TopicId, author, text, time_of_publication):
        # TopicId, MessageId, author, text, time_of_publication
        super().create(self)
        
        try:
            self.DBworker(f"INSERT INTO messages VALUES '{TopicId}', '{generate_id()}', '{author}', '{text}', '{get_current_time()}'")
            return 1
        except:
            return 0
