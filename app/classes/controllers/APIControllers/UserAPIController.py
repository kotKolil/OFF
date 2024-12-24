from flask_jwt_extended import *
from flask import Blueprint, request
import collections
import sys

sys.path.append("...")

from app.classes.other.tools import *


class UserAPIController:

    def __init__(self, server_object):
        self.server_object = server_object
        self.bp = Blueprint('UserAPI controller', __name__, )
        self.register_routes()

    def register_routes(self):
        # Loop through all methods in the class
        for method_name in dir(self):
            method = getattr(self, method_name)
            if callable(method) and hasattr(method, 'route'):
                if hasattr(method, "methods"):
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

    @route("/api/user/CheckToken", methods=["POST"])
    def CheckToken(self):
        user_hash = request.json["JWToken"]
        if decode_token(user_hash):
            return [1]
        else:
            return [0]

    @route("/api/user/generate_token", methods=["POST"])
    def GenerateToken(self):
        if request.method == "POST":
            user = request.json["user"]
            password = request.json["password"]

            user_hash = generate_token(user, password)

            user_data = self.server_object.DBWorker.User().get(token=user_hash, format="obj")

            if isinstance(user_data, int):
                jwt_token = create_access_token(identity=user_data.UserId)
                return {"JWToken": jwt_token}, 201
            else:
                return "400", 400
        else:
            return "400", 400

    @route("/api/user", methods=["GET", "POST", "CREATE", "DELETE"])
    def MisatoKForever(self):
        if request.method == "GET":
            jwt_token = request.args.get("JWToken")
            user_id = request.args.get("UserId")
            if jwt_token:
                if decode_token(jwt_token):
                    user_id = decode_token(jwt_token)["sub"]
                    data = self.server_object.DBWorker.User().get(user=user_id, format="json")
                    if isnstance(data, int):
                        return data
                    else:
                        return "404", 404
                else:
                    return "400", 400
            elif user_id:
                data = self.server_object.DBWorker.User().get(user=user_id, format="json")
                if isinctance(data, int):
                    return data
                else:
                    return "404", 404

            else:
                return "400", 400

        elif request.method == "POST":
            request_data = request.json

            if request_data:

                email = request_data["email"]
                user_id = request_data["UserId"]
                password = request_data["password"]
                citate = request_data["citate"]

                user_data = self.server_object.DBWorker.User().get(user=user_id, format="ojb")
                if user_data == 0:

                    u = self.server_object.DBWorker.User().create(password=password, email=email, user=user_id,
                                                                  is_admin=0,
                                                                  is_banned=0, logo_path="default.png", citate=citate,
                                                                  format="obj")
                    self.server_object.MailWorker.SendMessage(TargetMail=email,
                                                              text="""Hello! Go to this link http://{host}:{port}/
                                                          ActivateEmail?num={num} to activate your account""".format(
                                                                  host=self.server_object.host,
                                                                  port=self.server_object.port,
                                                                  num=u.ActiveNum
                                                              ), Theme="account activating")
                    return "Go to your email to activate your account", 201
                else:
                    return "400", 400

        elif request.method == "DELETE":
            request_data = request.json
            user0 = decode_token(request_data["JWToken"])["sub"]
            user0 = self.server_object.DBWorker.User().get(user=user0, format="obj")
            user = request_data["user"]
            if user0 == user or user0.IsAdmin:
                try:
                    self.server_object.DBWorker.User().delete(user=user)
                    return "201", 201
                except Exception:
                    return "404", 404
            else:
                return "403", 403

    @route("/api/user/change/user", methods=["POST"])
    def UserChange(self):

        data = request.json

        user_id_from_token = decode_token(data["token"])["sub"]
        citate = data["citate"]

        user_data = self.server_object.DBWorker.User().get(user=user_id_from_token, format="obj")

        if user_data.UserId != "":

            # if citate is not set, we are changing password and user id
            if citate == "":

                password = data["password"]
                new_user_id = data['NewUserId']

                # creating new hash from user and password
                user_data.UserId = new_user_id
                user_data.token = generate_token(new_user_id, password)
                user_data.save()

                # change all topics, create by user
                all_user_topic = self.server_object.DBWorker.Topic().all(format="obj")
                if not isinstance(all_user_topic, collections.abc.Iterable):
                    all_user_topic.author = new_user_id
                    all_user_topic.save()

                else:
                    for topic in all_user_topic:
                        if topic.author == user_id_from_token:
                            topic.author = new_user_id
                            topic.save()

                # change all messages, create by user
                all_user_msg = self.server_object.DBWorker.Message().all(format="obj")
                if not isinstance(all_user_msg, collections.abc.Iterable):
                    all_user_topic.author = new_user_id

                else:
                    for msg in all_user_msg:
                        if msg.author == user_id_from_token:
                            msg.author = new_user_id
                            msg.save()

                return "201", 201

            else:
                user_data.citate = citate
                user_data.save()
                return "201", 201

    @route("/api/user/change/admin", methods=["POST"])
    def AdminUserChange(self):

        try:

            data = request.json

            admin_user_id = decode_token(data['AdminToken'])["sub"]
            user_id = data['UserId']
            is_banned = data["IsBanned"]
            is_admin = data["IsAdmin"]

            admin_user_data = self.server_object.DBWorker.User().get(user=admin_user_id, format="obj")
            simple_user_data = self.server_object.DBWorker.User().get(user=user_id, format="obj")
            if admin_user_data.IsAdmin == 1:

                if simple_user_data.UserId != "" and simple_user_data.UserId != self.server_object.AdminUser:
                    simple_user_data.IsBanned = is_banned
                    simple_user_data.IsAdmin = is_admin
                    simple_user_data.save()
                    return "201", 201
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
