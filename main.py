import configparser
from pathlib import *

from classes.loggers import *
from classes.tools import *
from classes.forum import *
from classes.user_class import *
from classes.serv import *
from classes.database import *
from classes.logger import *
from classes.inters import *


Log = txt_log(Path=Path.cwd(),filename="a.log")
db  = sql_lite3_db("main.db")

Db = IDbMutable(db)
Logger = ILoggerMutable(Log)

initialise_database(db=Db)



fr_m = forum(Db, "Forum")
A = server(dbg=True, class_logger=Logger, db=Db ,frm=fr_m)
A.runserver()


