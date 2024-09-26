from .tools import *
from .TableMetaClass import *
from .storage import *

class messages(TableMetaClass):

    def __init__(self, DBworker):
        super().__init__(DBworker)

    def get(self, MessageId):
        super().get()

        return MessagesStorage(self.DBworker(f"SELECT * FROM messages WHERE MessageId = '{MessageId}'"))
    
    def JsonGet(self, MessageId):

        MessageId = self.DBworker(f"SELECT * FROM WHERE = '{MessageId}' ")

        return {"TopicId":MessageId[0], "MessageId":MessageId[1], "author":MessageId[2], "text":MessageId[3], "time":MessageId[4]}

    def all_(self, TopicId):
        super().get

        return [MessagesStorage(i) for i in self.DBworker(f"SELECT * FROM messages TopicId = '{TopicId}'")]
    
    def AllJson(self, TopicId):
        messages = self.DBworker(f"SELECT * FROM messages WHERE TopicId = '{TopicId}'")
        result = []
        for MessageId in messages:
            author_data = self.DBworker(f"SELECT * FROM user WHERE UserId = '{MessageId[2]}'")
            if author_data:
                author_data = author_data[0]
                result.append({
                    "TopicId": MessageId[0],
                    "MessageId": MessageId[1],
                    "author": {
                        "email": author_data[0],
                        "UserId": author_data[1],
                        "IsAdmin": author_data[2],
                        "IsBanned": author_data[3],
                        "LogoPath": author_data[4],
                        "citate": author_data[5],
                        "time": author_data[6]
                    },
                    "text": MessageId[3],
                    "time": MessageId[4]
                })
        return result

    def AllJson_(self):

        return [{"TopicId":MessageId[0], "MessageId":MessageId[1], "author":MessageId[2], "text":MessageId[3], "time":MessageId[4]} for MessageId in self.DBworker(f"SELECT * FROM messages") ]

    def delete(self, MessageId):

        super().get
        self.DBworker(f"DELETE * from messages WHERE MessageId = '{MessageId}'")

    def create(self, TopicId, author, text, time_of_publication):
        # TopicId, MessageId, author, text, time_of_publication
        super().create
        
        try:
            Token = generate_id()
            self.DBworker(f"INSERT INTO messages VALUES ('{TopicId}', '{Token}', '{author}', '{text}', '{get_current_time()}')")    
            return {"TopicId": TopicId, "MessageId": Token, "author":author, "text":text, "time":get_current_time()}
        except:
            return 0
