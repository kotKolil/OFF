from .tools import *

class user:
    #structure of table user password|user|is_admin|is_bannes|logo_path|citate|time_of_join
    def __init__(self, password, user, is_admin, is_banned,logo_path,citate,time_of_join, db):
        self.time_of_join = get_current_time()
        self.password = password
        self.user = user
        self.is_admin = is_admin
        self.is_banned = is_banned
        self.logo_path = logo_path
        self.citate = citate
        

    

        
    