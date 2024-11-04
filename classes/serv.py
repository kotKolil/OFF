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
from flask_sock import *
from time import *
from flask_socketio import *
import sqlite3
from flask import Flask, jsonify, request
from flask_jwt_extended import *
from flask_jwt_extended import exceptions
# local classes
from .loggers import *
from .tools import *


class server:

    def __init__(self,  ClassLoger, DBWorker, port=8000, IsDebug=True, host="127.0.0.1", AdminUser = "", AdminName = "", AdminPassword = "", 
                 AdminCitate = "admin always right",AdminLogoPath = "/media/admin.png", ForumName = "Forum", MailWorker:object = "", AppSecretKey = "", JwtSecretKey = ""):
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

        SockIO = SocketIO(self.server)

        #creating Admin Acount
        try:
            AdminAkk = DBWorker.User().create(AdminPassword, "", AdminUser, 1,0,"admin.png",AdminCitate, format = "obj")
            AdminAkk.IsActivated = 1
            AdminAkk.save()

        except sqlite3.IntegrityError:
            print("[debug]:Admin User Already Exists")

        @SockIO.on("TopicDelete")
        def topic_delete(message):

            decoder = json.JSONDecoder()
            message = decoder.decode(message)

            UserToken = decode_token(message["JWToken"])["sub"]
            TopicId = message["TopicId"]

            UserData = DBWorker.User().get(token = UserToken, format="obj")
            TopicData = DBWorker.Topic().get(TopicId = TopicId, format = "obj")

            if UserData.UserId == TopicData.author or UserData.IsAdmin == "1":
                DBWorker.Topic().delete(TopicId = TopicId)
                emit("TopicDelete", args = {"TopicId":TopicId}, broadcast=True)

        @SockIO.on("MessageDelete")
        def message_delete(message):

            decoder = json.JSONDecoder()
            message = decoder.decode(message)

            UserToken = decode_token(message["JWToken"])["sub"]
            MessageId = message["MessageId"]

            UserData = DBWorker.User().get(token = UserToken, format="obj")
            MessageData = DBWorker.Message().get(MessageId = MessageId, format = "obj")

            if UserData.UserId == MessageData.author or UserData.IsAdmin == "1":
                emit("TopicDelete", args={"TopicId": MessageData.TopicId, "MessageId":MessageId},
                     broadcast=True)

        @SockIO.on("message")
        def my_event(message):

            # try:
            decoder = json.JSONDecoder()
            message = decoder.decode(message)

            JWTData = decode_token(message["JWToken"])
            UserId = JWTData["sub"]
            TopicId = message["TopicId"]
            message = message["message"]

            UserData = DBWorker.User().get(user = UserId, format = "obj")

            result = ""
            
            if UserData.IsBanned != 1 and UserData.IsActivated == 1:

                result = DBWorker.Message().create(TopicId = TopicId, author = UserId ,  text = message, format="json")

                UserData.NumOfPosts += 1
                UserData.save()

                emit('NewMessage', result, broadcast=True)

            else:
                emit('NewMessage', 401, broadcast = False )

                
            # except Exception  as e:
            #     return emit('message', e, broadcast=False)

        @SockIO.on("connect")
        def OnOpenEvent():
            print("WebSockets connection estabilished")
            emit("message", {"info":"WebSockets connection estabilished"})

        #views, wich handle errors
        @self.server.errorhandler(404)
        def Handler404(e):
            return render("info.html", message="HTTP 404<p>Page Not Found")
            



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
        def topic():
            return render("topic.html")

        @self.server.route("/topic/create", methods=['GET', 'POST'])
        def TopicCreate():
            if request.method == "GET":
                if decode_token(request.cookies.get("token").encode()):
                    return render("CreateTopic.html")
                else:
                    redirect("/auth/log")
            elif request.method == "POST":
                Name = request.form.get("name")
                Theme = request.form.get("theme")
                About = request.form.get("about")

                if decode_token(request.cookies.get("token")):

                    JWTData = decode_token(request.cookies.get("token").encode())
                    UserId = JWTData["sub"]

                    UserData = DBWorker.User().get(user = UserId, format = "obj")

                    if not  UserData.IsActivated:

                        return render("info.html", message = "you are not activated you account. Please, go to your e-mail and activate")
                    
                    if UserData.IsBanned:
                    
                        return render("info.html", message = "you are banned on this forum. Please, contact with moderators")
                
                    if UserData.IsAdmin == 1:
                        
                        NewTopic = DBWorker.Topic().create(Theme,  UserData.UserId , About, format = "obj")
                        return redirect(f"http://{self.host}:{self.port}/topic?id={NewTopic.TopicId}")

                    else:
                        
                        try:

                            NewTopic = DBWorker.Topic().create(Theme, UserData.UserId, About, format="obj")
                            return redirect("/")
                        
                        except Exception as e:
                            return [0, str(e)]

                else:
                    
                    return render("info.html", message="you are not logged in. Please, log in or reg")

                # NewTopic = DBWorker.Topic().create(Theme, )
        

        #auth methods
        # structure of table user: password, user_id, is_admin, is_banned, logo_path, citate, time_of_join, token
        @self.server.route('/auth/reg', methods=["GET", "POST"])
        def reg():
            if request.method == "GET":
                if request.cookies.get("JWToken"):
                    IsLogged = decode_token(request.cookies.get("token"))
                else:
                    IsLogged = False
                if not IsLogged:
                    return render("reg.html")
                else:
                    return redirect("/")
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
                        u = DBWorker.User().create(password=password, email = email, user=login, is_admin = 0, is_banned=0, logo_path = filename,citate = citate, format = "obj")
                        MailWorker.SendMessage(email, f"Hello! Go to this link http://{host}/ActivateEmail?num={u.ActiveNum}", "Account Activating")
                        resp = make_response("go to your email to activate email", 200)

                        resp.mimetype = "text/plain"
                        
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
                if request.cookies.get("JWToken"):
                    IsToken = decode_token(request.cookies.get("JWToken"))
                else:
                    IsToken = False
                if not IsToken:
                    return render("log.html")
                else:
                    return redirect("/")
            elif request.method == "POST":

                    login = request.form.get("login")
                    password = request.form.get("password")
                    u = DBWorker.User().get(token = generate_token(login, password), format = "obj")
                    if u == 0:
                        return render("log.html", Text="Incorrect user or password")
                    else:
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
        
        
        
        @self.server.route("/api/user/ChangeLogo", methods = ["POST"])
        def ChangeLogo():
            if request.method == "POST":
                UserId = decode_token(request.json()["token"])["sub"]
                file = request.files.get('logo')
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(os.getcwd(), "classes\media", file.filename))
                    DBWorker.User().get(user = UserId).LogoPath = file.filename
                    return os.path.join(os.getcwd(), "classes\media", file.filename), 201
                return "Bad Request", 400

        

    
        

        @self.server.route("/api/user/CheckToken", methods = ["POST"])
        def CheckToken():
            JWToken = request.get_json()["JWToken"]
            if decode_token(JWToken):
                return [1]
            else:
                return [0]
            


        @self.server.route("/api/user", methods=["GET", "POST", "CREATE" ,"DELETE"])
        def MisatoKForever():
            if request.method == "GET":
                JWToken = request.args.get("JWToken")
                UserId = request.args.get("UserId")
                if JWToken != None:
                    if decode_token(JWToken):
                        UserId = decode_token(JWToken)["sub"]
                        return DBWorker.User().get(user = UserId, format = "json")
                    else:
                        return "400"
                elif UserId != None:
                    return DBWorker.User().get(user = UserId, format = "json")
                else:
                    return "400"

            elif request.method == "CREATE":
                RequestData = request.get_json()
                
                if RequestData:
                    
                    email = RequestData["email"]
                    UserId = RequestData["UserId"]
                    password  = RequestData["password"]
                    citate = RequestData["citate"]

                    try:
                        u = DBWorker.User().create(password, email, UserId, 0, 0, "", citate)
                        MailWorker(f"Hello! Go to this link http://{host}/ActivateEmail?num={u.ActiveNum} to activate you account")
                        message = f"<p>Go to your email to activate your account</p>"
                        return message, 201
                    except:
                        return "bad user or password", 400
                else:
                    return 400, "Bad Request"
                
            elif request.method == "DELETE":
                JWToken = request.args.get("JWToken")
                if decode_token(JWToken):
                    try:
                        DBWorker.User().delete(user = get_jwt_identity(JWToken))
                        return 200
                    except:
                        return 400
                else:
                    return 401

        @self.server.route("/ActivateEmail")
        def ActivateEmail():
            num = request.args.get('num')

            UserData = DBWorker.User().get(num=num, format = "obj")
            

            if UserData.IsActivated == 1:
                return render("info.html", message="account is activated now")

            UserData.IsActivated == 1

            UserData.save()

            MailWorker.SendMessage(UserData.email, "Congrutulasions! Account is activated!", "account status")

            return render("info.html", message="Account is activated")

        @self.server.route("/api/user/all")
        def UserAll():
            if type(DBWorker.User().all(format="json")) != list:
                return [DBWorker.User().all(format="json")]

            return DBWorker.User().all(format="json")
        
        @self.server.route("/api/topic", methods=["GET", "POST", "DELETE"])
        def ApiTopic():
            if request.method == "GET":
                TopciId = request.args.get("TopicId")
                return DBWorker.Topic().get(TopicId = TopciId, format = 'json')
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
                UserId = decode_token(RequestData["token"])["sub"]

                UserData = DBWorker.User().get(user = UserId, format = "obj")
                TopicData = DBWorker.Topic().get(TopicId = TopicId, format = "obj")
                print(TopicData.author)
                if TopicData.author == UserId or UserData.IsAdmin == "1":
                    DBWorker.Topic().delete(TopicId = TopicId)
                    return "200", 200
                else:
                    return "403", 403
            
        @self.server.route("/api/topic/all")
        def AllTopic():
            if type(DBWorker.Topic().all(format = "json")) != list:
                return [DBWorker.Topic().all(format = "json")]
            return DBWorker.Topic().all(format = "json")
        

        @self.server.route("/api/messages", methods = ["GET", "POST", "DELETE"])
        def ApiMessage():
            if request.method == "GET":
                TopicId = request.args.get("TopicId")
                if type(DBWorker.Message().get(TopicId = TopicId, format = 'json')) != list:
                    return [DBWorker.Message().get(TopicId = TopicId, format = 'json')]
            elif request.method == "POST":
                RequestData = request.get_json()
                UserId = decode_token(RequestData["token"])["sub"]
                if RequestData and UserId:
                    TopicId = RequestData["TopicId"]
                    text = RequestData["text"]
                    DBWorker.Message().create(TopicId, UserId, text)
                    return 201
            elif request.method == "DELETE":
                RequestData = request.get_json()

                # emit('NewMessage', result, broadcast=True)

                MessageId = RequestData["MessageId"]
                UserId = decode_token(RequestData["token"])["sub"]

                UserData = DBWorker.User().get(user = UserId)
                MsgData = DBWorker.Message().get(MessageId = MessageId)
                if MsgData.author == UserId or UserData.IsAdmin == "1":
                    DBWorker.Message().delete(MessageId = MessageId)
                    emit("MsgDel", result = {"TopicId":MsgData.TopicId, "MessageId":MsgData.MessageId}, broadcast=True)
                    return "200", 200
                else:
                    return "403", 403
                
        @self.server.route("/api/messages/all")
        def MessageAll():
            return DBWorker.Message().all(format="json")
    
        @self.server.route("/api/GetForumName")
        def ForumNameGet():
            return {"ForumName": self.ForumName}


        @self.server.route("/UserPage")
        def PageUser():
            return render_template("user_page.html")

        @self.server.route("/moderate/users")
        def UsersModerate():
            return render("user_moderation.html")


        SockIO.run(self.server, host=host,port=port, debug=IsDebug)