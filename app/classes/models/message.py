import sqlite3
import psycopg2
import copy

from app.classes.other.tools import *
from app.classes.Serialisation.TableDataSerialisation import *


class messages:

    def __init__(self, DBWorker):
        self.DBWorker = copy.copy(DBWorker)

    @MessageFormatWrapper
    def get(self, TopicId="", MessageId="", format="obj"):

        if TopicId != "" and MessageId == "":

            return [self.DBWorker("SELECT * FROM messages WHERE TopicId = ? ", param=[TopicId]), self.DBWorker]

        elif TopicId == "" and MessageId != "":

            return [self.DBWorker("SELECT * FROM messages WHERE MessageId = ? ", param=[MessageId]), self.DBWorker]

        else:
            return 0

    @MessageFormatWrapper
    def all(self, format="json"):
        return [self.DBWorker(query="SELECT * FROM messages ORDER BY DATETIME(time)", param=[]), self.DBWorker]

    def delete(self, MessageId="", TopicId=""):

        if MessageId != "":
            self.DBWorker(query="DELETE from messages WHERE MessageId = ? ", param=[MessageId])
            return 1
        elif TopicId != "":
            self.DBWorker(query="DELETE from messages WHERE TopicId = ? ", param=[TopicId])
            return 1

    def create(self, TopicId, author, text, format="obj"):
        # TopicId, MessageId, author, text, time_of_publication

        try:
            token = generate_id()
            self.DBWorker(query="INSERT INTO messages VALUES (?, ?, ?, ?, ?)",
                          param=[TopicId, token, author, text, get_current_time()])
            return self.get(MessageId=token, format=format)
        except sqlite3.IntegrityError or psycopg2.errors.UniqueViolation:
            return 0
