import sys

sys.path.self.server.append("...")

from config import *
from app.classes.tools import *
from flask_jwt_extended import *
from flask import Blueprint, request
import collections

class UserAPIController():

    def __init__(self, server_object):
        self.server_object = server_object
        self.bp = Blueprint('my_controller', __name__)
        self.register_routes(self)

    def register_routes(self):
        # Loop through all methods in the class
        for method_name in dir(self):
            method = getattr(self, method_name)
            if callable(method) and hasattr(method, 'route'):
                # Register the method as a route
                self.bp.add_url_rule(method.route, view_func=method, methods=method.methods)

    @staticmethod
    def route(path, methods=['GET']):
        """Decorator to define route path and methods."""
        def decorator(func):
            func.route = path
            func.methods = methods
            return func
        return decorator



    @route("/api/user/CheckToken", methods = ["POST"])
    def CheckToken(self):
        JWToken = request.json["JWToken"]
        if decode_token(JWToken):
            return [1]
        else:
            return [0]

    @route("/api/user/generate_token", methods = ["POST"])
    def GenerateToken(self):
        if request.method == "POST":
            user = request.json["user"]
            pswd = request.json["password"]

            UserHash = generate_token(user, pswd)

            UserData = self.server_object.DBWorker.User(self).get(token = UserHash, format = "obj")
            self.server.logger.info(UserData)

            if type(UserData) != int:
                JWToken = create_access_token(identity=UserData.UserId)
                return {"JWToken":JWToken}, 201
            else:
                return "400", 400
        else:
            return "400", 400


    @route("/api/user", methods=["GET", "POST", "CREATE" ,"DELETE"])
    def MisatoKForever(self):
        if request.method == "GET":
            JWToken = request.args.get("JWToken")
            UserId = request.args.get("UserId")
            if JWToken != None:
                if decode_token(JWToken):
                    UserId = decode_token(JWToken)["sub"]
                    data = self.server_object.DBWorker.User(self).get(user = UserId, format = "json")
                    if type(data) != int:
                        return data
                    else:
                        return "404",404
                else:
                    return "400", 400
            elif UserId != None:
                data = self.server_object.DBWorker.User(self).get(user=UserId, format="json")
                if type(data) != int:
                    return data
                else:
                    return "404", 404

            else:
                return "400", 400

        elif request.method == "POST":
            RequestData = request.json

            if RequestData:

                email = RequestData["email"]
                UserId = RequestData["UserId"]
                password  = RequestData["password"]
                citate = RequestData["citate"]

                UserData = self.server_object.DBWorker.User(self).get(user = UserId, format = "ojb")
                if UserData == 0:

                    u = self.server_object.DBWorker.User(self).create(password=password, email = email, user=UserId, is_admin = 0,
                                               is_banned=0, logo_path = "default.png",citate = citate,
                                               format = "obj")
                    self.server.MailWorker.SendMessage(TargetMail = email, text = f"""Hello! Go to this link http://{self.server.host}:{self.server.app}/ActivateEmail?num={u.ActiveNum} 
                    to activate you account""", Theme = "account activating")
                    message = f"<p>Go to your email to activate your account</p>"
                    return "201", 201
                else:
                    return "400",400
            else:
                return "400", 400
        elif request.method == "DELETE":
            RequestData = request.json
            user0 = decode_token(RequestData["JWToken"])["sub"]
            user0 = self.server_object.DBWorker.User(self).get(user = user0, format = "obj")
            user = RequestData["user"]
            if user0 == user or user0.IsAdmin:
                try:
                    self.server_object.DBWorker.User(self).delete(user = user)
                    return "201", 201
                except:
                    return "404", 404
            else:
                return "403", 403

    @route("/api/user/change/user", methods = ["POST"])
    def UserChange(self):

        Data = request.json

        UserIdFromToken = decode_token(Data["token"])["sub"]
        citate = Data["citate"]

        UserData = self.server_object.DBWorker.User(self).get(user = UserIdFromToken, format = "obj")
        self.server.logger.info(UserData.__dict__)

        if UserData.UserId != "":

            #if citate is not set, we are changing password and user id
            if citate == "":

                Password = Data["password"]
                NewUserId = Data['NewUserId']

                #creating new hash from user and password
                UserData.UserId = NewUserId
                UserData.token = generate_token(NewUserId, Password)
                UserData.save(self)

                #change all topics, create by user
                AllUserTopic = self.server_object.DBWorker.Topic(self).all(format = "obj")
                if not isinstance(AllUserTopic, collections.abc.Iterable):
                    AllUserTopic.author = NewUserId
                    AllUserTopic.save(self)

                else:
                    for topic in AllUserTopic:
                        if topic.author == UserIdFromToken:
                            topic.author = NewUserId
                            topic.save(self)

                #change all messages, create by user
                AllUserMsg = self.server_object.DBWorker.Message(self).all(format = "obj")
                if not isinstance(AllUserMsg, collections.abc.Iterable):
                    AllUserTopic.author = NewUserId

                else:
                    for msg in AllUserMsg:
                        if msg.author == UserIdFromToken:
                            msg.author = NewUserId
                            msg.save(self)

                return "201", 201

            else:
                UserData.citate = citate
                UserData.save(self)
                return "201", 201

    @route("/api/user/change/admin", methods = ["POST"])
    def AdminUserChange(self):

        try:

            data = request.json

            AdminUserId = decode_token(data['AdminToken'])["sub"]
            UserId = data['UserId']
            is_banned = data["IsBanned"]
            is_admin = data["IsAdmin"]

            AdminUserData = self.server_object.DBWorker.User(self).get(user = AdminUserId, format = "obj")
            SimpleUserData = self.server_object.DBWorker.User(self).get(user = UserId, format = "obj")
            if AdminUserData.IsAdmin == 1:

                if SimpleUserData.UserId != "" and SimpleUserData.UserId != self.AdminUser:
                    SimpleUserData.IsBanned = is_banned
                    SimpleUserData.IsAdmin = is_admin
                    SimpleUserData.save(self)
                    return "201",201
                else:
                    return "404", 404

            else:
                return "403", 403

        except IndexError or KeyError:

            return "400", 400


    @route("/api/user/all")
    def UserAll(self):
        if type(self.server_object.DBWorker.User().all(format="json")) != list:
            return [self.server_object.DBWorker.User().all(format="json")]

        return self.server_object.DBWorker.User().all(format="json")