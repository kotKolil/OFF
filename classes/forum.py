from database import *
from loggers import *
from tools import *
from abc_class import *


class forum:

    def __init__(self, db=sql_lite3_db("db.db"), name="forum"):

        self.__db  = db
        self.__name = name

        #creating table in database, which related with forum with SQL script
        #structure of table forum : name;date_of_creasting;id
        db.execute_query(f"INSERT INTO forums VALUES ({self._name}, {get_current_time()}, {generate_id}) ")

    def thread(method="POST"):
            pass