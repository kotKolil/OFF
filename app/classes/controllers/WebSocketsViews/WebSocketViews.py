# external classes
import sys

sys.path.append("...")

from flask_socketio import *
import json as j
from flask_jwt_extended import *


class WebSocketViews(object):

    def __init__(self, server_object):
        self.server_object = server_object
        self.SockIO = SocketIO(self.server_object.server)

        @self.SockIO.on("TopicDelete")
        def topic_delete(message):

            decoder = j.JSONDecoder()
            message = decoder.decode(message)

            user_token = decode_token(message["JWToken"])["sub"]
            topic_id = message["TopicId"]

            user_data = self.server_object.DBWorker.User().get(user=user_token, format="obj")
            topic_data = self.server_object.DBWorker.Topic().get(TopicId=topic_id, format="obj")

            if user_data.UserId == topic_data.author or user_data.IsAdmin == 1:
                self.server_object.DBWorker.Topic().delete(TopicId=topic_id)
                self.server_object.DBWorker.Message().delete(TopicId=topic_id)
                emit("TopicDelete", {"TopicId": topic_data.TopicId}, broadcast=True)

        @self.SockIO.on("MessageDelete")
        def topic_delete(message):

            decoder = j.JSONDecoder()
            message = decoder.decode(message)

            user_token = decode_token(message["JWToken"])["sub"]
            message_id = message["MessageId"]

            user_data = self.server_object.DBWorker.User().get(user=user_token, format="obj")
            msg_data = self.server_object.DBWorker.Message().get(MessageId=message_id, format="obj")

            if user_data.UserId == msg_data.author or user_data.IsAdmin == 1:
                self.server_object.DBWorker.Message().delete(MessageId=message_id)
                emit("MsgDel", {"MessageId": message_id}, broadcast=True)

        @self.SockIO.on("message")
        def my_event(message):

            # try:
            decoder = j.JSONDecoder()
            message = decoder.decode(message)

            jwt_data = decode_token(message["JWToken"])
            user_id = jwt_data["sub"]
            topic_id = message["TopicId"]
            message = message["message"]

            user_data = self.server_object.DBWorker.User().get(user=user_id, format="obj")
            topic_data = self.server_object.DBWorker.Topic().get(TopicId=topic_id, format="obj")

            if user_data.IsBanned != 1 and user_data.IsActivated == 1 and topic_data.protected != 1:

                result = self.server_object.DBWorker.Message().create(TopicId=topic_id, author=user_id, text=message,
                                                                      format="json")

                user_data.NumOfPosts += 1
                user_data.save()

                emit('NewMessage', result, broadcast=True)

            elif user_data.UserId == topic_data.author and topic_data.protected == 1:

                result = self.server_object.DBWorker.Message().create(TopicId=topic_id, author=user_id, text=message,
                                                                      format="json")

                user_data.NumOfPosts += 1
                user_data.save()

                emit('NewMessage', result, broadcast=True)

            else:
                emit('NewMessage', 401, broadcast=False)

            # except Exception  as e:
            #     return emit('message', e, broadcast=False)

        @self.SockIO.on("connect")
        def OnOpenEvent():
            self.logger.info("WebSockets connection established")
            emit("message", {"info": "WebSockets connection established"})
