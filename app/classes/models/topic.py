from app.classes.other.tools import *
from app.classes.Serialisation.wrap import *

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
        self.DBWorker(query = "DELETE from topic WHERE TopicId = ?", param = (TopicId,))
        return 1

    def create(self, theme, author, about, protected, format = "obj" , TopicId = ""):
        # time_of_creation|theme|author|about|sb_id


        if TopicId == "":

            Id = generate_id()

            try:
                self.DBWorker(query = "INSERT INTO topic VALUES (?, ?, ?, ?, ?, ?)", param = [get_current_time(), theme, author, about, Id, protected])
                return self.get(TopicId=Id, format = format)
            except sqlite3.IntegrityError or psycopg2.errors.UniqueViolation:
                return 0

        else:

            try:
                self.DBWorker(query = "INSERT INTO topic VALUES (?, ?, ?, ?, ?, ?)", param = [get_current_time(), theme, author, about, TopicId, protected])
                return self.get(TopicId=TopicId, format = format)
            except sqlite3.IntegrityError or psycopg2.errors.UniqueViolation:
                return 0