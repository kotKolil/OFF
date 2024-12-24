# importing external libs
import requests as r
import sys

# adding paths to venv
sys.path.append("...")
sys.path.append("..")

# importing local classes
from config import *

BASE_URL = "http://{}:{}/api/topic".format(APPhost, APPport)  # api entrypoint URI

# generating user token
request_data = r.post(
    "http://{}:{}/api/user/generate_token".format(APPhost, APPport),
    json={
        "user": AdminUser,
        "password": AdminPassword,
    },
    headers={
        'Content-Type': 'application/json'
    }
)

valid_token = request_data.json()["JWToken"]

topic_data = {
    "theme": "Test Topic",
    "about": "This is a test topic.",
    "is_protected": "0"
}


# creating topic
def test_TopicCreation():
    global topic_data

    response = r.post(
        BASE_URL,
        json={
            "token": str(valid_token),
            "theme": topic_data["theme"],
            "about": topic_data["about"],
            "is_protected": topic_data["is_protected"]
        },
        headers={
            'Content-Type': 'application/json'
        }
    )

    topic_data = response.json()
    assert response.status_code == 200


def test_TopicGet():
    response = r.get(
        BASE_URL + "?TopicId={}".format(topic_data["TopicId"])
    )

    assert topic_data == response.json()


def test_PatchTopicData():
    global topic_data

    topic_data["theme"] = "Test Topic No. 2"
    topic_data["about"] = "This is a test topic No. 2"

    response = r.patch(
        BASE_URL,
        json={
            "token": str(valid_token),
            "theme": topic_data["theme"],
            "about": topic_data["about"],
            "TopicId": topic_data["TopicId"]
        },
        headers={
            'Content-Type': 'application/json'
        }
    )

    assert response.status_code == 201


def test_DeleteTopic():
    response = r.delete(
        BASE_URL,
        json={
            "token": str(valid_token),
            "TopicId": topic_data["TopicId"]
        },
        headers={
            'Content-Type': 'application/json'
        }
    )

    assert response.status_code == 200
