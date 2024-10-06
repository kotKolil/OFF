import sqlite3
import psycopg2

from .tools import *
from .storage import *
from wrap import *

class messages():

    def __init__(self, DBworker):
        self.DBworker = DBworker

    @MessageFormatWrapper
    def get(self, MessageId, format = "obj"):
        return MessagesStorage(query = self.DBworker("SELECT * FROM messages WHERE MessageId = ?", param = (MessageId)))
    
    @MessageFormatWrapper
    def all(self, TopicId = "", format = "obj"):
        if TopicId == "":
            return self.DBworker(query = "SELECT * FROM messages")
        else:
            return self.DBworker( query  = "SELECT * FROM messages TopicId = ?", param = (TopicId) )


    def delete(self, MessageId):

        self.DBworker(query = "DELETE * from messages WHERE MessageId = ?", param = (MessageId))

    @MessageFormatWrapper
    def create(self, TopicId, author, text):
        # TopicId, MessageId, author, text, time_of_publication
        
        try:
            Token = generate_id()
            self.DBworker(query = "INSERT INTO messages VALUES (?, ?, ?, ?, ?)", para = ( TopicId, generate_id(), author, text, get_current_time ) ) 
            return self.get(Token)
        except sqlite3.IntegrityError or psycopg2.errors.UniqueViolation:
            return 0
