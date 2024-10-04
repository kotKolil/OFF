from .tools import *
from .wrap import *
from .storage import *
from random import *
import os

class user():

    def __init__(self, DBworker):
        self.DBworker = DBworker

    @UserFormatWrapper
    def get(self, user="", password="", format = "obj", token = ""):
        if user != "" and password != "":
            UserHash = generate_token(user, password)
            return [self.DBworker(query = "SELECT * FROM user WHERE token = ? OR ActiveNum = ? ", param =  (UserHash)), self.DBworker ]
        
        elif token != "":
            return [self.DBworker( query = "SELECT * FROM user WHERE token = ?", param =  (UserHash)), self.DBworker ]
    
    @UserFormatWrapper
    def all(self, format = "obj"):
        return [UserStorage([i], self.DBworker) for i in self.DBworker("SELECT * FROM user")]

    def delete(self,user, password, token):
        if user != "" and password != "":
            self.DBworker(query = "DELETE * FROM user WHERE token = ?", param = (generate_token(user, password)) )
            return 1
        elif token != "":
            self.DBworker(query = "DELETE * FROM user WHERE token = ?", param = (generate_token(user, password)) )
            return 1
    
    @UserFormatWrapper
    def create(self, password, email, user, is_admin, is_banned, logo_path, citate):
        self.DBworker(query = """INSERT INTO user VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? ) """, param = (user, is_admin, logo_path, citate, get_current_time(), generate_token(user, password), randint(0,10**6), 0 ))
        return self.get(user= user, password = password)