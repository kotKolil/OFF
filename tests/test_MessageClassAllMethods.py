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

# Defining data of example topic for tests
SimpleTopicData = {
    "theme":"theme",
    "author":"author",
    "about":'about',
    "protected":"0",
}

#creating topic for messages
SampleTopic =DBWorker.Topic().create(**SimpleTopicData)

# Defining data of example message for tests in Message() class
SimpleMsgData = {
    "TopicId":SampleTopic.TopicId,
    "author":"SomeUser",
    "text":"simple text",
}
def test_TestOfCreationMethod():
    # Testing create method in Message class
    # Creating message
    SimpleMsgObj = DBWorker.Message().create(**SimpleMsgData, format = "obj")
    assert SimpleMsgObj

def test_TestOfGetMethod():
    # Testing get method in Message class
    # Checking getting message via message id in object format
    SimpleMsgObj = DBWorker.Message().create(**SimpleMsgData, format = "obj")

    # Checking getting message via message id in object format
    MsgFromDB = DBWorker.Message().get(MessageId =  SimpleMsgObj.MessageId, format = "obj")

    assert SimpleMsgObj.__dict__ == MsgFromDB.__dict__

    #checking getting message via message id in json format
    MsgFromDB = DBWorker.Message().get(MessageId=SimpleMsgObj.MessageId, format="json")

    #removing DBWorker from MsgFromDB, this variable not in MsgFromDB
    del SimpleMsgObj.__dict__["DBWorker"]

    assert SimpleMsgObj.__dict__ == MsgFromDB

    # Checking getting message via topic id in object format
    for i in DBWorker.Message().get( TopicId = SampleTopic.TopicId,format = "obj"):
        SomeMessage = DBWorker.Message().get(MessageId=i.MessageId, format="obj")

        assert i.__dict__ == SomeMessage.__dict__

    #checking getting message via topic id in json format
    for i in DBWorker.Message().get(TopicId = SampleTopic.TopicId, format = "json"):
        SomeMessage = DBWorker.Message().get(MessageId=i["MessageId"], format="json")
        assert i == SomeMessage

def test_TestOfAllMethod():

    #getting data from DB in object format
    SomeMsgs = DBWorker.Message().all(format="obj")

    #iterating them
    for i in SomeMsgs:
        SomeMsg = DBWorker.Message().get(MessageId=i.MessageId, format="obj")

        #check data equality
        assert i.__dict__ == SomeMsg.__dict__

    # getting data from DB in json format
    SomeMsgs = DBWorker.Message().all(format="json")

    # iterating them
    for i in SomeMsgs:
        SomeMsg = DBWorker.Message().get(MessageId=i["MessageId"], format="json")

        # check data equality
        assert i == SomeMsg


def test_TestOfModifyData():

    #creating new object
    MsgObject = DBWorker.Message().create(**SimpleMsgData, format = "obj")

    #modifying it
    MsgObject.text = "awesome text"
    MsgObject.save()

    NewMsgObject = DBWorker.Message().get(MessageId=MsgObject.MessageId, format="obj")

    #checking local object and data from DB
    assert NewMsgObject.__dict__ == MsgObject.__dict__

def test_TestOfDeleteMethod():

    #creating new object
    MsgObject = DBWorker.Message().create(**SimpleMsgData, format = "obj")

    #if deletion successful, function will return 1
    assert DBWorker.Message().delete(MessageId = MsgObject.MessageId) == 1