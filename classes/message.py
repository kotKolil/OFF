import sqlite3
import psycopg2
from os import *

from .tools import *
from .storage import *
from .wrap import *

class messages():

    def __init__(self, DBWorker):
        self.DBWorker = DBWorker

    @MessageData_FormatWrapper
    def get(self, Topic_Id = "", MessageId = "", data_format = "obj"):

        if Topic_Id != "" and MessageId == "":

            return [self.DBWorker("SELECT * FROM messages WHERE TopicId = ? ", param = [Topic_Id] ), self.DBWorker ]
        
        elif Topic_Id == "" and MessageId != "":

            return [self.DBWorker("SELECT * FROM messages WHERE MessageId = ? ", param = [MessageId] ), self.DBWorker ]
    
        else:
            return 0
    
    @MessageData_FormatWrapper
    def all(self, data_format = "obj"):
            return [self.DBWorker(query = "SELECT * FROM messages ORDER BY DATETIME(time)", param = []), self.DBWorker]


    def delete(self, MessageId = "", Topic_Id = ""):

        if MessageId != "":
            self.DBWorker(query="DELETE from messages WHERE MessageId = ? ", param=[MessageId])
            return 1
        elif Topic_Id != "":
            self.DBWorker(query="DELETE from messages WHERE TopicId = ? ", param=[Topic_Id])
            return 1

    def create(self, Topic_Id, author, text, data_format = "obj"):
        # TopicId, MessageId, author, text, time_of_publication
        
        try:
            Token = generate_id()
            self.DBWorker(query = "INSERT INTO messages VALUES (?, ?, ?, ?, ?)", param = [ Topic_Id, Token, author, text, get_current_time() ] ) 
            return self.get( MessageId = Token, data_format = data_format)
        except sqlite3.IntegrityError or psycopg2.errors.UniqueViolation:
            return 0
