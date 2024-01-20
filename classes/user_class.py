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
        
    def check_token(self, token, user):
        if self.db_execute(f"SELECT user FROM  user WHERE token = '{token}'") == user:
            return 1
        else:
            return 0
    

        
    