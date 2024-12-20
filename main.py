from classes.loggers import *
from classes.serv import *
from classes.database import *
from classes.MailClient import *
from config import *

import sys

logger = Logger(logger_type=logger_type)

db = DB(DBType=DBtype, name=DBname, port=DBport, user=DBuser, password=DBpassword)
db.DBInit()
logger.info("db inited")

MailWorker = MailClient(SiteAdress=MailSite, SitePort=MailPort, MailLogin=MailLogin, MailPassword=MailPassword,
                        ForumName=ForumName, logger = logger)



if __name__ == "__main__":
    try:
        A = server(IsDebug=IsDebug, ClassLoger=logger, DBWorker=db, AdminUser=AdminUser,
               AdminName=AdminName, AdminPassword=AdminPassword, AdminCitate=AdminCitate,
               AdminLogoPath=AdminLogoPath, ForumName=ForumName, AppSecretKey=AppSecretKey, JwtSecretKey=JwtSecretKey,
               MailWorker=MailWorker, port=APPport, host=APPhost)
        input()
        sys.exit(0)
    except Exception as e:
        print(e)
        input()
        sys.exit(1)
