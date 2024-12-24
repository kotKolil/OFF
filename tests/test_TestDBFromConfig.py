# External libraries
import sys

# Adding classes to path
sys.path.append('..')
sys.path.append('...')

# importing local libraries
from app.classes.ApplicationPart.database import *
from config import *


def test_TestingDBFromConfig():
    DB(DBType=DBtype, port=DBport, host=DBhost, name=DBname, password=DBpassword, user=DBuser, )
