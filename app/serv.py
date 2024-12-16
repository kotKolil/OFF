#external classes
import sys
sys.path.append("..")
from flask_socketio import *
# local classes
from app.classes.ApplicationPart.loggers import *
#importing API controllers
from app.classes.controllers.APIControllers.MessageAPIController import *
from app.classes.controllers.APIControllers.TopicAPIController import *
from app.classes.controllers.APIControllers.UserAPIController import *
#imporing HTML controllers
from app.classes.controllers.HTMLControllers.HTMLController import *

class server:

    def __init__(self,  ClassLoger, DBWorker, port=8000, IsDebug=True, host="127.0.0.1", AdminUser = "", AdminName = "", AdminPassword = "",
                 AdminCitate = "admin always right",AdminLogoPath = "/media/admin.png", ForumName = "Forum", MailWorker:object = "", AppSecretKey = "", JwtSecretKey = "", logger = Logger()):
        #settings of server's behavior

        self.host = host
        self.port = port
        self.IsDebug = IsDebug
        self.server = Flask(__name__)
        self.jwt = JWTManager(self.server)
        self.server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        self.server.config['SECRET_KEY'] = AppSecretKey
        self.server.config['JWT_SECRET_KEY'] = JwtSecretKey
        self.ClassLogger = ClassLoger
        self.AdminName = AdminName
        self.AdminUser = AdminUser
        self.AdminPassword = AdminPassword
        self.AdminCitate = AdminCitate
        self.AdminToken = generate_token(self.AdminPassword, self.AdminUser)
        self.AdminLogoPath = AdminLogoPath
        self.ForumName = ForumName
        self.MailWorker = MailWorker
        self.DBWorker = DBWorker
        self.logger = logger
        self.SockIO = SocketIO(self.server)
        self.server.config['UPLOAD_FOLDER'] = MEDIA_PREFIX
        self.server.config['SECRET_KEY'] = AppSecretKey
        self.server.config['JWT_SECRET_KEY'] = JwtSecretKey
        self.server.config["template_folder"] = TEMPLATE_PREFIX

        message_api_controller = MessageAPIController(server_object=self)
        topic_api_controller = TopicAPIController(server_object=self)
        user_api_controller = UserAPIController(server_object=self)

        self.server.register_blueprint(message_api_controller.bp)
        self.server.register_blueprint(topic_api_controller.bp)
        self.server.register_blueprint(user_api_controller.bp)

        html_controller = HTMLController(server_object=self)

        self.server.register_blueprint(html_controller.bp)

        #creating Admin Acount
        try:
            AdminAkk = DBWorker.User().create(AdminPassword, "", AdminUser, 1,0,"admin.png",AdminCitate, format = "obj")
            AdminAkk.IsActivated = 1
            AdminAkk.save()

        except sqlite3.IntegrityError:
                self.logger.warning("Admin User Already Exists")

        @self.server.errorhandler(404)
        def Handler404(e):
            return render("info.html", message="HTTP 404.Page Not Found", code = 404)

        #in this place we are registring error handlers
        self.server.register_error_handler(404, Handler404)

        @self.SockIO.on("TopicDelete")
        def topic_delete(message):

            decoder = json.JSONDecoder()
            message = decoder.decode(message)

            UserToken = decode_token(message["JWToken"])["sub"]
            TopicId = message["TopicId"]

            UserData = DBWorker.User().get(user = UserToken, format="obj")
            TopicData = DBWorker.Topic().get(TopicId = TopicId, format = "obj")

            if UserData.UserId == TopicData.author or UserData.IsAdmin == 1:
                DBWorker.Topic().delete(TopicId = TopicId)
                DBWorker.Message().delete(TopicId = TopicId)
                emit("TopicDelete", {"TopicId":TopicData.TopicId}, broadcast=True)


        @self.SockIO.on("MessageDelete")
        def topic_delete(message):


            decoder = json.JSONDecoder()
            message = decoder.decode(message)


            UserToken = decode_token(message["JWToken"])["sub"]
            MessageId = message["MessageId"]

            UserData = DBWorker.User().get(user = UserToken, format="obj")
            MsgData = DBWorker.Message().get(MessageId = MessageId, format = "obj")

            if UserData.UserId == MsgData.author or UserData.IsAdmin == 1:
                DBWorker.Message().delete(MessageId = MessageId)
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

            UserData = DBWorker.User().get(user = UserId, format = "obj")
            TopicData = DBWorker.Topic().get(TopicId = TopicId, format = "obj")

            result = ""

            if UserData.IsBanned != 1 and UserData.IsActivated == 1 and TopicData.protected != 1:

                result = DBWorker.Message().create(TopicId = TopicId, author = UserId ,  text = message, format="json")

                UserData.NumOfPosts += 1
                UserData.save()

                emit('NewMessage',  result, broadcast=True)



            elif UserData.UserId == TopicData.author and TopicData.protected == 1:

                result = DBWorker.Message().create(TopicId = TopicId, author = UserId ,  text = message, format="json")

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


    def render(self, template_name, **context):
            return render_template(template_name, **context)

    def run(self):
        self.SockIO.run(self.server, host=self.host, port=self.port, debug=self.IsDebug)