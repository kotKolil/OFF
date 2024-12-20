#external classes
from msilib.schema import SelfReg
from typing import Self
import collections
from flask import *
from flask import render_template as render
from werkzeug.utils import secure_filename
from werkzeug.exceptions import *
from pathlib import *
import os
from pathlib import *
from os import *
from flask_socketio import *
from time import *
from flask_socketio import *
import sqlite3
from flask import Flask, jsonify, request
from flask_jwt_extended import *
import sqlite3
import psycopg2

# local classes
from .loggers import *
from .tools import *
from .storage import *


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
        self.logger = logger

        SockIO = SocketIO(self.server)

        #creating Admin Acount
        try:
            AdminAkk = DBWorker.User().create(AdminPassword, "", AdminUser, 1,0,"admin.png",AdminCitate, format = "obj")
            AdminAkk.IsActivated = 1
            AdminAkk.save()

        except sqlite3.IntegrityError:
                self.logger.warning("Admin User Already Exists")
        @SockIO.on("TopicDelete")
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


        @SockIO.on("MessageDelete")
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

        @SockIO.on("connect")
        def OnOpenEvent():
            self.logger.info("WebSockets connection estabilished")
            emit("message", {"info":"WebSockets connection estabilished"})

        #views, wich handle errors
        @self.server.errorhandler(404)
        def Handler404(e):
            return render("info.html", message="HTTP 404.Page Not Found", code = 404)
            



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
                protected = request.form.get("protected")

                if decode_token(request.cookies.get("token")):

                    JWTData = decode_token(request.cookies.get("token").encode())
                    UserId = JWTData["sub"]

                    UserData = DBWorker.User().get(user = UserId, format = "obj")

                    if not  UserData.IsActivated:

                        return render("info.html", message = "you are not activated you account. Please, go to your e-mail and activate")
                    
                    if UserData.IsBanned:
                    
                        return render("info.html", message = "you are banned on this forum. Please, contact with moderators")
                    else:
                        
                        try:

                            NewTopic = DBWorker.Topic().create(Theme, UserData.UserId, About, str( (protected == "on") * 1), format="obj")
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
                        TheWall = DBWorker.Topic().create(f"Private page of {u.UserId}", u.UserId, "The Wall", 0, format = "obj", TopicId = u.UserId)
                        MailWorker.SendMessage(email, f"Hello! Go to this link http://{host}:{port}/ActivateEmail?num={u.ActiveNum}", "Account Activating")
                        resp = make_response("go to your email to activate email", 200)

                        resp.mimetype = "text/plain"
                        
                        JWToken = create_access_token(identity=u.UserId)

                        resp.set_cookie("token", JWToken)
                        return resp
                    except sqlite3.IntegrityError:
                        return render_template("reg.html", message="Username already used")
  
                else:
                    return "400",400


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

        """
        
        entripoint for changing passowrd
        
        in GET method we return for password changing
        in POST method we get data from this form
        
        """
        @self.server.route("/auth/change_password", methods=["GET","POST", "PATCH"])
        def ChangePswd():

            if request.method == "GET":
                return render("change_pswd.html")
            elif request.method == "POST":
                user = request.form.get("user")
                email = request.form.get("email")
                NewPassword = request.form.get("NewPswd")

                UserData = DBWorker.User().get(user = user, format = "obj")
                if UserData != 0:
                    MailWorker.SendMessage(email, f"""Please, go to this link 
                    http://{host}:{port}/auth/action_change_password?num={UserData.ActiveNum}&NewPswd={NewPassword} 
to change password""", "password changing")
                    return render("info.html", message = "check your email")
                else:
                    return render("change_pswd.whtml", message = "invalid user")

        @self.server.route("/auth/action_change_password", methods = ["GET", "POST"])
        def PasswordChangeForm():
            if request.args.get("num") != None and request.args.get("NewPswd") != None:
                Num = request.args.get("num")
                NewPswd = request.args.get("NewPswd")
                UserData = DBWorker.User().get(num = Num, format = "obj")
                if isinstance(UserData, UserStorage) and str(UserData.ActiveNum) == Num:
                    UserHash = generate_token(UserData.UserId, NewPswd)
                    UserData.token = UserHash
                    UserData.save()
                    return render("info.html", message = "password updated.Please, log in system")

        #logging out
        @self.server.route("/auth/dislog", methods=["GET"])
        def dislog():
            resp = redirect("/")
            resp.set_cookie("token", "Null")
            return resp

        @self.server.route("/api/user/CheckToken", methods = ["POST"])
        def CheckToken():
            JWToken = request.json["JWToken"]
            if decode_token(JWToken):
                return [1]
            else:
                return [0]

        @self.server.route("/api/user/generate_token", methods = ["POST"])
        def GenerateToken():
            if request.method == "POST":
                user = request.json["user"]
                pswd = request.json["password"]

                UserHash = generate_token(user, pswd)

                UserData = DBWorker.User().get(token = UserHash, format = "obj")
                logger.info(UserData)

                if type(UserData) != int:
                    JWToken = create_access_token(identity=UserData.UserId)
                    return {"JWToken":JWToken}, 201
                else:
                    return "400", 400
            else:
                return "400", 400


        @self.server.route("/api/user", methods=["GET", "POST", "CREATE" ,"DELETE"])
        def MisatoKForever():
            if request.method == "GET":
                JWToken = request.args.get("JWToken")
                UserId = request.args.get("UserId")
                if JWToken != None:
                    if decode_token(JWToken):
                        UserId = decode_token(JWToken)["sub"]
                        data = DBWorker.User().get(user = UserId, format = "json")
                        if type(data) != int:
                            return data
                        else:
                            return "404",404
                    else:
                        return "400", 400
                elif UserId != None:
                    data = DBWorker.User().get(user=UserId, format="json")
                    if type(data) != int:
                        return data
                    else:
                        return "404", 404

                else:
                    return "400", 400

            elif request.method == "POST":
                RequestData = request.json

                if RequestData:

                    email = RequestData["email"]
                    UserId = RequestData["UserId"]
                    password  = RequestData["password"]
                    citate = RequestData["citate"]

                    UserData = DBWorker.User().get(user = UserId, format = "ojb")
                    if UserData == 0:

                        u = DBWorker.User().create(password=password, email = email, user=UserId, is_admin = 0,
                                                   is_banned=0, logo_path = "default.png",citate = citate,
                                                   format = "obj")
                        MailWorker.SendMessage(TargetMail = email, text = f"""Hello! Go to this link http://{host}:{app}/ActivateEmail?num={u.ActiveNum} 
                        to activate you account""", Theme = "account activating")
                        message = f"<p>Go to your email to activate your account</p>"
                        return "201", 201
                    else:
                        return "400",400
                else:
                    return "400", 400
            elif request.method == "DELETE":
                RequestData = request.json
                user0 = decode_token(RequestData["JWToken"])["sub"]
                user0 = DBWorker.User().get(user = user0, format = "obj")
                user = RequestData["user"]
                if user0 == user or user0.IsAdmin:
                    try:
                        DBWorker.User().delete(user = user)
                        return "201", 201
                    except:
                        return "404", 404
                else:
                    return "403", 403

        @self.server.route("/api/user/change/user", methods = ["POST"])
        def UserChange():

            Data = request.json

            UserIdFromToken = decode_token(Data["token"])["sub"]
            citate = Data["citate"]

            UserData = DBWorker.User().get(user = UserIdFromToken, format = "obj")
            logger.info(UserData.__dict__)

            if UserData.UserId != "":

                #if citate is not set, we are changing password and user id
                if citate == "":

                    Password = Data["password"]
                    NewUserId = Data['NewUserId']

                    #creating new hash from user and password
                    UserData.UserId = NewUserId
                    UserData.token = generate_token(NewUserId, Password)
                    UserData.save()

                    #change all topics, create by user
                    AllUserTopic = DBWorker.Topic().all(format = "obj")
                    if not isinstance(AllUserTopic, collections.abc.Iterable):
                        AllUserTopic.author = NewUserId
                        AllUserTopic.save()

                    else:
                        for topic in AllUserTopic:
                            if topic.author == UserIdFromToken:
                                topic.author = NewUserId
                                topic.save()

                    #change all messages, create by user
                    AllUserMsg = DBWorker.Message().all(format = "obj")
                    if not isinstance(AllUserMsg, collections.abc.Iterable):
                        AllUserTopic.author = NewUserId

                    else:
                        for msg in AllUserMsg:
                            if msg.author == UserIdFromToken:
                                msg.author = NewUserId
                                msg.save()

                    return "201", 201

                else:
                    UserData.citate = citate
                    UserData.save()
                    return "201", 201

        @self.server.route("/api/user/change/admin", methods = ["POST"])
        def AdminUserChange():

            try:

                data = request.json

                AdminUserId = decode_token(data['AdminToken'])["sub"]
                UserId = data['UserId']
                is_banned = data["IsBanned"]
                is_admin = data["IsAdmin"]

                AdminUserData = DBWorker.User().get(user = AdminUserId, format = "obj")
                SimpleUserData = DBWorker.User().get(user = UserId, format = "obj")
                if AdminUserData.IsAdmin == 1:

                    if SimpleUserData.UserId != "" and SimpleUserData.UserId != self.AdminUser:
                        SimpleUserData.IsBanned = is_banned
                        SimpleUserData.IsAdmin = is_admin
                        SimpleUserData.save()
                        return "201",201
                    else:
                        return "404", 404

                else:
                    return "403", 403

            except IndexError or KeyError:

                return "400", 400


        @self.server.route("/ActivateEmail")
        def ActivateEmail():
            num = request.args.get('num')

            UserData = DBWorker.User().get(num=num, format = "obj")


            if UserData.IsActivated == 1:
                return render("info.html", message="account is activated now")

            UserData.IsActivated = 1
            UserData.ActiveNum = 0

            UserData.save()

            MailWorker.SendMessage(UserData.email, "Congrutulasions! Account is activated!", "account status")

            return render("info.html", message="Account is activated")

        @self.server.route("/api/user/all")
        def UserAll():
            if type(DBWorker.User().all(format="json")) != list:
                return [DBWorker.User().all(format="json")]

            return DBWorker.User().all(format="json")

        @self.server.route("/api/topic", methods=["GET", "POST", "DELETE", "PATCH"])
        def ApiTopic():
            if request.method == "GET":
                TopciId = request.args.get("TopicId")
                return DBWorker.Topic().get(TopicId = TopciId, format = 'json')
            elif request.method == "POST":
                RequestData = request.get_json()
                UserId = decode_token(RequestData["token"])["sub"]

                if RequestData and UserId:
                    theme = RequestData["theme"]
                    about = RequestData["about"]
                    is_protected = RequestData["is_protected"]

                    TopicCreated = DBWorker.Topic().create(theme, UserId, about, is_protected, format = "obj")
                    return DBWorker.Topic().get(TopicId = TopicCreated.TopicId, format = "json")

                else:
                    return 400

            elif request.method == "DELETE":
                RequestData = request.get_json()

                TopicId = RequestData["TopicId"]
                UserId = decode_token(RequestData["token"])["sub"]

                UserData = DBWorker.User().get(user = UserId, format = "obj")
                TopicData = DBWorker.Topic().get(TopicId = TopicId, format = "obj")
                if TopicData.author == UserId or UserData.IsAdmin == 1:
                    DBWorker.Topic().delete(TopicId = TopicId)
                    return "200", 200
                else:
                    return "403", 403

            elif request.method == "PATCH":

                # try:

                RequestData = request.get_json()

                UserId = decode_token(RequestData["token"])["sub"]
                TopicId = RequestData["TopicId"]

                Topic = DBWorker.Topic().get(TopicId = TopicId, format = "obj")
                User = DBWorker.User().get(user = UserId, format = "obj" )
                if Topic.author == UserId or User.IsAdmin == 1:
                    Topic.theme = RequestData["theme"]
                    Topic.about = RequestData["about"]
                    Topic.save()

                    return "201", 201

                # except:
                #
                #     return "400", 400


        @self.server.route("/api/topic/all")
        def AllTopic():
            if type(DBWorker.Topic().all(format = "json")) != list:
                return [DBWorker.Topic().all(format = "json")]
            return DBWorker.Topic().all(format = "json")


        @self.server.route("/api/messages", methods = ["GET", "POST", "DELETE", "PATCH"])
        def ApiMessage():
            if request.method == "GET":
                TopicId = request.args.get("TopicId")
                MessageId = request.args.get("MessageId")
                logger.info(TopicId)
                logger.info(MessageId)
                if TopicId != None:
                    if type(DBWorker.Message().get(TopicId = TopicId, format = 'json')) != list:
                        return [DBWorker.Message().get(TopicId = TopicId, format = 'json')]
                    return DBWorker.Message().get(TopicId=TopicId, format='json')
                elif MessageId != None:
                    MessageData = DBWorker.Message().get(MessageId = MessageId, format = "json")
                    if MessageData != []:
                        return MessageData, 200
                    return '404', 404

            elif request.method == "POST":
                RequestData = request.get_json()
                self.logger.info(text = RequestData)
                UserId = decode_token(RequestData["token"])["sub"]
                TopicData = DBWorker.Topic().get(TopicId = RequestData["TopicId"], format = "obj")
                if TopicData == []:
                    return "404", 404
                if RequestData and UserId and TopicData.protected != 1:
                    TopicId = RequestData["TopicId"]
                    text = RequestData["text"]
                    NewMessage = DBWorker.Message().create(TopicId, UserId, text, format = "json")
                    return NewMessage, 201
                elif TopicData.author == UserId and TopicData.protected == 1:
                    TopicId = RequestData["TopicId"]
                    text = RequestData["text"]
                    NewMessage = DBWorker.Message().create(TopicId, UserId, text, format = "json")
                    return NewMessage, 201
                else:
                    return "403",403
            elif request.method == "DELETE":
                RequestData = request.get_json()

                MessageId = RequestData["MessageId"]
                UserId = decode_token(RequestData["token"])["sub"]

                UserData = DBWorker.User().get(user=UserId, format='obj')
                MsgData = DBWorker.Message().get(MessageId=MessageId, format='obj')
                if MsgData.author == UserId or UserData.IsAdmin == 1:
                    DBWorker.Message().delete(MessageId = MessageId)
                    return "200", 201
                else:
                    return "403", 403

            elif request.method == "PATCH":

                RequestData = request.get_json()

                text = RequestData['text']
                MsgId = RequestData["MsgId"]
                UserId = decode_token(RequestData["token"])["sub"]

                MsgData = DBWorker.Message().get(MessageId = MsgId, format = "obj")

                if UserId == MsgData.author or UserId == AdminUser:

                    MsgData.text = text
                    MsgData.save()

                    return "201", 201

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
            try:
                UserId = decode_token(request.cookies.get("token"))["sub"]
                UserData = DBWorker.User().get(user = UserId, format = "obj")
                if UserData.IsAdmin == 1:
                    return render("user_moderation.html")
                else:
                    return render_template("info.html", message = "HTTP 403. Access denied")
            except:
                return render_template("info.html", message="HTTP 403. Access denied")

        @self.server.route("/FAQ")
        def FuYo():
            return render("faq.html")


        SockIO.run(self.server, host=host,port=port, debug=IsDebug)