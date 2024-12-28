# External libraries
import sys

# Adding classes to path
sys.path.append('..')
sys.path.append('...')

# importing local libraries
from app.classes.ApplicationPart.database import *
from config import *


def test_TestingDBFromConfig():
    DB(DBType=db_type, port=db_port, host=db_host, name=db_name, password=db_password, user=db_user, )
