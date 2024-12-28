# External libraries
import sys

# Adding classes to path
sys.path.append('..')

# Importing local classes
from app.classes.ApplicationPart.database import *

# Creating DBWorker object and initializing database
DBWorker = DB()
DBWorker.db_init()
# Defining data of example topic for tests
SimpleTopicData = {
    "theme": "theme",
    "author": "author",
    "about": 'about',
    "protected": "0",
}

# creating topic for messages
SampleTopic = DBWorker.topic().create(**SimpleTopicData)

# Defining data of example message for tests in message() class
SimpleMsgData = {
    "TopicId": SampleTopic.TopicId,
    "author": "SomeUser",
    "text": "simple text",
}


def test_TestOfCreationMethod():
    # Testing create method in Message class
    # Creating message
    simple_msg_obj = DBWorker.message().create(format="obj", **SimpleMsgData)
    assert simple_msg_obj


def test_TestOfGetMethod():
    # Testing get method in Message class
    # Checking getting message via message id in object format
    simple_msg_obj = DBWorker.message().create(format="obj", **SimpleMsgData)

    # Checking getting message via message id in object format
    some_message = DBWorker.message().get(format="obj", MessageId=simple_msg_obj.MessageId)

    assert simple_msg_obj.__dict__ == some_message.__dict__

    # checking getting message via message id in json format
    some_message = DBWorker.message().get(format="json", MessageId=simple_msg_obj.MessageId)

    # removing DBWorker from MsgFromDB, this variable not in MsgFromDB
    del simple_msg_obj.__dict__["DBWorker"]

    assert simple_msg_obj.__dict__ == some_message

    # Checking getting message via topic id in object format
    for i in DBWorker.message().get(TopicId=SampleTopic.TopicId, format="obj"):
        some_message = DBWorker.message().get(MessageId=i.MessageId, format="obj")

        assert i.__dict__ == some_message.__dict__

    # checking getting message via topic id in json format
    for i in DBWorker.message().get(TopicId=SampleTopic.TopicId, format="json"):
        some_message = DBWorker.message().get(MessageId=i["MessageId"], format="json")
        assert i == some_message


def test_TestOfAllMethod():
    # getting data from DB in object format
    some_msg = DBWorker.message().all(format="obj")

    # iterating them
    for i in some_msg:
        some_msg = DBWorker.message().get(MessageId=i.MessageId, format="obj")

        # check data equality
        assert i.__dict__ == some_msg.__dict__

    # getting data from DB in json format
    some_msg = DBWorker.message().all(format="json")

    # iterating them
    for i in some_msg:
        some_msg = DBWorker.message().get(MessageId=i["MessageId"], format="json")

        # check data equality
        assert i == some_msg


def test_TestOfModifyData():
    # creating new object
    msg_object = DBWorker.message().create(format="obj", **SimpleMsgData)

    # modifying it
    msg_object.text = "awesome text"
    msg_object.save()

    new_msg_object = DBWorker.message().get(MessageId=msg_object.MessageId, format="obj")

    # checking local object and data from DB
    assert new_msg_object.__dict__ == msg_object.__dict__


def test_TestOfDeleteMethod():
    # creating new object
    msg_object = DBWorker.message().create(format="obj", **SimpleMsgData)

    # if deletion successful, function will return 1
    assert DBWorker.message().delete(MessageId=msg_object.MessageId) == 1
