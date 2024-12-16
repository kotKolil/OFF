# External libraries
import sys

# Adding classes to path
sys.path.append('..')

# Importing local classes
from app.classes.ApplicationPart.database import *
from app.classes.ApplicationPart.loggers import *

# Creating DBWorker object and initializing database
DBWorker = DB()
DBWorker.DBInit()

# Setting logger
Logger = Logger()

# Defining data of example topic for tests in Topic() class
SimpleTopicData = {
    "theme": "theme",
    "author": "author",
    "about": 'about',
    "protected": "0",
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
    Topic = DBWorker.Topic().get(TopicId=TopicObject.TopicId, format="obj")
    assert Topic.__dict__ == TopicObject.__dict__


def test_TestOfAllMethod():
    # testing all method in Topic class

    # creating new topic in DB
    DBWorker.Topic().create(**SimpleTopicData, format="obj")

    AllUsers = DBWorker.Topic().all(format="obj")

    # iterating them
    for i in AllUsers:
        print(i.__dict__)
        SomeTopic = DBWorker.Topic().get(TopicId=i.TopicId, format="obj")

        assert i.__dict__ == SomeTopic.__dict__


def test_TestOfModifyData():
    # testing object modifyng

    TopicObject = DBWorker.Topic().create(**SimpleTopicData, format="obj")

    #modifying object via object fields
    TopicObject.theme = "awesome theme"
    TopicObject.about = "awesome about"
    #saving object
    TopicObject.save()

    #checking local object and data from DB
    assert TopicObject.__dict__ == DBWorker.Topic().get(TopicId=TopicObject.TopicId, format="obj").__dict__


def test_TestOfDeleteMethod():
    # testing delete method

    # creating new topic
    TopicObject = DBWorker.Topic().create(**SimpleTopicData, format="obj")

    # if deletion is successful, function will return 1
    assert DBWorker.Topic().delete(TopicId=TopicObject.TopicId) == 1
