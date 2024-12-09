from classes.MailClient import *
from classes.database import *
from classes.serv import *
from config import *

logger = Logger(logger_type=logger_type)

db = DB(DBType=DBtype, name=DBname, port=DBport, user=DBuser, password=DBpassword)
db.DBInit()
logger.info("db inited")

MailWorker = MailClient(SiteAdress=MailSite, SitePort=MailPort, MailLogin=MailLogin, MailPassword=MailPassword,
                        ForumName=ForumName, logger = logger)



if __name__ == "__main__":
    try:
        A = Server(is_debug=IsDebug, class_loger=logger, db_worker=db, admin_user=AdminUser,
                   admin_name=AdminName, admin_password=AdminPassword, admin_citate=AdminCitate,
                   admin_logo_path=AdminLogoPath, forum_name=ForumName, app_secret_key=AppSecretKey,
                   jwt_secret_key=JwtSecretKey,
                   mail_worker=MailWorker, port=APPport, host=APPhost)
        input()
        sys.exit(0)
    except Exception as e:
        print(e)
        input()
        sys.exit(1)
