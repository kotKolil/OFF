import sqlite3
import psycopg2
from os import *

from .tools import *
from .storage import *
from .wrap import *

class messages():

    def __init__(self, DBWorker):
        self.DBWorker = DBWorker

    @MessageFormatWrapper
    def get(self, TopicId = "", MessageId = ""  ,format = "obj"):

        if TopicId != "" and MessageId == "":

            return [self.DBWorker("SELECT * FROM messages WHERE TopicId = ? ", param = [TopicId] ), self.DBWorker ]
        
        elif TopicId == "" and MessageId != "":

            return [self.DBWorker("SELECT * FROM messages WHERE MessageId = ? ", param = [MessageId] ), self.DBWorker ]
    
        else:
            return 0
    
    @MessageFormatWrapper
    def all(self, format = "obj"):
            return [self.DBWorker(query = "SELECT * FROM messages", param = []), self.DBWorker]


    def delete(self, MessageId):

        self.DBWorker(query = "DELETE * from messages WHERE MessageId = ? ", param = [MessageId])

    def create(self, TopicId, author, text, format = "obj"):
        # TopicId, MessageId, author, text, time_of_publication
        
        try:
            Token = generate_id()
            self.DBWorker(query = "INSERT INTO messages VALUES (?, ?, ?, ?, ?)", param = [ TopicId, Token, author, text, get_current_time() ] ) 
            return self.get( MessageId = Token, format = format)
        except sqlite3.IntegrityError or psycopg2.errors.UniqueViolation:
            return 0
