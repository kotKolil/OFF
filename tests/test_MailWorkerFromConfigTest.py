# External libraries
import sys

# Adding classes to path
sys.path.append('..')
sys.path.append('...')

#importing local libraries
from app.MailClient import *
from config import *
from app.loggers import *

def test_MailWorkerConfigTest():

    logger = Logger()

    MailWorker = MailClient(SiteAdress=MailSite, SitePort=MailPort, MailLogin=MailLogin, MailPassword=MailPassword,
                        ForumName=ForumName, logger = logger)

    MailWorker.SendMessage(MailLogin, "It works!", "MailWorker test")