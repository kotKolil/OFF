# External libraries
import sys

# Adding classes to path
sys.path.append('..')

# Importing local classes
from app.classes.ApplicationPart.loggers import *


def test_TestingUnknownTypeOfLogger():
    try:
        Logger("awesome type")
    except Exception as e:
        assert isinstance(e, TypeError)


def test_TestingConsoleLogger():
    # creating new logger
    console_logger = Logger("console")

    # testing functions
    console_logger.info("connection established")
    console_logger.warning("invalid HTTP headers")
    console_logger.error("kernel panik")


def test_TestingTxtLogger():
    # creating new logger
    console_logger = Logger("txt", name_of_file="main.txt")

    # testing functions
    console_logger.info("connection established")
    console_logger.warning("invalid HTTP headers")
    console_logger.error("kernel panik")