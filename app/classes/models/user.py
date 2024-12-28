from app.classes.other.tools import *
from app.classes.Serialisation.TableDataSerialisation import *
from random import *


class user:

    def __init__(self, db_worker):
        self.db_worker = db_worker

    @UserFormatWrapper
    def get(self, username="", password="", format="obj", token="", num=""):

        if username != "" and password == "" and token == "":
            return [self.db_worker(query="SELECT * FROM user WHERE UserId = ?", param=[username,]), self.db_worker]

        elif username == "" and password == "" and token == "" and num != "":
            return [self.db_worker(query="SELECT * FROM user WHERE ActiveNum = ?", param=[num,]), self.db_worker]

        elif token != "" and username == "" and password == "":
            return [self.db_worker(query="SELECT * FROM user WHERE token = ?", param=[token,]), self.db_worker]

        elif username != "" and password != "" and token == "":
            user_hash = generate_token(username, password)
            return [self.db_worker(query="SELECT * FROM user WHERE token = ?", param=[user_hash,]), self.db_worker]

    @UserFormatWrapper
    def all(self, format="obj"):
        return [self.db_worker("SELECT * FROM user", []), self.db_worker]

    def delete(self, username="", password="", token=""):
        if username != "" and password == "":
            self.db_worker(query="DELETE FROM user WHERE UserId = ?", param=[username,])
            return 1
        elif username != "" and password != "":
            self.db_worker(query="DELETE FROM user WHERE token = ?", param=[generate_token(username, password)])
            return 1
        elif token != "":
            self.db_worker(query="DELETE FROM user WHERE token = ?", param=[generate_token(username, password)])
            return 1

    def create(self, password="", email="", username="", is_admin="", is_banned="", logo_path="",
               citate="", format="obj"):
        self.db_worker(query="""INSERT INTO user VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ) """,
                      param=[email, username, is_admin, is_banned, logo_path, citate,
                             get_current_time(), generate_token(username, password), randint(0, 10 ** 6), 0, 0])
        return self.get(username=username, password=password, format = "obj")
