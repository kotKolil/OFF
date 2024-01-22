from pathlib import *
from classes.loggers import *
from classes.tools import *

a_logger = txt_log(p4th=Path.cwd(),filename="a.log")
db  = sql_lite3_db("main.db")
initialise_database(db=db)


from classes.serv import *
from classes.database import *

A = server(dbg=True, class_logger=a_logger, db=db)
A.runserver()


