from .tools import *
from .storage import *
from .TableMetaClass import *

from random import *
import os

class user(TableMetaClass):

    def __init__(self, DBworker):
        self.DBworker = DBworker

    def get(self, user="", password="", num=""):

        super().get()

        UserHash = generate_token(user, password)
        
        return UserStorage(self.DBworker( query = "SELECT * FROM user WHERE token = ? OR ActiveNum = ? ", param =  (UserHash, num)), DBWorker=self.DBworker)
    
    def JsonGet(self, user, password):
        UserHash = generate_token(user, password)
        UserData = self.DBworker(query="SELECT  FROM user WHERE token = ?", param=(UserHash,))
        if UserData:  # Check if the query returned any results
            return {
                "email": UserData[0][0],
                "UserId": UserData[0][1],
                "IsAdmin": UserData[0][2],
                "IsBanned": UserData[0][3],
                "LogoPath": UserData[0][4],
                "citate": UserData[0][5],
                "time": UserData[0][6]
            }
        else:
            return None  # Or return an appropriate error message

    def GetViaTokenJson(self, token):
        os.system("cls")
        print(token)
        UserData = self.DBworker(query = "SELECT * FROM user WHERE token = ?", param = (token,))
        if len(UserData) == 0:
            return False
        else:
            return {"email":UserData[0][0], "UserId":UserData[0][1], "IsAdmin":UserData[0][2], "IsBanned":UserData[0][3],"LogoPath":UserData[0][4], "citate":UserData[0][5], "time":UserData[0][6]}

    def ActivateUser(self, num):
        UserData = UserStorage(self.DBworker(query = "SELECT * FROM user WHERE token = ?", param = (num)))
        self.DBworker(query = "INSERT INTO user(IsActivated) VALUES (?)", param = (1))
    


    def GetViaToken(self, token):

        try:
            return UserStorage(self.DBworker(query = "SELECT * FROM user WHERE token = ?", param = (token)))
        except:
            return False
    
    def all_(self):
        super().all_()

        return [UserStorage(i) for i in self.DBworker(query = "SELECT * FROM user", param = ())]
    
    def AllJson(self):
        super().all_()

        return [ {"email":i[0], "UserId":i[1], "IsAdmin":i[2], "IsBanned":i[3],"LogoPath":i[4], "citate":i[5], "time":i[6]} for i in self.DBworker(query = "SELECT * FROM user", param = ())]

    def delete(self,user, password):
        super().delete()

        UserHash = generate_id(user, password)
        

        self.DBworker(query = "DELETE * FROM user WHERE token = ?", param = (UserHash) )

    def create(self, password, email, user, is_admin, is_banned, logo_path, citate):
        # structure of table user: user_id, is_admin, is_banned, logo_path, citate, time_of_join, token ActiveNum IsActivated

        super().create()


        # try:
        self.DBworker(query = """INSERT INTO user VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? ) """, param = (user, is_admin, logo_path, citate, get_current_time(), generate_token(user, password), randint(0,10**6), 0 ))
        return self.get(user, password)
        # except:
        #     return 0