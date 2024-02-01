from pathlib import *
from classes.loggers import *
from classes.tools import *
from classes.forum import *

a_logger = txt_log(p4th=Path.cwd(),filename="a.log")
db  = sql_lite3_db("main.db")
initialise_database(db=db)


from classes.serv import *
from classes.database import *

fr_m = forum(db, "Forum")
A = server(dbg=True, class_logger=a_logger, db=db ,frm=fr_m)
A.runserver()


