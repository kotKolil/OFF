#external classes
from msilib.schema import SelfReg
from typing import Self
from flask import *
from flask import render_template as render
from werkzeug.utils import secure_filename
from werkzeug.exceptions import *
from pathlib import *
import os
from pathlib import *
from os import *
from flask import jsonify
from flask_sock import *
from time import *
from flask_socketio import *
import sqlite3
from flask import Flask, jsonify, request
from flask_jwt_extended import *

# local classes
from .loggers import *
from .tools import *


class server:

    def __init__(self,  ClassLoger, DBWorker, port=8000, IsDebug=True, host="127.0.0.1", AdminUser = "", AdminName = "", AdminPassword = "", 
                 AdminCitate = "admin always right",AdminLogoPath = "/media/admin.png", ForumName = "Forum", MailWorker = "", AppSecretKey = "", JwtSecretKey = ""):
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
        # self.MailWorker = MailWorker

        SockIO = SocketIO(self.server)

        try:
            DBWorker.User().create(self.AdminPassword,"",self.AdminUser,1,0,self.AdminLogoPath,AdminCitate)
            ClassLoger.log_message("Admin user created")
        except Exception as e:
            ClassLoger.log_message(f"Admin user created; There are error ocurred:{e}")

        @SockIO.on("message")
        def my_event(message):

            JWTData = decode_token(message["JWToken"])
            UserId = JWTData["identity"]
            ThreadId = message["ThreadId"]
            Message = message["Message"]
            DBWorker.Message().create(ThreadId, UserId  , Message, get_current_time())
            UserData = DBWorker.User().get(user = UserId, format="json")

            emit("message", {"UserData":UserData, "MessageData":{"text":Message, "TopicId":ThreadId}}, broadcast=True)

        @SockIO.on("connect")
        def OnOpenEvent():
            print("WebSockets connection estabilished")
            emit("message", {"info":"WebSockets connection estabilished"})

        #views, wich handle errors
        @self.server.errorhandler(404)
        def Handler404(e):
            return render("info_html", message="HTTP 404<p>Page Not Found")
            



        #in this place we are registring error handlers
        self.server.register_error_handler(404, Handler404)



        #serving static files
        @self.server.route("/static/<path:path>")
        def static_files(path):
            return send_from_directory('static', path)
        
        #serving media files
        @self.server.route("/media/<path:path>")
        def media_files(path):
            return send_from_directory('media', path)
        
        #index page
        @self.server.route('/')
        def index():
            return render("index.html")     

        #topic page
        @self.server.route('/topic')
        def index():
            return render("topic.html")

        #auth methods
        # structure of table user: password, user_id, is_admin, is_banned, logo_path, citate, time_of_join, token
        @self.server.route('/auth/reg', methods=["GET", "POST"])
        def reg():
            if request.method == "GET":
                # return page of registration
                tok = request.cookies.get('token')
                JWTData = decode_token(tok)
                if JWTData:
                    return redirect("/")
                else:
                    return render_template("reg.html")
            elif request.method == "POST":

                # getting data from POST request
                login = request.form.get("login")
                email = request.form.get("email")
                password = request.form.get("password")
                citate = request.form.get("citate")
                file = request.files.get('logo')

                if file.filename == '': 
                    return redirect(request.url)
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(os.getcwd(), "classes\media", file.filename))
                    try:
                        u = DBWorker.User().create(password=password, email = email, user=login, is_admin = 0, is_banned=0, logo_path = filename,citate = citate)
                        MailWorker(f"Hello! Go to this link http://{host}/ActivateEmail?num={u.ActiveNum}")
                        resp = render("info.html", message = f"<p>Go to your email to activate your account</p>")
                        
                        JWToken = create_access_token(identity=u.UserId)

                        resp.set_cookie("token", JWToken)
                        return resp
                    except sqlite3.IntegrityError:
                        return render_template("reg.html", message="Username already used")
  
                else:
                    return "400 Bad Request"


        #log method
        @self.server.route("/auth/log", methods=["GET", "POST"])
        def log():
            if request.method == "GET":
                tok = request.cookies.get('token')
                JWTData = decode_token(tok)
                if JWTData:
                    return redirect("/")
            elif request.method == "POST":

                    login = request.form.get("login")
                    password = request.form.get("password")
                    u = DBWorker.User().get(login, password)
                    resp = redirect("/")
                    JWToken = create_access_token(identity=u.UserId)
                    resp.set_cookie("token", JWToken)
                    return resp

            

        #logging out
        @self.server.route("/auth/dislog", methods=["GET"])
        def dislog():
            resp = redirect("/")
            resp.set_cookie("token", "Null")
            return resp
        
        @self.server.route("api/user/ChangeLogo")
        def ChangeLogo():
            if request.method == "POST":
                UserId = get_jwt_identity(request.json()["token"])
                file = request.files.get('logo')
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(os.getcwd(), "classes\media", file.filename))
                    DBWorker.User().get(user = UserId).LogoPath = file.filename
                    return os.path.join(os.getcwd(), "classes\media", file.filename), 201
                return "Bad Request", 400

        @self.server.route("/api/user")
        def user():
            if request.method == "GET":
                JWToken = request.args.get("JWToken")
                if decode_token(JWToken):
                    UserId = get_jwt_identity(JWToken)
                    return DBWorker.User().get(user = UserId, format = "json")
                else:
                    return 401
            elif request.method == "CREATE":
                RequestData = request.get_json()
                
                if RequestData:
                    
                    email = RequestData["email"]
                    UserId = RequestData["UserId"]
                    password  = RequestData["password"]
                    citate = RequestData["citate"]

                    try:
                        DBWorker.User().create(password, email, UserId, 0, 0, "", citate)
                        MailWorker(f"Hello! Go to this link http://{host}/ActivateEmail?num={u.ActiveNum} to activate you account")
                        message = f"<p>Go to your email to activate your account</p>"
                        return message, 201
                    except:
                        return "bad user or password", 400
                else:
                    return 400, "Bad Request"
                
            elif request.method == "DELETE":
                WToken = request.args.get("JWToken")
                if decode_token(JWToken):
                    try:
                        DBWorker.User().delete(user = get_jwt_identity(JWToken))
                        return 200
                    except:
                        return 400
                else:
                    return 401
    
        

        @self.server.route("/api/user/CheckToken", methods = ["POST"])
        def CheckToken():
            JWToken = request.get_json()["JWToken"]
            if decode_token(JWToken):
                return [1]
            else:
                return [0]
            
        @self.server.route("/ActivateEmail")
        def ActivateEmail():
            num = request.args.get('num')

            UserData = DBWorker.User().get(num=num)
            UserData.IsActivated = 1
            UserData.save()

            return render("info.html", message="Account is activated")

        @self.server.route("/api/user/all")
        def UserAll():
            return DBWorker.User().all(format="json")
        
        
        @self.server.route("api/topic")
        def ApiTopic():
            if request.method == "GET":
                TopciId = request.args.get("TopicId")
                return DBWorker.Topic().get(TopciId = TopciId, format = 'json')
            elif request.method == "POST":
                RequestData = request.get_json()
                UserId = get_jwt_identity(RequestData["token"])

                if RequestData and UserId:
                    theme = RequestData["theme"]
                    about = RequestData["about"]

                    TopicCreated = DBWorker.Topic().create(theme, UserId, about)

                    return DBWorker.Topic().get(TopciId = TopicCreated.TopicId, format = "json")

                else:
                    return 400
                
            elif request.method == "DELETE":
                RequestData = request.get_json()

                TopicId = RequestData["TopicId"]
                UserId = get_jwt_identity(RequestData["token"])

                UserData = DBWorker.User().get(user = UserId)
                TopicData = DBWorker.Topic().get(TopicId = TopicId)
                if TopicData.auhor == UserId or UserData.IsAdmin:
                    DBWorker.Message().delete(TopciId = TopicId)
                    return 200
                else:
                    return "Denied", 403
            
        @self.server.route("/api/topic/all")
        def AllTopic():
            return DBWorker.Topic().all(format = "json")
        

        @self.server.route("/api/messages")
        def ApiMessage():
            if request.method == "GET":
                MessageId = request.args.get("MessageId")
                return DBWorker.Topic().get(MessageId = MessageId, format = 'json')
            elif request.method == "POST":
                RequestData = request.get_json()
                UserId = get_jwt_identity(RequestData["token"])
                if RequestData and UserId:
                    TopicId = RequestData["TopicId"]
                    text = RequestData["text"]
                    DBWorker.Message().create(TopicId, UserId, text)
                    return 201
            elif request.method == "DELETE":
                RequestData = request.get_json()

                TopicId = RequestData["MessageId"]
                UserId = get_jwt_identity(RequestData["token"])

                UserData = DBWorker.User().get(user = UserId)
                TopicData = DBWorker.Message().get(MessageId = TopicId)
                if TopicData.auhor == UserId or UserData.IsAdmin:
                    DBWorker.Message().get(MessageId = TopicId)
                    return 200
                else:
                    return "Denied", 403
                
        @self.server.route("/api/messages/all")
        def TopicAll():
            return DBWorker.Messagee().all(format="json")
            

        SockIO.run(self.server, host=host,port=port, debug=IsDebug)