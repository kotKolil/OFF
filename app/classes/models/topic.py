from app.classes.other.tools import *
from app.classes.Serialisation.TableDataSerialisation import *

import sqlite3
import psycopg2
import copy

class topic:

    def __init__(self, DBWorker):
        self.DBWorker = copy.copy(DBWorker)

    @TopicFormatWrapper
    def get(self, TopicId, format="obj"):
        return [self.DBWorker(query="SELECT * FROM topic WHERE TopicId = ?", param=[TopicId]), self.DBWorker]

    @TopicFormatWrapper
    def all(self, format="obj"):
        return [self.DBWorker(query="SELECT * FROM topic", param=()), self.DBWorker]

    def delete(self, TopicId):
        self.DBWorker(query="DELETE from topic WHERE TopicId = ?", param=(TopicId,))
        return 1

    def create(self, theme, author, about, protected, img_path, format="obj", TopicId=""):
        # time_of_creation|theme|author|about|sb_id

        if TopicId == "":

            user_id = generate_id()

            try:
                self.DBWorker(query="INSERT INTO topic VALUES (?, ?, ?, ?, ?, ?, ?)",
                              param=[get_current_time(), theme, author, about, user_id, protected, img_path])
                return self.get(TopicId=user_id, format=format)
            except sqlite3.IntegrityError or psycopg2.errors.UniqueViolation:
                return 0

        else:

            try:
                self.DBWorker(query="INSERT INTO topic VALUES (?, ?, ?, ?, ?, ?, ?)",
                              param=[get_current_time(), theme, author, about, TopicId, protected, img_path])
                return self.get(TopicId=TopicId, format=format)
            except sqlite3.IntegrityError or psycopg2.errors.UniqueViolation:
                return 0
