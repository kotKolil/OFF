# External libraries
import sys

# Adding classes to path
sys.path.append('..')

# Importing local classes
from classes.database import *
from classes.loggers import *

def test_TestingUnknownTypeOfLogger():

    try:
        Logger("awesome type")
    except Exception as e:
        assert isinstance(e, TypeError)

def test_TestingConsoleLogger():

    #creating new logger
    ConsoleLogger = Logger("console")

    #testing functions
    ConsoleLogger.info("connection estabilished")
    ConsoleLogger.warning("invalid HTTP headers")
    ConsoleLogger.error("kernel panik")

def test_TestingTxtLogger():
    #creating new logger
    ConsoleLogger = Logger("txt", name_of_file="main.txt")

    #testing functions
    ConsoleLogger.info("connection estabilished")
    ConsoleLogger.warning("invalid HTTP headers")
    ConsoleLogger.error("kernel panik")

def test_TestingTxtLogger():
    #creating new logger
    ConsoleLogger = Logger("json", name_of_file="main.json")

    #testing functions
    ConsoleLogger.info("connection estabilished")
    ConsoleLogger.warning("invalid HTTP headers")
    ConsoleLogger.error("kernel panik")
