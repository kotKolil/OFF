# external classes
import random
import sys

sys.path.append("...")

from flask_socketio import *
import json as j
from config import *
from flask_jwt_extended import *
import copy
import base64

class WebSocketViews(object):

    def __init__(self, server_object):
        self.server_object = copy.copy(server_object)
        self.SockIO = SocketIO(self.server_object.server)

        @self.SockIO.on("TopicDelete")
        def topic_delete(message):

            decoder = j.JSONDecoder()
            message = decoder.decode(message)

            user_token = decode_token(message["JWToken"])["sub"]
            topic_id = message["TopicId"]

            user_data = self.server_object.DBWorker.user().get(username=user_token, format="obj")
            topic_data = self.server_object.DBWorker.topic().get(TopicId=topic_id, format="obj")

            if user_data.UserId == topic_data.author or user_data.IsAdmin == 1:
                self.server_object.DBWorker.topic().delete(TopicId=topic_id)
                self.server_object.DBWorker.message().delete(TopicId=topic_id)
                emit("TopicDelete", {"TopicId": topic_data.TopicId}, broadcast=True)

        @self.SockIO.on("MessageDelete")
        def topic_delete(message):

            decoder = j.JSONDecoder()
            message = decoder.decode(message)

            user_token = decode_token(message["JWToken"])["sub"]
            message_id = message["MessageId"]

            user_data = self.server_object.DBWorker.user().get(username=user_token, format="obj")
            msg_data = self.server_object.DBWorker.message().get(MessageId=message_id, format="obj")

            if user_data.UserId == msg_data.author or user_data.IsAdmin == 1:
                self.server_object.DBWorker.message().delete(MessageId=message_id)
                emit("MsgDel", {"MessageId": message_id}, broadcast=True)

        @self.SockIO.on("message")
        def my_event(message):

            # try:
            decoder = j.JSONDecoder()
            message = decoder.decode(message)

            jwt_data = decode_token(message["JWToken"])
            user_id = jwt_data["sub"]
            topic_id = message["TopicId"]
            image = message["ImgData"]
            print(image)
            message = message["message"]

            user_data = self.server_object.DBWorker.user().get(username=user_id, format="obj")
            topic_data = self.server_object.DBWorker.topic().get(TopicId=topic_id, format="obj")

            if user_data.IsBanned != 1 and user_data.IsActivated == 1 and topic_data.protected != 1:

                #saving image
                if image:
                    bin_img = base64.b64decode( image.split(",", 1)[1] )
                    img_type = image.split("/")[1].split(";")[0]
                    img_name = f"{random.randint(1, 10**6)}.{img_type}"
                    with open(os.path.join(os.getcwd(), MEDIA_PREFIX, img_name), "wb") as file:
                        file.write(bin_img)
                else:
                    img_name = ""
                print(img_name)

                result = self.server_object.DBWorker.message().create(TopicId=topic_id, author=user_id, text=message,
                                                                      img = img_name, format="json")

                user_data.NumOfPosts += 1
                user_data.save()

                emit('NewMessage', result, broadcast=True)

            elif user_data.UserId == topic_data.author and topic_data.protected == 1:

                result = self.server_object.DBWorker.message().create(TopicId=topic_id, author=user_id, text=message,
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
            emit("message", {"info": "WebSockets connection established"})
