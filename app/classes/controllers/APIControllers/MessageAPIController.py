import sys

sys.path.append("...")

from flask_jwt_extended import *
from flask import Blueprint, request

class MessageAPIController:

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

    @route("/api/messages", methods = ["GET", "POST", "DELETE", "PATCH"])
    def ApiMessage(self):
        if request.method == "GET":
            TopicId = request.args.get("TopicId")
            MessageId = request.args.get("MessageId")
            self.logger.DBWorker.info(TopicId)
            self.logger.DBWorker.info(MessageId)
            if TopicId != None:
                if type(self.server_object.DBWorker.Message().get(TopicId = TopicId, format = 'json')) != list:
                    return [self.server_object.DBWorker.Message().get(TopicId = TopicId, format = 'json')]
                return self.server_object.DBWorker.Message().get(TopicId=TopicId, format='json')
            elif MessageId != None:
                MessageData = self.server_object.DBWorker.Message().get(MessageId = MessageId, format = "json")
                if MessageData != []:
                    return MessageData, 200
                return '404', 404

        elif request.method == "POST":
            RequestData = request.get_json()
            self.self.logger.DBWorker.info(text = RequestData)
            UserId = decode_token(RequestData["token"])["sub"]
            TopicData = self.server_object.DBWorker.Topic().get(TopicId = RequestData["TopicId"], format = "obj")
            if TopicData == []:
                return "404", 404
            if RequestData and UserId and TopicData.protected != 1:
                TopicId = RequestData["TopicId"]
                text = RequestData["text"]
                NewMessage = self.server_object.DBWorker.Message().create(TopicId, UserId, text, format = "json")
                return NewMessage, 201
            elif TopicData.author == UserId and TopicData.protected == 1:
                TopicId = RequestData["TopicId"]
                text = RequestData["text"]
                NewMessage = self.server_object.DBWorker.Message().create(TopicId, UserId, text, format = "json")
                return NewMessage, 201
            else:
                return "403",403
        elif request.method == "DELETE":
            RequestData = request.get_json()

            MessageId = RequestData["MessageId"]
            UserId = decode_token(RequestData["token"])["sub"]

            UserData = self.server_object.DBWorker.User().get(user=UserId, format='obj')
            MsgData = self.server_object.DBWorker.Message().get(MessageId=MessageId, format='obj')
            if MsgData.author == UserId or UserData.IsAdmin == 1:
                self.server_object.DBWorker.Message().delete(MessageId = MessageId)
                return "200", 201
            else:
                return "403", 403

        elif request.method == "PATCH":

            RequestData = request.get_json()

            text = RequestData['text']
            MsgId = RequestData["MsgId"]
            UserId = decode_token(RequestData["token"])["sub"]

            MsgData = self.server_object.DBWorker.Message().get(MessageId = MsgId, format = "obj")

            if UserId == MsgData.author or UserId == self.server_object.AdminUser:

                MsgData.text = text
                MsgData.save()

                return "201", 201

            return "403", 403

    @route("/api/messages/all")
    def MessageAll(self):
        return self.server_object.DBWorker.Message().all(format="json")
