from .tools import *
from .wrap import *
from .storage import *
from random import *
import os

class user():

    def __init__(self, DBworker):
        self.DBworker = DBworker

    @UserData_FormatWrapper
    def get(self, user="", password="", data_format = "obj", token = "", num = ""):    

        if user != "" and password == "" and token == "":
            return [ self.DBworker(query = "SELECT * FROM user WHERE UserId = ?", param = [user] ) , self.DBworker]
    
        elif user == "" and password == "" and token == "" and num != "":
            return [ self.DBworker(query = "SELECT * FROM user WHERE ActiveNum = ?", param = [num] ) , self.DBworker]

        elif token != "" and user == "" and password == "":
            UserHash = generate_token(user, password)
            return [self.DBworker(query = "SELECT * FROM user WHERE token = ?", param =  [token] ), self.DBworker ]

        elif user != "" and password != "" and token == "":
            UserHash = generate_token(user, password)
            return [self.DBworker( query = "SELECT * FROM user WHERE token = ?", param =  [UserHash] ), self.DBworker ]
    
    @UserData_FormatWrapper
    def all(self, data_format = "obj"):
        return [ self.DBworker("SELECT * FROM user", []), self.DBworker ]

    def delete(self,user = "", password = "", token = ""):
        if user != "" and password == "":
            self.DBworker(query = "DELETE FROM user WHERE UserId = ?", param = [user] )
            return 1
        elif user != "" and password != "":
            self.DBworker(query = "DELETE FROM user WHERE token = ?", param = [ generate_token(user, password) ] )
            return 1
        elif token != "":
            self.DBworker(query = "DELETE FROM user WHERE token = ?", param = [ generate_token(user, password) ] )
            return 1
    
    def create(self, password = "", email = "", user = "", is_admin = "", is_banned = "", logo_path = "", 
               citate = "", data_format = "obj"):
        self.DBworker(query = """INSERT INTO user VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ) """,
                      param = [ email,  user, is_admin, is_banned,  logo_path, citate,
                                get_current_time(), generate_token(user, password), randint(0,10**6), 0, 0 ])
        return self.get(user= user, password = password, data_format="obj")
