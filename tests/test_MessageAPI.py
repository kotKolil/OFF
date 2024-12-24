# importing external libs
import sys
import requests

# adding some paths to venv
sys.path.append('..')

# importing local
from config import *

# generating user token
r = requests.post(
    "http://{}:{}/api/user/generate_token".format(APPhost, APPport),
    json={
        "user": AdminUser,
        "password": AdminPassword,
    },
    headers={
        'Content-Type': 'application/json'
    }
)

valid_token = r.json()["JWToken"]

sample_message_data = {
    "text": "Sample text",
}

# base API url
BASE_URL = "http://{}:{}/api/messages".format(APPhost, APPport)  # api entrypoint URI

# creating new topic
r = requests.post(
    "http://{}:{}/api/topic".format(APPhost, APPport),
    json={
        "token": valid_token,
        "theme": "theme",
        "about": "about",
        "is_protected": 0,
        "TopicId": "",
    },
    headers={
        'Content-Type': 'application/json'
    }
)

topic_data = r.json()

print(topic_data)


def test_CreateMessageViaAPI():
    global sample_message_data

    response = requests.post(
        BASE_URL,
        json={
            "token": str(valid_token),
            "TopicId": topic_data["TopicId"],
            "text": sample_message_data["text"]
        },
        headers={
            'Content-Type': 'application/json'
        }
    )

    assert response.status_code == 201
    sample_message_data = response.json()


def test_GetMessageFromTopic():
    global sample_message_data

    response = requests.get(BASE_URL + "?TopicId={}".format(sample_message_data["TopicId"]))
    assert response.json()[0] == sample_message_data


def test_GetMessageViaMessageId():
    global sample_message_data

    response = requests.get(BASE_URL + "?MessageId={}".format(sample_message_data["MessageId"]))
    print(response.json())
    assert response.json() == sample_message_data


def test_RaiseNotFoundErrorViaMessageId():
    global sample_message_data

    response = requests.get(BASE_URL + "?MessageId=MessageNotExist")
    print(response.json())
    assert response.status_code == 404


def test_EditingMessageText():
    global sample_message_data

    response = requests.patch(
        BASE_URL,
        json={
            "token": valid_token,
            "TopicId": topic_data["TopicId"],
            "text": "another sample text",
            "MsgId": sample_message_data["MessageId"]
        },
        headers={
            'Content-Type': 'application/json'
        }
    )

    assert response.status_code == 201

    sample_message_data["text"] = "another sample text"


def test_DeleteMessage():
    response = requests.delete(
        BASE_URL,
        json={
            "MessageId": sample_message_data["MessageId"],
            "token": valid_token
        }
    )

    assert response.status_code == 201
