import configparser
import os
from pathlib import *

from classes.loggers import *
from classes.tools import *
from classes.forum import *
from classes.user_class import *
from classes.serv import *
from classes.database import *


"""
#getting data about Postgres database
#you can change on another db

port = os.environ.get('port')
password =  os.environ.get("password")
user = os.environ.get("user")
name = os.environ.get("name")
host = os.eenviron.get("host")

"""


a_logger = txt_log(path=Path.cwd(),filename="a.log")
#db  = PostgresDb(port=port, password=password, user=user, name=name, host = host)
db = sql_lite3_db("main.db")
initialise_database(db=db)



fr_m = forum(db, "Forum")
A = server(dbg=True, class_logger=a_logger, db=db ,frm=fr_m)



