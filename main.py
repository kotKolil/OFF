import configparser
from pathlib import *

from classes.loggers import *
from classes.tools import *
from classes.user import *
from classes.serv import *
from classes.database import *
from config import *

a_logger = txt_log(path=LogPath,filename=LogFilename)
db = DB(DBType="sqlite3",path="main.db")
db.DBInit()
A = server(dbg=is_debug, class_logger=a_logger, db=db , AdminUser =  AdminUser, AdminName =  AdminName, AdminPassword =  AdminPassword, AdminCitate = AdminCitate,AdminLogoPath = AdminLogoPath)