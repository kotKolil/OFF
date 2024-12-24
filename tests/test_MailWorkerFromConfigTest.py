# External libraries
import sys

# Adding classes to path
sys.path.append('..')
sys.path.append('...')

# importing local libraries
from app.classes.ApplicationPart.MailClient import *
from config import *
from app.classes.ApplicationPart.loggers import *


def test_MailWorkerConfigTest():
    logger = Logger()

    mail_worker = MailClient(SiteAdress=MailSite, SitePort=MailPort, MailLogin=MailLogin, MailPassword=MailPassword,
                             ForumName=ForumName, logger=logger)

    mail_worker.SendMessage(MailLogin, "It works!", "MailWorker test")
