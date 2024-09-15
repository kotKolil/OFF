from .tools import *
from .storage import *
from .TableMetaClass import *

class user(TableMetaClass):

    def __init__(self, DBworker):
        super().__init__(self, DBworker)

    def get(self, user, password):

        super().get(self)

        UserHash = generate_id(user, password)

        return UserStorage(self.DBworker(f"SELECT * FROM user WHERE token = '{UserHash}'"))
    
    def all_(self):
        super().all_(self)

        return [UserStorage(i) for i in self.DBworker(f"SELECT * FROM user")]

    def delete(self,user, password):
        super().delete(self)

        UserHash = generate_id(user, password)
        
        self.DBworker(f"DELETE * FROM user WHERE token = '{UserHash}'")

    def create(self, password, email, user, is_admin, is_banned, logo_path, citate):
        # structure of table user: password, user_id, is_admin, is_banned, logo_path, citate, time_of_join, token

        super().create(self)

        try:
            self.DBworker(f"INSERT INTO user VALUES '{email}', '{user}', {is_admin}, {is_banned} , '{logo_path}', '{citate}', '{get_current_time()}',  '{generate_token(user, password)}'")
            return 1
        except:
            return 0