from .tools import *
from .storage import *
from .TableMetaClass import *

class Topic(TableMetaClass):

    def __init__(self, DBworker):
        super().__init__(self, DBworker)

    def get(self, TopicId):
        super().get(self)

        return TopicStorage(self.DBworker(f"SELECT * FROM topic WHERE TopicId = {TopicId}"))
    
    def JsonGet(self, TopicId):
        TopicData = self.DBworker(f"SELECT * FROM topic WHERE TopicId = {TopicId}")

        return {"time":TopicData[0], "theme":TopicData[1], "author":TopicData[2], "about":TopicData[3], "TopicId":TopicData[4]}

    def all_(self):
        super().get(self)

        return [TopicStorage(i) for i in self.DBworker("SELECT * FROM topic")]
    
    def AllJson(self):
        return [{"time":TopicData[0], "theme":TopicData[1], "author":TopicData[2], "about":TopicData[3], "TopicId":TopicData[4]} for TopicData in self.DBworker("SELECT * FROM topic")]

    def delete(self, TopicId):
        super().get(self)
        self.DBworker(f"DELETE * from topic WHERE TopicId = {TopicId}")

    def create(self, theme, author, about):
        # time_of_creation|theme|author|about|sb_id
        super().create(self)
        
        try:
            self.DBworker(f"INSERT INTO topic VALUES '{get_current_time()}', '{theme}', '{author}', '{about}', '{generate_id()}'")
            return 1
        except:
            return 0