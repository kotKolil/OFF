#importing external libs
import requests as r
import sys
import os

#importing local classes
sys.path.append("...")
sys.path.append("..")
from config import *

SampleUserData = {

    "email":"sample@example.com",
    "UserId":"SampleUser",
    "password":"123",
    "citate":"Sample Quote",

}


"""

in this tests we are checking API of OFF.
To run tests correctly, you need to run app before

"""

import requests  # Ensure you have the requests library imported

def test_TestOfCreationUser():
    # Creating example user from SampleUserData
    response = requests.post(  # Use the requests.post method correctly
        url=f"http://{APPhost}:{APPport}/api/user",
        json=SampleUserData,
        headers={
            'Content-Type': 'application/json'  # Corrected the header format
        }
    )

    # Assert that the response status code is 201 (Created)
    assert response.status_code == 201

    # creating sample user to raise error
    response = requests.post(  # Use the requests.post method correctly
        url=f"http://{APPhost}:{APPport}/api/user",
        json=SampleUserData,
        headers={
            'Content-Type': 'application/json'  # Corrected the header format
        }
    )

    # Assert that the response status code is 201 (Created)
    assert response.status_code == 400


def test_TestGetUserViaUserId():
    response = r.get(
        f"http://{APPhost}:{APPport}/api/user?UserId={SampleUserData["UserId"]}"
    )
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
        data = {
            "user" : SampleUserData["UserId"],
            "password":SampleUserData["password"],
        }
    )

    #getting a token
    UserToken = response.json()["JWToken"]

    #checking token validness
    response = r.post(
        f"http://{APPhost}:{APPport}/api/user/CheckToken",
        data = {
            "JWToken":UserToken
        }
    )

    assert response.json() == [1]

# def test_TestOfChangingUserLogoViaAPI():
#
#     #make request to user token API
#     response = r.post(
#         f"http://{DBhost}:{DBport}/api/user/generate_token",
#         data = {
#             "user" : SampleUserData["UserId"],
#             "password":SampleUserData["password"],
#         }
#     )
#
#     #getting a token from response body
#     UserToken = response.json()["JWToken"]
#
#
#     with open(os.path.join(os.getcwd(), "classes\media", "admin.png"), "rb") as file:
#         FileData = file.read()
#         response = r.post(
#             f"http://{DBhost}:{DBport}/api/user/ChangeLogo",
#             data = {
#                 "token":UserToken,
#                 "filename":"admin.png",
#                 "file":FileData
#             }
#         )
#
# def test_TestOfChangingUserId():
#     #make request to user token API
#     response = r.post(
#         f"http://{DBhost}:{DBport}/api/user/generate_token",
#         data = {
#             "user" : SampleUserData["UserId"],
#             "password":SampleUserData["password"],
#         }
#     )
#
#     #getting a token from response body
#     UserToken = response.json()["JWToken"]
#
#     global SampleUserData
#
#     SampleUserData["UserId"] = "treska"
#
#     response = r.post(
#         f"http://{DBhost}:{DBport}/api/user/change/user",
#         data = {
#             "NewUserId":SampleUserData["UserId"],
#             "token":UserToken,
#         }
#     )
#
#     assert response.status_code == 201
#
#     #checking user data in DB
#     response = r.get(
#         f"http://{DBhost}:{DBport}/api/user?UserId={SampleUserData["UserId"]}"
#     )
#     assert response["UserId"] == SampleUserData["UserId"]
#
# def test_TestChangingUserQuote():
#     # make request to user token API
#     response = r.post(
#         f"http://{DBhost}:{DBport}/api/user/generate_token",
#         data={
#             "user": SampleUserData["UserId"],
#             "password": SampleUserData["password"],
#         }
#     )
#
#     # getting a token from response body
#     UserToken = response.json()["JWToken"]
#
#     global SampleUserData
#
#     SampleUserData["quote"] = "another awesome quote"
#
#     response = r.post(
#         f"http://{DBhost}:{DBport}/api/user/change/user",
#         data={
#             "citate":SampleUserData["quote"],
#             "token": UserToken,
#         }
#     )
#
#     assert response.status_code == 201
#
#     # checking user data in DB
#     response = r.get(
#         f"http://{DBhost}:{DBport}/api/user?UserId={SampleUserData["UserId"]}"
#     )
#     assert response["citate"] == SampleUserData["quote"]
#
# def test_TestAdminChangesAPI():
#     # make request to user token API
#     response = r.post(
#         f"http://{DBhost}:{DBport}/api/user/generate_token",
#         data={
#             "user": AdminUser,
#             "password": AdminPassword,
#         }
#     )
#
#     # getting a token from response body
#     UserToken = response.json()["JWToken"]
#
#     response = r.post(
#         f"http://{DBhost}:{DBport}/api/user/change/admin",
#         data={
#             "IsBanned":1,
#             "IsAdmin":1
#         }
#     )
#
#     assert response.status_code == 201
#
# def test_TestAllMethod():
#
#     #getting all users via API
#     response = r.get("/api/user/all")
#     k = 0
#     for i in response.json():
#         if i["UserId"] == SampleUserData["UserId"]:
#             k = 1
#
#     assert k == 1
#
def test_TestDeleteMethodViaUserId():

    #make request to user token API
    response = r.post(
        f"http://{APPhost}:{APPport}/api/user/generate_token",
        data = {
            "user" : SampleUserData["UserId"],
            "password":SampleUserData["password"],
        }
    )

    #getting a token from response body
    UserToken = response.json()["JWToken"]

    #deleting user via user API
    response = r.delete(
        f"http://{DBhost}:{DBport}/api/user",
        json={
                "JWToken":UserToken,
                "user": SampleUserData['UserId'],
        },
        headers={
            'Content-Type': 'application/json'  # Corrected the header format
        }
    )

    response.status_code = 201
#
#
# def test_TestDeleteMethodViaAdmin():
#     #creating example user from SampleUserData
#     r.create(f"http://{DBhost}:{DBport}/api/user", data = SampleUserData)
#
#     #make request to user token API
#     response = r.post(
#         f"http://{DBhost}:{DBport}/api/user/generate_token",
#         data = {
#             "user" : AdminUser,
#             "password": AdminPassword,
#         }
#     )
#
#     #getting a token from response body
#     UserToken = response.json()["JWToken"]
#
#     #deleting user via user API
#     response = r.delete(
#         f"http://{DBhost}:{DBport}/api/user",
#         data={
#                 "JWToken":UserToken,
#                 "user": SampleUserData['UserId'],
#         }
#     )
#
#     response.status_code = 201