from .tools import *
from .storage import *
from .TableMetaClass import *

class Topic(TableMetaClass):

    def __init__(self, DBworker):
        super().__init__(self, DBworker)

    def get(self, TopicId):
        super().get(self)

        return TopicStorage(self.DBworker(f"SELECT * FROM topic WHERE TopicId = {TopicId}"))

    def all_(self):
        super().get(self)

        return [TopicStorage(i) for i in self.DBworker("SELECT * FROM topic")]

    def delete(self, TopicId):
        super().get(self)
        self.DBworker(f"DELETE * from topic WHERE TopicId = {TopicId}")

    def create(self, time_of_creation, theme, author, about):
        # time_of_creation|theme|author|about|sb_id
        super().create(self)
        
        try:
            self.DBworker(f"INSERT INTO topic VALUES '{get_current_time()}', '{theme}', '{author}', '{about}', '{generate_id()}'")
            return 1
        except:
            return 0