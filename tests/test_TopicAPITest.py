#importing external libs
import requests as r
import sys
import os

#importing local classes
sys.path.append("...")
sys.path.append("..")
from config import *
import requests
import pytest

BASE_URL = f"http://{APPhost}:{APPport}/api/topic"  #api entripoint URI

#generating user token
r = requests.post(
    f"http://{APPhost}:{APPport}/api/user/generate_token",
    json = {
    "user" : AdminUser,
    "password":AdminPassword,
    },
    headers={
    'Content-Type': 'application/json'
    }
)

valid_token = r.json()["JWToken"]

topic_data = {
        "theme": "Test Topic",
        "about": "This is a test topic.",
        "is_protected":"0"
    }


#creating topic
def test_TopicCreation():
    global topic_data

    r = requests.post(
        BASE_URL,
        json = {
             "token":str(valid_token),
            "theme":topic_data["theme"],
            "about":topic_data["about"],
            "is_protected": topic_data["is_protected"]
        },
        headers={
            'Content-Type': 'application/json'
        }
    )

    topic_data = r.json()
    assert r.status_code == 200

def test_TopicGet():
    r = requests.get(
        BASE_URL + f"?TopicId={topic_data["TopicId"]}"
    )

    assert topic_data == r.json()

def test_PatchTopicData():

    global topic_data

    topic_data["theme"] = "Test Topic No. 2"
    topic_data["about"] = "This is a test topic No. 2"

    r = requests.patch(
        BASE_URL,
        json = {
             "token":str(valid_token),
            "theme":topic_data["theme"],
            "about":topic_data["about"],
            "TopicId":topic_data["TopicId"]
        },
        headers={
            'Content-Type': 'application/json'
        }
    )

    assert r.status_code == 201


def test_DeleteTopic():

    r = requests.delete(
    BASE_URL,
    json = {
         "token":str(valid_token),
        "TopicId": topic_data["TopicId"]
    },
    headers={
        'Content-Type': 'application/json'
    }
    )

    assert r.status_code == 200