from .tools import *
from .storage import *
from .TableMetaClass import *

class user(TableMetaClass):

    def __init__(self, DBworker):
        self.DBworker = DBworker

    def get(self, user, password):

        super().get()

        UserHash = generate_token(user, password)

        return UserStorage(self.DBworker(f"SELECT * FROM user WHERE token = '{UserHash}'"))
    

    def JsonGet(self, user, password):

        UserHash = generate_token(user, password)
        UserData = self.DBworker(f"SELECT * FROM user WHERE token = '{UserHash}'")
        return {"email":UserData[0][0], "UserId":UserData[0][1], "IsAdmin":UserData[0][2], "IsBanned":UserData[0][3],"LogoPath":UserData[0][4], "citate":UserData[0][5], "time":UserData[0][6], "token":UserData[0][7]}
    def GetViaTokenJson(self, token):
        UserData = self.DBworker(f"SELECT * FROM user WHERE token = '{token}'")
        if len(UserData) == 0:
            return False
        else:
            return {"email":UserData[0][0], "UserId":UserData[0][1], "IsAdmin":UserData[0][2], "IsBanned":UserData[0][3],"LogoPath":UserData[0][4], "citate":UserData[0][5], "time":UserData[0][6], "token":UserData[0][7]}


    
    


    def GetViaToken(self, token):

        try:
            return UserStorage(self.DBworker(f"SELECT * FROM user WHERE token = '{token}'"))
        except:
            return False
    
    def all_(self):
        super().all_()

        return [UserStorage(i) for i in self.DBworker(f"SELECT * FROM user")]
    
    def AllJson(self):
        super().all_()

        return [ {"email":i[0], "UserId":i[1], "IsAdmin":i[2], "IsBanned":i[3],"LogoPath":i[4], "citate":i[5], "time":i[6], "token":i[7]} for i in self.DBworker(f"SELECT * FROM user")]

    def delete(self,user, password):
        super().delete()

        UserHash = generate_id(user, password)
        

        self.DBworker(f"DELETE * FROM user WHERE token = '{UserHash}'")

    def create(self, password, email, user, is_admin, is_banned, logo_path, citate):
        # structure of table user: password, user_id, is_admin, is_banned, logo_path, citate, time_of_join, token

        super().create()

        # try:
        self.DBworker(f"INSERT INTO user VALUES '{email}', '{user}', {is_admin}, {is_banned} , '{logo_path}', '{citate}', '{get_current_time()}',  '{generate_token(user, password)}'")
        return self.get(user, password)
        # except:
        #     return 0