from flask_jwt_extended import *
from flask import Blueprint, request


class MessageAPIController:

    def __init__(self, server_object):

        self.server_object = server_object
        self.bp = Blueprint('my_controller', __name__)
        self.register_routes()

    def register_routes(self):
        # Loop through all methods in the class
        for method_name in dir(self):
            method = getattr(self, method_name)
            if callable(method) and hasattr(method, 'route'):
                # Register the method as a route
                if hasattr(method, 'methods'):
                    self.bp.add_url_rule(method.route, view_func=method, methods=method.methods)

    @staticmethod
    def route(path, methods=['GET']):
        """Decorator to define route path and methods."""

        def decorator(func):
            func.route = path
            func.methods = methods
            return func

        return decorator

    @route("/api/messages", methods=["GET", "POST", "DELETE", "PATCH"])
    def ApiMessage(self):
        if request.method == "GET":
            topic_id = request.args.get("TopicId")
            message_id = request.args.get("MessageId")
            if topic_id:
                if type(self.server_object.DBWorker.Message().get(TopicId=topic_id, format='json')) != list:
                    return [self.server_object.DBWorker.Message().get(TopicId=topic_id, format='json')]
                return self.server_object.DBWorker.Message().get(TopicId=topic_id, format='json')
            elif message_id:
                message_data = self.server_object.DBWorker.Message().get(MessageId=message_id, format="json")
                if message_data:
                    return message_data, 200
                return '404', 404

        elif request.method == "POST":
            request_data = request.get_json()
            user_id = decode_token(request_data["token"])["sub"]
            topic_data = self.server_object.DBWorker.Topic().get(TopicId=request_data["TopicId"], format="obj")
            if not topic_data:
                return "404", 404
            if request_data and user_id and topic_data.protected != 1:
                topic_id = request_data["TopicId"]
                text = request_data["text"]
                new_message = self.server_object.DBWorker.Message().create(topic_id, user_id, text, format="json")
                return new_message, 201
            elif topic_data.author == user_id and topic_data.protected == 1:
                topic_id = request_data["TopicId"]
                text = request_data["text"]
                new_message = self.server_object.DBWorker.Message().create(topic_id, user_id, text, format="json")
                return new_message, 201
            else:
                return "403", 403
        elif request.method == "DELETE":
            request_data = request.get_json()

            message_id = request_data["MessageId"]
            user_id = decode_token(request_data["token"])["sub"]

            user_data = self.server_object.DBWorker.User().get(user=user_id, format='obj')
            msg_data = self.server_object.DBWorker.Message().get(MessageId=message_id, format='obj')
            if msg_data.author == user_id or user_data.IsAdmin == 1:
                self.server_object.DBWorker.Message().delete(MessageId=message_id)
                return "200", 201
            else:
                return "403", 403

        elif request.method == "PATCH":

            request_data = request.get_json()

            text = request_data['text']
            msg_id = request_data["MsgId"]
            user_id = decode_token(request_data["token"])["sub"]

            msg_data = self.server_object.DBWorker.Message().get(MessageId=msg_id, format="obj")

            if user_id == msg_data.author or user_id == self.server_object.AdminUser:
                msg_data.text = text
                msg_data.save()

                return "201", 201

            return "403", 403

    @route("/api/messages/all")
    def MessageAll(self):
        return self.server_object.DBWorker.Message().all(format="json")
