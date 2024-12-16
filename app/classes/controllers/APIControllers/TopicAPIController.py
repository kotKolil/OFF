import sys

sys.path.append("...")

from flask_jwt_extended import *
from flask import Blueprint, request

class TopicAPIController:
    def __init__(self, server_object):
        self.server_object = server_object
        self.bp = Blueprint('TopicAPI controller', __name__, )
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


    @route("/api/topic", methods=["GET", "POST", "DELETE", "PATCH"])
    def ApiTopic(self):
        if request.method == "GET":
            TopciId = request.args.get("TopicId")
            return self.server_object.DBWorker.Topic().get(TopicId = TopciId, format = 'json')
        elif request.method == "POST":
            RequestData = request.get_json()
            UserId = decode_token(RequestData["token"])["sub"]

            if RequestData and UserId:
                theme = RequestData["theme"]
                about = RequestData["about"]
                is_protected = RequestData["is_protected"]

                TopicCreated = self.server_object.DBWorker.Topic().create(theme, UserId, about, is_protected, format = "obj")
                return self.server_object.DBWorker.Topic().get(TopicId = TopicCreated.TopicId, format = "json")

            else:
                return 400

        elif request.method == "DELETE":
            RequestData = request.get_json()

            TopicId = RequestData["TopicId"]
            UserId = decode_token(RequestData["token"])["sub"]

            UserData = self.server_object.DBWorker.User().get(user = UserId, format = "obj")
            TopicData = self.server_object.DBWorker.Topic().get(TopicId = TopicId, format = "obj")
            if TopicData.author == UserId or UserData.IsAdmin == 1:
                self.server_object.DBWorker.Topic().delete(TopicId = TopicId)
                return "200", 200
            else:
                return "403", 403

        elif request.method == "PATCH":

            # try:

            RequestData = request.get_json()

            UserId = decode_token(RequestData["token"])["sub"]
            TopicId = RequestData["TopicId"]

            Topic = self.server_object.DBWorker.Topic().get(TopicId = TopicId, format = "obj")
            User = self.server_object.DBWorker.User().get(user = UserId, format = "obj" )
            if Topic.author == UserId or User.IsAdmin == 1:
                Topic.theme = RequestData["theme"]
                Topic.about = RequestData["about"]
                Topic.save()

                return "201", 201

    @route("/api/topic/all")
    def AllTopic(self):
        if type(self.server_object.DBWorker.Topic().all(format = "json")) != list:
            return [self.server_object.DBWorker.Topic().all(format = "json")]
        return self.server_object.DBWorker.Topic().all(format = "json")
