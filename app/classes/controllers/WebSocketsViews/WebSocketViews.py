#external classes
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

            UserToken = decode_token(message["JWToken"])["sub"]
            TopicId = message["TopicId"]

            UserData = self.server_object.DBWorker.User().get(user = UserToken, format="obj")
            TopicData = self.server_object.DBWorker.Topic().get(TopicId = TopicId, format = "obj")

            if UserData.UserId == TopicData.author or UserData.IsAdmin == 1:
                self.server_object.DBWorker.Topic().delete(TopicId = TopicId)
                self.server_object.DBWorker.Message().delete(TopicId = TopicId)
                emit("TopicDelete", {"TopicId":TopicData.TopicId}, broadcast=True)


        @self.SockIO.on("MessageDelete")
        def topic_delete(message):


            decoder = j.JSONDecoder()
            message = decoder.decode(message)


            UserToken = decode_token(message["JWToken"])["sub"]
            MessageId = message["MessageId"]

            UserData = self.server_object.DBWorker.User().get(user = UserToken, format="obj")
            MsgData = self.server_object.DBWorker.Message().get(MessageId = MessageId, format = "obj")

            if UserData.UserId == MsgData.author or UserData.IsAdmin == 1:
                self.server_object.DBWorker.Message().delete(MessageId = MessageId)
                emit("MsgDel", {"MessageId":MessageId}, broadcast=True)

        @self.SockIO.on("message")
        def my_event(message):

            # try:
            decoder = j.JSONDecoder()
            message = decoder.decode(message)

            JWTData = decode_token(message["JWToken"])
            UserId = JWTData["sub"]
            TopicId = message["TopicId"]
            message = message["message"]

            UserData = self.server_object.DBWorker.User().get(user = UserId, format = "obj")
            TopicData = self.server_object.DBWorker.Topic().get(TopicId = TopicId, format = "obj")

            result = ""

            if UserData.IsBanned != 1 and UserData.IsActivated == 1 and TopicData.protected != 1:

                result = self.server_object.DBWorker.Message().create(TopicId = TopicId, author = UserId ,  text = message, format="json")

                UserData.NumOfPosts += 1
                UserData.save()

                emit('NewMessage',  result, broadcast=True)



            elif UserData.UserId == TopicData.author and TopicData.protected == 1:

                result = self.server_object.DBWorker.Message().create(TopicId = TopicId, author = UserId ,  text = message, format="json")

                UserData.NumOfPosts += 1
                UserData.save()

                emit('NewMessage',  result, broadcast=True)

            else:
                emit('NewMessage', 401, broadcast = False )


            # except Exception  as e:
            #     return emit('message', e, broadcast=False)

        @self.SockIO.on("connect")
        def OnOpenEvent():
            self.logger.info("WebSockets connection estabilished")
            emit("message", {"info":"WebSockets connection estabilished"})

        