#importing external libs
import requests as r
import sys
import os

#importing local classes
sys.path.append("...")
sys.path.append("..")
from config import *

global SampleUserData

SampleUserData = {

    "email":"noreply@domain.ru",
    "UserId":"SampleUser",
    "password":"123",
    "citate":"Sample Quote",

}



"""

in this tests we are checking API of OFF.
To run tests correctly, you need to run app before

"""

import requests

def test_TestOfCreationUser():
    # Creating example user from SampleUserData
    response = requests.post(
        url=f"http://{APPhost}:{APPport}/api/user",
        json=SampleUserData,
        headers={
            'Content-Type': 'application/json'
        }
    )

    # Assert that the response status code is 201 (Created)
    assert response.status_code == 201

    # creating sample user to raise error
    response = requests.post(
        url=f"http://{APPhost}:{APPport}/api/user",
        json=SampleUserData,
        headers={
            'Content-Type': 'application/json'
        }
    )

    # Assert that the response status code is 201 (Created)
    assert response.status_code == 400


def test_TestGetUserViaUserId():
    response = r.get(
        f"http://{APPhost}:{APPport}/api/user?UserId={SampleUserData["UserId"]}"
    )
    print(response.raw)
    assert response.json()["email"] == SampleUserData["email"]
    assert response.json()["UserId"] == SampleUserData["UserId"]

def test_TestGetUserNotFound():
    response = r.get(
        f"http://{APPhost}:{APPport}/api/user?UserId={"NotExisitingUser"}"
    )
    assert response.status_code == 404

def test_TestGetUserTokenAndUserTokenOperations():

    #creating request to API
    response = r.post(
        f"http://{APPhost}:{APPport}/api/user/generate_token",
        json = {
            "user" : SampleUserData["UserId"],
            "password":SampleUserData["password"],
        },
        headers={
            'Content-Type': 'application/json'
        }
    )

    #getting a token
    UserToken = response.json()["JWToken"]

    #checking token validness
    response = r.post(
        f"http://{APPhost}:{APPport}/api/user/CheckToken",
        json = {
            "JWToken":UserToken
        }
    )

    assert response.json() == [1]


def test_TestOfChangingUserId():
    #make request to user token API
    response = r.post(
        f"http://{APPhost}:{APPport}/api/user/generate_token",
        json = {
            "user": SampleUserData["UserId"],
            "password":SampleUserData["password"],
        },
        headers={
            'Content-Type': 'application/json'
        }
    )

    #getting a token from response body
    UserToken = response.json()["JWToken"]

    SampleUserData["UserId"] = "treska"

    response = r.post(
        f"http://{APPhost}:{APPport}/api/user/change/user",
        json = {
            "NewUserId":SampleUserData["UserId"],
            "token":UserToken,
            "citate":"",
            "password":SampleUserData["password"]
        },
        headers={
            'Content-Type': 'application/json'
        }
    )

    assert response.status_code == 201

    #checking user json in DB
    response = r.get(
        f"http://{APPhost}:{APPport}/api/user?UserId={SampleUserData["UserId"]}"
    )
    assert response.json()["UserId"] == SampleUserData["UserId"]




def test_TestChangingUserQuote():
    # make request to user token API
    response = r.post(
        f"http://{APPhost}:{APPport}/api/user/generate_token",
        json={
            "user": SampleUserData["UserId"],
            "password": SampleUserData["password"],
        },
        headers={
            'Content-Type': 'application/json'
        }
    )

    # getting a token from response body
    UserToken = response.json()["JWToken"]

    SampleUserData["quote"] = "another awesome quote"

    response = r.post(
        f"http://{APPhost}:{APPport}/api/user/change/user",
        json={
            "citate": SampleUserData["quote"],
            "token": UserToken,
        },
        headers={
            'Content-Type': 'application/json'
        }
    )

    assert response.status_code == 201

    # checking user json in DB
    response = r.get(
        f"http://{APPhost}:{APPport}/api/user?UserId={SampleUserData['UserId']}"
    )
    assert response.json()["citate"] == SampleUserData["quote"]



def test_TestAdminChangesAPI():
    # make request to user token API
    response = r.post(
        f"http://{APPhost}:{APPport}/api/user/generate_token",
        json={
            "user": AdminUser,
            "password": AdminPassword,
        },
        headers={
            'Content-Type': 'application/json'
        }
    )

    # getting a token from response body
    UserToken = response.json()["JWToken"]

    response = r.post(
        f"http://{APPhost}:{APPport}/api/user/change/admin",
        json={
            "IsBanned":1,
            "IsAdmin":1,
            "AdminToken":UserToken,
            "UserId": SampleUserData["UserId"]
        },
        headers={
            'Content-Type': 'application/json'
        }
    )

    assert response.status_code == 201

def test_TestAllMethod():

    #getting all users via API
    response = r.get(f"http://{APPhost}:{APPport}/api/user/all")
    k = 0
    for i in response.json():
        if i["UserId"] == SampleUserData["UserId"]:
            k = 1

    assert k == 1

def test_TestDeleteMethodViaUserId():

    #make request to user token API
    response = r.post(
        f"http://{APPhost}:{APPport}/api/user/generate_token",
        json = {
            "user": SampleUserData["UserId"],
            "password": SampleUserData["password"],
        },
        headers={
            'Content-Type': 'application/json'
        }
    )

    #getting a token from response body
    print(response.json())
    UserToken = response.json()["JWToken"]



    #deleting user via user API
    response = r.delete(
        f"http://{APPhost}:{APPport}/api/user",
        json={
                "JWToken":UserToken,
                "user": SampleUserData['UserId'],
        },
        headers={
            'Content-Type': 'application/json'  # Corrected the header format
        }
    )

    response.status_code = 201

def test_TestDeleteMethodViaAdmin():
    #creating example user from SampleUserData
    r.post(f"http://{APPhost}:{APPport}/api/user", json = SampleUserData)

    #make request to user token API
    response = r.post(
        f"http://{APPhost}:{APPport}/api/user/generate_token",
        json = {
            "user" : AdminUser,
            "password": AdminPassword,
        }
    )

    #getting a token from response body
    UserToken = response.json()["JWToken"]

    #deleting user via user API
    response = r.delete(
        f"http://{APPhost}:{APPport}/api/user",
        json={
                "JWToken":UserToken,
                "user": SampleUserData['UserId'],
        }
    )

    response.status_code = 201
