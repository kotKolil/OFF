from flask_jwt_extended import *
from flask import Blueprint, request
import copy

class TopicAPIController:
    def __init__(self, server_object):
        self.server_object = copy.copy(server_object)
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
            topic_id = request.args.get("TopicId")
            return self.server_object.DBWorker.topic().get(TopicId=topic_id, format='json')
        elif request.method == "POST":
            request_data = request.get_json()
            user_id = decode_token(request_data["token"])["sub"]

            if request_data and user_id:
                theme = request_data["theme"]
                about = request_data["about"]
                is_protected = request_data["is_protected"]

                topic_created = self.server_object.DBWorker.topic().create(theme, user_id, about, is_protected,
                                                                           format="obj")
                return self.server_object.DBWorker.topic().get(TopicId=topic_created.TopicId, format="json")

            else:
                return 400

        elif request.method == "DELETE":
            request_data = request.get_json()

            topic_id = request_data["TopicId"]
            user_id = decode_token(request_data["token"])["sub"]

            user_data = self.server_object.DBWorker.user().get(username=user_id, format="obj")
            topic_data = self.server_object.DBWorker.topic().get(TopicId=topic_id, format="obj")
            if topic_data.author == user_id or user_data.IsAdmin == 1:
                self.server_object.DBWorker.topic().delete(TopicId=topic_id)
                return "200", 200
            else:
                return "403", 403

        elif request.method == "PATCH":

            # try:

            request_data = request.get_json()

            user_id = decode_token(request_data["token"])["sub"]
            topic_id = request_data["TopicId"]

            topic = self.server_object.DBWorker.topic().get(TopicId=topic_id, format="obj")
            user = self.server_object.DBWorker.user().get(username=user_id, format="obj")
            if topic.author == user_id or user.IsAdmin == 1:
                topic.theme = request_data["theme"]
                topic.about = request_data["about"]
                topic.save()

                return "201", 201

    @route("/api/topic/all")
    def AllTopic(self):
        if type(self.server_object.DBWorker.topic().all(format="json")) != list:
            return [self.server_object.DBWorker.topic().all(format="json")]
        return self.server_object.DBWorker.topic().all(format="json")
