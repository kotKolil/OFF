# External libraries
import sys
import os
from time import sleep
import psycopg2
import sqlite3

# Adding classes to path
sys.path.append('..')

# Importing local classes
from app.database import *
from app.loggers import *
from app.tools import *

# Creating DBWorker object and initializing database
DBWorker = DB()
DBWorker.DBInit()

# Setting logger
Logger = Logger()

# Defining data of example user for tests in User() class
SimpleUserData = {
    "password": "123",
    "email": "mail@example.com",
    "user": "user",
    "is_admin": "0",
    "is_banned": "0",
    "logo_path": "",
    "citate": "",
    "format": "",
}

UserObj = []

def test_TestOfCreationMethod():
    # Testing create method in User class
    try:
        
        global UserObj

        # Creating sample user
        UserObject = DBWorker.User().create(**SimpleUserData)

        UserObj = UserObject

        # Creating user with different id to raise error of unique values
        DBWorker.User().create(password="1234567890", email="example@example.com", user="user", is_admin="0",
                               is_banned="0", logo_path="", citate="", format="obj")

    except (sqlite3.IntegrityError, psycopg2.errors.UniqueViolation) as e:
        assert isinstance(e, (sqlite3.IntegrityError, psycopg2.errors.UniqueViolation))

    try:
        # Creating user with same email to raise error of unique values
        DBWorker.User().create(password="1234567890", email="mail@example.com", user="user1", is_admin="0",
                               is_banned="0", logo_path="", citate="", format="obj")

    except (sqlite3.IntegrityError, psycopg2.errors.UniqueViolation) as e:
        assert isinstance(e, (sqlite3.IntegrityError, psycopg2.errors.UniqueViolation)) 

def test_TestOfGetMethod():
    # Testing get method in User class

    #checking ouptut data as a obj
    # Checking getting user data from user id
    assert isinstance(DBWorker.User().get(user=SimpleUserData["user"], format="obj"), UserStorage)

    # Checking getting user data from user id and password
    assert isinstance(DBWorker.User().get(user=SimpleUserData["user"], password=SimpleUserData["password"], format="obj"), UserStorage)

    # Checking getting user data via token, created as a hash from password and user id
    assert isinstance(DBWorker.User().get(token=generate_token(s1=SimpleUserData["user"], s2=SimpleUserData["password"]), format="obj"), UserStorage)

    assert DBWorker.User().get(user = "UserNotExist", format="obj") == 0

def test_TestOfAllMethod():
    #testing all method in User class

    #creaeting new user in DB

    DBWorker.User().create(password="1234567890", email="example5@example.com", user="user5", is_admin="0",
                               is_banned="0", logo_path="", citate="", format="obj")

    AllUsers = DBWorker.User().all(format = "obj")


    for i in AllUsers:

        print(i.__dict__)

        SomeUser = DBWorker.User().get(user=i.UserId, format="obj")

        assert i.__dict__ == SomeUser.__dict__

def test_TestOfModifyData():

    global UserObj

    #modifyning object
    UserObj.UserId = "User777"
    UserObj.save()

    # checking local object and data from DB
    assert UserObj.__dict__ == DBWorker.User().get(user = UserObj.UserId, format = "obj").__dict__

def test_TestOfDeleteMethod():
    #testing delete method in User class

    #creating new user in DB
    NewUser = DBWorker.User().create(password="1234567890", email="example7@example.com", user="user7", is_admin="0",
                               is_banned="0", logo_path="", citate="", format="obj")
    #deleting him via user id
    assert DBWorker.User().delete(user = NewUser.UserId) == 1


    #creating new user in DB
    NewUser = DBWorker.User().create(password="1234567890", email="example7@example.com", user="user7", is_admin="0",
                               is_banned="0", logo_path="", citate="", format="obj")
    #deleting him via user id and password
    assert DBWorker.User().delete(user = NewUser.UserId, password= "1234567890") == 1


    #creating new user in DB
    NewUser = DBWorker.User().create(password="1234567890", email="example7@example.com", user="user7", is_admin="0",
                               is_banned="0", logo_path="", citate="", format="obj")
    #deleting him via his token
    token = generate_token("user7", "1234567890")
    assert DBWorker.User().delete(token=token) == 1
