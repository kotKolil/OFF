# External libraries
import sys

# Adding classes to path
sys.path.append('..')

# Importing local classes
from classes.database import *
from classes.loggers import *

# Creating DBWorker object and initializing database
DBWorker = DB()
DBWorker.DBInit()

# Setting logger
Logger = Logger()

# Defining data of example topic for tests in Topic() class
SimpleTopicData = {
    "theme":"theme",
    "author":"author",
    "about":'about',
    "protected":"0",
}



def test_TestOfCreationMethod():
    # Testing create method in Topic class

        # Creating topic
        DBWorker.Topic().create(**SimpleTopicData)

def test_TestOfGetMethod():
    # Testing get method in Topic class


    # checking ouptut data as a obj
    # Checking getting topic data from topic id
    TopicObject = DBWorker.Topic().create(**SimpleTopicData)
    Topic = DBWorker.Topic().get(TopicId = TopicObject.TopicId, format = "obj")
    assert Topic.__dict__ == TopicObject.__dict__


def test_TestOfAllMethod():
    # testing all method in Topic class

    # creating new topic in DB
    DBWorker.Topic().create(**SimpleTopicData, format="obj")

    AllUsers = DBWorker.Topic().all(format="obj")

    #iterating them
    for i in AllUsers:
        print(i.__dict__)
        SomeTopic = DBWorker.Topic().get(TopicId=i.TopicId, format="obj")

        assert i.__dict__ == SomeTopic.__dict__


def test_TestOfModifyData():

    TopicObject = DBWorker.Topic().create(**SimpleTopicData, format = "obj")

    TopicObject.theme = "awesome theme"
    TopicObject.about = "awesome about"
    TopicObject.save()

    assert TopicObject.__dict__ == DBWorker.Topic().get(TopicId=TopicObject.TopicId, format="obj").__dict__