import configparser
from pathlib import *

from classes.loggers import *
from classes.tools import *
from classes.forum import *
from classes.user_class import *
from classes.serv import *
from classes.database import *
from config import *


a_logger = txt_log(path=LogPath,filename=LogFilename)
db = sql_lite3_db(DBname)
initialise_database(db=db)

fr_m = forum(db, forum_name)
A = server(dbg=is_debug, class_logger=a_logger, db=db ,frm=fr_m, AdminUser =  AdminUser, AdminName =  AdminName, AdminPassword =  AdminPassword)