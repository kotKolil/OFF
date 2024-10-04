from .tools import *
from .storage import *
from .wrap import *

import sqlite3
import psycopg2

class topic:

    def __init__(self, DBworker):
        self.DBWorker = DBworker

    @TopicFormatWrapper
    def get(self, TopicId, format="obj"):
        return [ self.DBworker(query="SELECT * FROM topic WHERE TopicId = ?", param=(TopicId,)), self.DBWorker ]

    @TopicFormatWrapper
    def all(self):
        return [self.DBworker(query = "SELECT * FROM topic", param = ()), self.DBWorker ]

    def delete(self, TopicId):
        self.DBworker(query = "DELETE * from topic WHERE TopicId = ?", param = (TopicId,))

    @TopicFormatWrapper
    def create(self, theme, author, about):
        # time_of_creation|theme|author|about|sb_id
        
        Id = generate_id()

        try:
            self.DBworker(query = "INSERT INTO topic VALUES (?, ?, ?, ?, ?)", param = (get_current_time(), theme, author, about, Id))
            return self.get(Id)
        except sqlite3.IntegrityError or psycopg2.errors.UniqueViolation:
            return 0