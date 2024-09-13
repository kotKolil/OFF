from .tools import *
from .TableMetaClass import *

class user(TableMetaClass):

    def get(self, user, password):

        super().get(self)

        UserHash = generate_id(user, password)

        return self.DBworker(f"SELECT * FROM user WHERE token = '{UserHash}'")
    
    def all_(self):
        super().all_(self)

        return self.DBworker(f"SELECT * FROM user")

    def delete(self,user, password):
        super().delete(self)

        UserHash = generate_id(user, password)

        return self.DBworker(f"DELETE * FROM user WHERE UserHash = '{UserHash}'")

    def create(self, password, user, is_admin, is_banned, logo_path, citate):
        # structure of table user: password, user_id, is_admin, is_banned, logo_path, citate, time_of_join, token

        super().create(self)

        try:
            self.DBworker(f"INSERT INTO user VALUES '{password}', '{user}', 0, 0 , '{logo_path}', '{citate}', '{get_current_time()}',  '{generate_token(user, paassword)}'")
            return 1
        except:
            return 0