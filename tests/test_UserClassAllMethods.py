# External libraries
import sys

# Adding classes to path
sys.path.append('..')

# Importing local classes
from app.classes.ApplicationPart.database import *
from app.classes.ApplicationPart.loggers import *
from app.classes.other.tools import *

# Creating DBWorker object and initializing database
DBWorker = DB()
DBWorker.db_init()

# Defining data of example user for tests in User() class
SimpleUserData = {
    "password": "123",
    "email": "mail@example.com",
    "username": "user",
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
        UserObject = DBWorker.user().create(**SimpleUserData)

        UserObj = UserObject

        # Creating user with different id to raise error of unique values
        DBWorker.user().create(password="1234567890", email="example@example.com", username="user", is_admin="0",
                               is_banned="0", logo_path="", citate="", format="obj")

    except (sqlite3.IntegrityError, psycopg2.errors.UniqueViolation) as e:
        assert isinstance(e, (sqlite3.IntegrityError, psycopg2.errors.UniqueViolation))

    try:
        # Creating user with same email to raise error of unique values
        DBWorker.user().create(password="1234567890", email="mail@example.com", username="user1", is_admin="0",
                               is_banned="0", logo_path="", citate="", format="obj")

    except (sqlite3.IntegrityError, psycopg2.errors.UniqueViolation) as e:
        assert isinstance(e, (sqlite3.IntegrityError, psycopg2.errors.UniqueViolation))


def test_TestOfGetMethod():
    # Testing get method in User class

    # checking output data as a obj
    # Checking getting user data from user id
    assert isinstance(DBWorker.user().get(username=SimpleUserData["username"], format="obj"), UserStorage)

    # Checking getting user data from user id and password
    assert isinstance(
        DBWorker.user().get(username=SimpleUserData["username"], password=SimpleUserData["password"], format="obj"),
        UserStorage)

    # Checking getting user data via token, created as a hash from password and user id
    assert isinstance(
        DBWorker.user().get(token=generate_token(s1=SimpleUserData["username"], s2=SimpleUserData["password"]),
                            format="obj"), UserStorage)

    assert DBWorker.user().get(username="UserNotExist", format="obj") == 0


def test_TestOfAllMethod():
    # testing all method in User class

    # creating new user in DB

    DBWorker.user().create(password="1234567890", email="example5@example.com", username="user5", is_admin="0",
                           is_banned="0", logo_path="", citate="", format="obj")

    AllUsers = DBWorker.user().all(format="obj")

    for i in AllUsers:
        print(i.__dict__)

        SomeUser = DBWorker.user().get(username=i.UserId, format="obj")

        assert i.__dict__ == SomeUser.__dict__


def test_TestOfModifyData():
    global UserObj

    # modifying object
    UserObj.UserId = "User777"
    UserObj.save()

    # checking local object and data from DB
    assert UserObj.__dict__ == DBWorker.user().get(username=UserObj.UserId, format="obj").__dict__


def test_TestOfDeleteMethod():
    # testing delete method in User class

    # creating new user in DB
    NewUser = DBWorker.user().create(password="1234567890", email="example7@example.com", username="user7", is_admin="0",
                                     is_banned="0", logo_path="", citate="", format="obj")
    # deleting him via user id
    assert DBWorker.user().delete(username=NewUser.UserId) == 1

    # creating new user in DB
    NewUser = DBWorker.user().create(password="1234567890", email="example7@example.com", username="user7", is_admin="0",
                                     is_banned="0", logo_path="", citate="", format="obj")
    # deleting him via user id and password
    assert DBWorker.user().delete(username=NewUser.UserId, password="1234567890") == 1

    # creating new user in DB
    DBWorker.user().create(password="1234567890", email="example7@example.com", username="user7", is_admin="0",
                           is_banned="0", logo_path="", citate="", format="obj")
    # deleting him via his token
    token = generate_token("user7", "1234567890")
    assert DBWorker.user().delete(token=token) == 1
