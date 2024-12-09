from .tools import *
from .storage import *
from .wrap import *

import sqlite3
import psycopg2

class topic:

    def __init__(self, DBworker):
        self.DBWorker = DBworker

    @TopicData_FormatWrapper
    def get(self, topic_id, data_format="obj"):
        return [ self.DBWorker(query="SELECT * FROM topic WHERE TopicId = ?", param=[topic_id] ), self.DBWorker ]

    @TopicData_FormatWrapper
    def all(self, data_format = "obj"):
        return [self.DBWorker(query = "SELECT * FROM topic", param = ()), self.DBWorker ]

    def delete(self, topic_id):
        self.DBWorker(query = "DELETE from topic WHERE TopicId = ?", param = (topic_id,))
        return 1

    def create(self, theme, author, about, protected, data_format = "obj" , topic_id = ""):
        # time_of_creation|theme|author|about|sb_id


        if topic_id == "":

            Id = generate_id()

            try:
                self.DBWorker(query = "INSERT INTO topic VALUES (?, ?, ?, ?, ?, ?)", param = [get_current_time(), theme, author, about, Id, protected])
                return self.get(topic_id=Id, data_format = data_format)
            except sqlite3.IntegrityError or psycopg2.errors.UniqueViolation:
                return 0

        else:

            try:
                self.DBWorker(query = "INSERT INTO topic VALUES (?, ?, ?, ?, ?, ?)", param = [get_current_time(), theme, author, about, topic_id, protected])
                return self.get(topic_id=topic_id, data_format = data_format)
            except sqlite3.IntegrityError or psycopg2.errors.UniqueViolation:
                return 0