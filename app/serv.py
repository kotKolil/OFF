# external classes
import sys

sys.path.append("..")
from flask_socketio import *
import json as j
# local classes
from app.classes.ApplicationPart.loggers import *
# importing API controllers
from app.classes.controllers.APIControllers.MessageAPIController import *
from app.classes.controllers.APIControllers.TopicAPIController import *
from app.classes.controllers.APIControllers.UserAPIController import *
from app.classes.controllers.WebSocketsViews.WebSocketViews import *
# importing HTML controllers
from app.classes.controllers.HTMLControllers.HTMLController import *


class server:

    def __init__(self, ClassLoger, DBWorker, port=8000, IsDebug=True, host="127.0.0.1", AdminUser="", AdminName="",
                 AdminPassword="",
                 AdminCitate="admin always right", AdminLogoPath="/media/admin.png", ForumName="Forum",
                 MailWorker: object = "", AppSecretKey="", JwtSecretKey="", logger=Logger()):
        # settings of server's behavior

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
        self.server.config['UPLOAD_FOLDER'] = MEDIA_PREFIX
        self.server.config['SECRET_KEY'] = AppSecretKey
        self.server.config['JWT_SECRET_KEY'] = JwtSecretKey
        self.server.config["template_folder"] = TEMPLATE_PREFIX

        message_api_controller = MessageAPIController(server_object=self)
        topic_api_controller = TopicAPIController(server_object=self)
        user_api_controller = UserAPIController(server_object=self)
        self.web_socket_controller = WebSocketViews(server_object=self)

        self.server.register_blueprint(message_api_controller.bp)
        self.server.register_blueprint(topic_api_controller.bp)
        self.server.register_blueprint(user_api_controller.bp)

        self.html_controller = HTMLController(server_object=self)

        self.server.register_blueprint(self.html_controller.bp)

        # creating Admin account
        try:
            admin_akk = DBWorker.user().create(AdminPassword, "", AdminUser, 1, 0, "admin.png", AdminCitate,
                                               format="obj")
            admin_akk.IsActivated = 1
            admin_akk.save()

        except sqlite3.IntegrityError:
            self.logger.warning("Admin User Already Exists")

        @self.server.errorhandler(404)
        def Handler404(e):
            return render("info.html", message=e, code=404)

        # in this place we are registering error handlers
        self.server.register_error_handler(404, Handler404)

    @staticmethod
    def render(template_name, **context):
        return render_template(template_name, **context)

    def run(self):
        self.web_socket_controller.SockIO.run(self.server, host=self.host, port=self.port,
                                              debug=self.IsDebug, allow_unsafe_werkzeug=True)
