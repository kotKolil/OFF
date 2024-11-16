# adding classes to path
import sys
sys.path.append('..')
from time import sleep
from classes.database import *
import psycopg2
import sqlite3
from classes.tools import *

class UserClassAllMethodstest(object):
    #defining data of example user for tests User() class
    SimpleUserData = {
        "password":"123",
        'email': 'mail@example.com',
        "user":"user",
        "is_admin":"0",
        "is_banned":'0',
        "is_banned":"0",
        "logo_path":'',
        "citate":"",
        "format":"",

    }

    def __init__(self, DBWorker=DB()):
        self.DBWorker = DBWorker
        DBWorker.db.DBInit()

    # checking methods of User() class
    def TestClass(self):

        """
        checks create method

        #in first case we are checking creation of new user
        #in second case we are checking error from same emails
        #in third case we are checking errors from same user ID
        """

        assert self.DBWorker.User().create(**UserClassAllMethodstest.SimpleUserData)

        

        try:
            self.DBWorker.User().create(**UserClassAllMethodstest.SimpleUserData)
            self.DBWorker.User().create(password="1234567890", email="example@example.com", user="user1", is_admin="",
                                  is_banned="", logo_path="", citate="", format="obj")
        except Exception as e:

            assert type(e) == sqlite3.IntegrityError or type(e) == psycopg2.errors.UniqueViolation

        

        try:
            self.DBWorker.User().create(password="1234567890", email="example2@example.com", user="user", is_admin="",
                                    is_banned="", logo_path="", citate="", format="obj")

            self.DBWorker.User().create(password="1234567890", email="example2@example.com", user="user", is_admin="",\
                                  is_banned="", logo_path="",\
                                  citate="", format="obj")


        except Exception as e:
            
            print(e)
            assert type(e) == sqlite3.IntegrityError or type(e) == psycopg2.errors.UniqueViolation

        


        """
        checks get method
        
        in first case we checking receiving user by his user id
        in second case we checking receiving user by his user id and password
        in second case we checking receiving user by his token, created as a hash from password and user id
        in four case we checking getting user from num
        in case 5 we checking getting data in json (dict in python) format
        in case 6 we checking getting data from not existing user id
        
        """

        assert self.DBWorker.User().get(user = UserClassAllMethodstest.SimpleUserData["user"], format = "obj").UserId == \
               UserClassAllMethodstest.SimpleUserData["user"]

        

        assert self.DBWorker.User().get(user=UserClassAllMethodstest.SimpleUserData["user"], password = \
                                   UserClassAllMethodstest.SimpleUserData["password"], format = "obj").UserId == \
               UserClassAllMethodstest.SimpleUserData['user']

        


        token = generate_token(UserClassAllMethodstest.SimpleUserData["user"],UserClassAllMethodstest.SimpleUserData["password"])

        assert self.DBWorker().get(token=token, format = "obj").UserId ==\
               UserClassAllMethodstest["user"]
        


        TestUser = self.DBWorker.User().create(password="1234567890", email="exampl4e@example.com", user="user5", is_admin="",
                                  is_banned="", logo_path="",
                                  citate="", format="obj")

        

        assert self.DBWorker.User().get(num = TestUser.ActiveNum).__dict__ == TestUser.__dict__

        


        assert self.DBWorker.User().get(user = UserClassAllMethodstest.SimpleUserData["user"], format = "json")["UserId"] == \
               UserClassAllMethodstest.SimpleUserData["user"]

        

        """
        checks data changing via UserStorage() class
        """

        UserData = self.DBWorker.User().get(user = UserClassAllMethodstest.SimpleUserData["user"], format = "obj")

        try:

            UserData.email = "example1337@example.com"
            UserData.UserId = "user1337"
            UserData.IsAdmin = "1"
            UserData.IsBanned = "1"
            UserData.LogoPath = "sample_image"
            UserData.citate = "sample quote"
            UserData.time = "13:37:14"
            UserData.ActiveNum = "1337"
            self.IsActivated = "1"
            self.NumOfPosts = "666"

            UserData.save()

        except Exception as e:

            raise AssertionError

        """
        checks delete method
        
        in case 1 we checking deleting data via user id
        in case 2 we checking deleting data via user id and password
        in case 3 we checking deleting via token created as a hash from user id and password
        """

        assert self.DBWorker.User().delete(user == UserClassAllMethodstest.SimpleUserData["user"]) == 1
        assert self.DBWorker.User().create(**UserClassAllMethodstest.SimpleUserData)

        assert self.DBWorker.User().delete(user == UserClassAllMethodstest.SimpleUserData["user"], password = UserClassAllMethodstest.SimpleUserData["password"]) == 1
        assert self.DBWorker.User().create(**UserClassAllMethodstest.SimpleUserData)

        assert self.DBWorker.User().delete(token = token) == 1

if __name__ == '__main__':
    UserClassAllMethodstest().TestClass()