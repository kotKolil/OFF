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
        return [ self.DBWorker(query="SELECT * FROM topic WHERE TopicId = ?", param=[TopicId] ), self.DBWorker ]

    @TopicFormatWrapper
    def all(self, format = "obj"):
        return [self.DBWorker(query = "SELECT * FROM topic", param = ()), self.DBWorker ]

    def delete(self, TopicId):
        self.DBworker(query = "DELETE * from topic WHERE TopicId = ?", param = (TopicId,))

    @TopicFormatWrapper
    def create(self, theme, author, about, format = "obj"):
        # time_of_creation|theme|author|about|sb_id
        
        Id = generate_id()

        try:
            self.DBWorker(query = "INSERT INTO topic VALUES (?, ?, ?, ?, ?)", param = [get_current_time(), theme, author, about, Id])
            return [ self.DBWorker(query="SELECT * FROM topic WHERE TopicId = ?", param=[Id]), self.DBWorker ]
        except sqlite3.IntegrityError or psycopg2.errors.UniqueViolation:
            return 0