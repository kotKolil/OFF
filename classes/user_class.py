from .tools import *

class user:
    #structure of table user password|user|is_admin|is_bannes|logo_path|citate|time_of_join|token
    def __init__(self, password, user_id, is_admin, is_banned,logo_path,citate,time_of_join, db):
        self.time_of_join = get_current_time()
        self.password = password
        self.user_id = user_id
        self.is_admin = is_admin
        self.is_banned = is_banned
        self.logo_path = logo_path
        self.citate = citate
        self.token = generate_token(self.user_id, self.password)
        try: 
            db.excute_query(f"INSERT INTO user VALUES ('{password}', '{user_id}', 0, 0, '{logo_path}', '{citate}', '{str(get_current_time())}', '{generate_token()}') ")
        except:
            raise Exception("Same user are exisiting")
        
    def check_token(self, token):
        if self.db_execute(f"SELECT user FROM  user WHERE token = '{token}'") == user:
            return 1
        else:
            return 0
    

        
    