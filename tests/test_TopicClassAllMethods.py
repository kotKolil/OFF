# External libraries
import sys

# Adding classes to path
sys.path.append('..')

# Importing local classes
from app.classes.ApplicationPart.database import *
from app.classes.ApplicationPart.loggers import *

# Creating DBWorker object and initializing database
DBWorker = DB()
DBWorker.db_init()

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
    DBWorker.topic().create(**SimpleTopicData)


def test_TestOfGetMethod():
    # Testing get method in Topic class

    # checking output data as an obj
    # Checking getting topic data from topic id
    topic_object = DBWorker.topic().create(**SimpleTopicData)
    topic = DBWorker.topic().get(TopicId=topic_object.TopicId, format="obj")
    assert topic.__dict__ == topic_object.__dict__


def test_TestOfAllMethod():
    # testing all method in Topic class

    # creating new topic in DB
    DBWorker.topic().create(format="obj", **SimpleTopicData)

    all_users = DBWorker.topic().all(format="obj")

    # iterating them
    for i in all_users:
        print(i.__dict__)
        SomeTopic = DBWorker.topic().get(TopicId=i.TopicId, format="obj")

        assert i.__dict__ == SomeTopic.__dict__


def test_TestOfModifyData():
    # testing object modifying

    TopicObject = DBWorker.topic().create(format="obj", **SimpleTopicData)

    # modifying object via object fields
    TopicObject.theme = "awesome theme"
    TopicObject.about = "awesome about"
    # saving object
    TopicObject.save()

    # checking local object and data from DB
    assert TopicObject.__dict__ == DBWorker.topic().get(TopicId=TopicObject.TopicId, format="obj").__dict__


def test_TestOfDeleteMethod():
    # testing delete method

    # creating new topic
    TopicObject = DBWorker.topic().create(**SimpleTopicData)

    # if deletion is successful, function will return 1
    assert DBWorker.topic().delete(TopicId=TopicObject.TopicId) == 1
