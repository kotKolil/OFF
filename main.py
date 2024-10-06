import configparser
from pathlib import *

from classes.loggers import *
from classes.tools import *
from classes.user import *
from classes.serv import *
from classes.database import *
from classes.MailClient import *
from config import *

a_logger = txt_log(path=LogPath,filename=LogFilename)

db = DB(DBType="sqlite3",path="main.db")
db.DBInit()

# MailObject = MailClient(SiteAdress, SitePort, MailLogin, MailPassword)
A = server(IsDebug=IsDebug, ClassLoger=a_logger, DBWorker=db , AdminUser =  AdminUser,
            AdminName =  AdminName, AdminPassword =  AdminPassword, AdminCitate = AdminCitate,
            AdminLogoPath = AdminLogoPath, ForumName = ForumName)
