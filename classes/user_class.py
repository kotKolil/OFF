from .tools import *

class user:
    #structure of table user password|user|is_admin|is_bannes|logo_path|citate|time_of_join|token
    def __init__(self, email , password, user_id, is_admin, is_banned,logo_path,citate,time_of_join, db):
        self.time_of_join = get_current_time()
        self.password = password
        self.user_id = user_id
        self.is_admin = is_admin
        self.is_banned = is_banned
        self.logo_path = logo_path
        self.citate = citate
        self.token = generate_token(self.user_id, self.password)
        db.excute_query(f"INSERT INTO user VALUES ('{email}', '{password}', '{user_id}', 0, 0, '{logo_path}', '{citate}', '{str(get_current_time())}', '{generate_token()}') ")
        

    @staticmethod
    def get(user, password, db:object):
        return db.excute_query(f"SELECT * FROM user WHERE user_id = '{user}' and password = '{password}' ")

    @staticmethod
    def GetUserOnToken(Token, db:object):
        return db.excute_query(f"SELECT * FROM user WHERE token = '{Token}' ")
