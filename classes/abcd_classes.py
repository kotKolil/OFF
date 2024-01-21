from abc import *
from flask import *
from .loggers import *

class abc_db:

    __metaclass__ = ABCMeta

    def __init__(self, port=5432, password="admin", user="admin", name="", host="127.0.0.1"):
        self.port = port
        self.password = password
        self.user = user
        self.name = name
    
    @abstractclassmethod
    def excute_expression(self, query):
        #logic of sending SQL script to Database
        pass

class abc_log:

    __metaclass__ = ABCMeta

    def __init__(self, filename,p4th):
        self.p4th = p4th
        self.filename = filename

    @abstractmethod
    def log_message(text):
        pass


class sub_disscussion:

    __metaclass__ = ABCMeta

    def __init__(self, time_of_creation, theme,author,about, sb_id, db:object):
        self.time_of_creation = time_of_creation
        self.theme = theme
        self.author = author
        self.about = about
        self.name = about
        self.sb_id = sb_id
        self.db = db
    def all(self):
        pass
    
    def get(self, sb_id):
        pass
    def delete(self, sb_id):
        pass
    
    def create(self, sb_id):
        pass
    def update(self, sb_id):
        pass