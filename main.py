from classes.loggers import *
from pathlib import *
from classes.serv import *
from classes.database import *

# a_logger = txt_log(p4th=Path.cwd(),filename="a.log")
db  = sql_lite3_db("main.db")
initialise_database(db=db)
# A = server(dbg=True, class_logger=a_logger)
# A.runserver()
