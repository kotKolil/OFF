from app.serv import *
from app.classes.ApplicationPart.database import *
from app.classes.ApplicationPart.MailClient import *
from config import *

import sys

logger = Logger(logger_type=logger_type)

db = DB(DBType=db_type, name=db_name, port=db_port, user=db_user, password=db_password)
db.db_init()
logger.info("db inited")

MailWorker = MailClient(SiteAddress=MailSite, SitePort=MailPort, MailLogin=MailLogin, MailPassword=MailPassword,
                        ForumName=ForumName, logger=logger)

if __name__ == "__main__":
    # try:
    A = server(IsDebug=IsDebug, ClassLoger=logger, DBWorker=db, AdminUser=AdminUser,
               AdminName=AdminName, AdminPassword=AdminPassword, AdminCitate=AdminCitate,
               AdminLogoPath=AdminLogoPath, ForumName=ForumName, AppSecretKey=AppSecretKey,
               JwtSecretKey=JwtSecretKey,
               MailWorker=MailWorker, port=app_port, host=app_host)
    A.run()
    # except Exception as e:
    #     print(e)
    #     sys.exit(1)
