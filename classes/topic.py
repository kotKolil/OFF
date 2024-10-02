from .tools import *
from .storage import *
from .TableMetaClass import *

class topic(TableMetaClass):

    def __init__(self, DBworker):
        super().__init__(DBworker)

    def get(self, TopicId):
        super().get()

        return TopicStorage(self.DBworker(query = "SELECT * FROM topic WHERE TopicId ?", param = (TopicId,)), DBWorker=self.DBworker)
    
    def JsonGet(self, TopicId):
        TopicData = self.DBworker(query = "SELECT * FROM topic WHERE TopicId = ?", param = (TopicId))

        return {"time":TopicData[0], "theme":TopicData[1], "author":TopicData[2], "about":TopicData[3], "TopicId":TopicData[4]}

    def all_(self):
        super().get()

        return [TopicStorage(i) for i in self.DBworker(query = "SELECT * FROM topic", param = ())]
    
    def AllJson(self):
        return [{"time":TopicData[0], "theme":TopicData[1], "author":TopicData[2], "about":TopicData[3], "TopicId":TopicData[4]} for TopicData in self.DBworker(query = "SELECT * FROM topic", param = ())]

    def delete(self, TopicId):
        super().get()
        self.DBworker(query = "DELETE * from topic WHERE TopicId = ?", param = (TopicId,))

    def create(self, theme, author, about):
        # time_of_creation|theme|author|about|sb_id
        super().create()
        
        try:
            self.DBworker(query = "INSERT INTO topic VALUES (?, ?, ?, ?, ?)", param = (get_current_time(), theme, author, about, generate_id()))
            return 1
        except:
            return 0