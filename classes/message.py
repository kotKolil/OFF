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
    def get(self, TopicId, format = "obj"):

        system("cls")

        print([self.DBWorker("SELECT * FROM messages WHERE TopicId = ? ", param = [TopicId] ), self.DBWorker ])

        return [self.DBWorker("SELECT * FROM messages WHERE TopicId = ? ", param = [TopicId] ), self.DBWorker ]
    
    @MessageFormatWrapper
    def all(self, format = "obj"):
            return self.DBWorker(query = "SELECT * FROM messages", param = [])


    def delete(self, MessageId):

        self.DBWorker(query = "DELETE * from messages WHERE MessageId = ? ", param = [MessageId])

    @MessageFormatWrapper
    def create(self, TopicId, author, text, format = "obj"):
        # TopicId, MessageId, author, text, time_of_publication
        
        try:
            Token = generate_id()
            self.DBWorker(query = "INSERT INTO messages VALUES (?, ?, ?, ?, ?)", param = [ TopicId, generate_id(), author, text, get_current_time() ] ) 
            return self.get(Token)
        except sqlite3.IntegrityError or psycopg2.errors.UniqueViolation:
            return 0
