import sys
sys.path.append("...")
from flask_socketio import *
from flask_jwt_extended import *
import json
from app.container import ServerContainer



server = ServerContainer.user_service()

class socketio_views(server):
    
    def __init__(self):
        super().__init__()

        @self.SockIO.on("TopicDelete")
        def topic_delete(message):

            decoder = json.JSONDecoder()
            message = decoder.decode(message)

            UserToken = decode_token(message["JWToken"])["sub"]
            TopicId = message["TopicId"]

            UserData = self.DBWorker.User().get(user = UserToken, format="obj")
            TopicData = self.DBWorker.Topic().get(TopicId = TopicId, format = "obj")

            if UserData.UserId == TopicData.author or UserData.IsAdmin == 1:
                self.DBWorker.Topic().delete(TopicId = TopicId)
                self.DBWorker.Message().delete(TopicId = TopicId)
                emit("TopicDelete", {"TopicId":TopicData.TopicId}, broadcast=True)


        @self.SockIO.on("MessageDelete")
        def topic_delete(message):


            decoder = json.JSONDecoder()
            message = decoder.decode(message)


            UserToken = decode_token(message["JWToken"])["sub"]
            MessageId = message["MessageId"]

            UserData = self.DBWorker.User().get(user = UserToken, format="obj")
            MsgData = self.DBWorker.Message().get(MessageId = MessageId, format = "obj")

            if UserData.UserId == MsgData.author or UserData.IsAdmin == 1:
                self.DBWorker.Message().delete(MessageId = MessageId)
                emit("MsgDel", {"MessageId":MessageId}, broadcast=True)

        @self.SockIO.on("message")
        def my_event(message):

            # try:
            decoder = json.JSONDecoder()
            message = decoder.decode(message)

            JWTData = decode_token(message["JWToken"])
            UserId = JWTData["sub"]
            TopicId = message["TopicId"]
            message = message["message"]

            UserData = self.DBWorker.User().get(user = UserId, format = "obj")
            TopicData = self.DBWorker.Topic().get(TopicId = TopicId, format = "obj")

            result = ""
            
            if UserData.IsBanned != 1 and UserData.IsActivated == 1 and TopicData.protected != 1:

                result = self.DBWorker.Message().create(TopicId = TopicId, author = UserId ,  text = message, format="json")

                UserData.NumOfPosts += 1
                UserData.save()

                emit('NewMessage',  result, broadcast=True)



            elif UserData.UserId == TopicData.author and TopicData.protected == 1:

                result = self.DBWorker.Message().create(TopicId = TopicId, author = UserId ,  text = message, format="json")

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
