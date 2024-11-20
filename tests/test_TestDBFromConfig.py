# External libraries
import sys

# Adding classes to path
sys.path.append('..')
sys.path.append('...')

#importing local libraries
from classes.database import *
from config import *
from config import *

def test_TestingSQLite3Class():

    #creating DB object
    DBWorker = DB()
    #testing DB initialization
    DBWorker.DBInit()


def test_TestingPSQLClass():

    #creating DB object
    DBWorker = DB(DBType="postgres",host = DBhost, port = DBport, name = DBname, user = DBuser, password = DBpassword)
    #testing DB initialization
    DBWorker.DBInit()