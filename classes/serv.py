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

# local classes
from .loggers import *
from .tools import *


class server:

    def __init__(self,  ClassLoger, DBWorker, port=8000, IsDebug=True, host="127.0.0.1", AdminUser = "", AdminName = "", AdminPassword = "", AdminCitate = "admin always right",AdminLogoPath = "/media/admin.png", ForumName = "Forum", MailWorker = ""):
        #settings of server's behavior
        self.host = host
        self.port = port
        self.IsDebug = IsDebug
        self.server = Flask(__name__)
        self.server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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

            system("cls")
            print(message)

            UserToken = message["UserToken"]
            ThreadId = message["ThreadId"]
            Message = message["Message"]
            
            UserData = DBWorker.User().GetViaTokenJson(UserToken)
            DBWorker.Message().create(ThreadId, UserData["UserId"], Message, get_current_time())

            emit("message", {"UserData":UserData, "MessageData":{"text":Message, "TopicId":ThreadId}}, broadcast=True)

            








        @SockIO.on("connect")
        def OnOpenEvent():
            print("WebSockets connection estabilished")



        #views, wich handle errors
        @self.server.errorhandler(404)
        def Handler404(e):

            tok = request.cookies.get('token')
            
            data = DBWorker.User().GetViaToken(tok)
            try:
                return render("index.html",  TopicHtml="<H1>404. Page not found")      
            except:
                return render("index.html", logo_path="default.png")
            



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


        #auth methods
        # structure of table user: password, user_id, is_admin, is_banned, logo_path, citate, time_of_join, token
        @self.server.route('/auth/reg', methods=["GET", "POST"])
        def reg():
            if request.method == "GET":
                # return page of registration
                tok = request.cookies.get('token')
                data = DBWorker.User().GetViaTokenJson(tok)
                if data:
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
                    #open( os.path.join( os.getcwd(),"classes\media", file.filename ) , "w" ).close() 
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(os.getcwd(), "classes\media", file.filename))
                    try:
                        u = DBWorker.User().create(password=password, email = email, user=login, is_admin = 0, is_banned=0, logo_path = filename,citate = citate)
                        MailWorker(f"Hello! Go to this link http://{host}/ActivateEmail?num={u.ActiveNum}")
                        resp = render("info.html", message = f"<p>Go to your email to activate your account</p>")
                        
                        resp.set_cookie("token", u.token)
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
                if DBWorker.User().GetViaTokenJson(tok):
                    return redirect("/")
                else:
                    return render_template("log.html")
            elif request.method == "POST":

                try:

                    login = request.form.get("login")
                    password = request.form.get("password")
                    u = DBWorker.User().get(login, password)
                    resp = redirect("/")
                    resp.set_cookie("token", u.token)
                    return resp
                
                except:
                    
                    return render_template("log.html", Text = "Incorret User or Password")


            

        #logging out
        @self.server.route("/auth/dislog", methods=["GET"])
        def dislog():
            resp = redirect("/")
            resp.set_cookie("token", "Null")
            return resp
        

        #topic view
        @self.server.route("/topic", methods=["GET", "POST"])
        def Topic():
            if request.method == "GET":
                return render_template("topic.html")

        #topic create
        @self.server.route("/topic/create", methods = ["POST", "GET", "PATCH"])
        def TopicCreate():
            if request.method == "GET":

                tok = request.cookies.get('token')
                data = DBWorker.User().GetViaToken(tok)

                try:
                    return render_template("CreateTopic.html", logo_path = data.LogoPath, user=data.UserId)
                except:
                    return redirect("/auth/log")
            elif request.method == "POST":


                tok = request.cookies.get('token')
                data = DBWorker.User().GetViaToken(tok)
                
                #creating new thread
                theme = request.form.get("name")
                name = request.form.get("theme")
                about = request.form.get("about")

                

                a = DBWorker.Topic().create(theme, data.UserId, get_current_time())

                return redirect("/auth/log")
                
                
            else:
                return ["400"]


        @self.server.route("/message", methods=["POST"])
        def PostMessage():
            if request.method == "POST":
                #LogoPath,Username, Message, Phrase
                tok = request.cookies.get('token')
                Text = request.form.get("Message")
                TopicId = request.form.get("TopicId")
                AuthToken = request.form.get("AuthToken")

                UserData = DBWorker.User().GetViaToken(tok)

                DBWorker.Message().create(TopicId, UserData.UserId, Text, get_current_time())

                return {"MessageSnippet":""}

        #this API is giving tokens for log in system
        @self.server.route("/api/auth")
        def ApiAuth(request):
            if request.method == "GET":
                data = request.get_json(force=False, silent=False, cache=True)
                if len(data) == 0:  
                    return jsonify(["400", "bad request"], status=400)
                
                pswd = data["pswd"]
                login = data["login"]
                data = DBWorker.User().get(login, pswd)
                return data[0][8]

        #this API is registrating users
        @self.server.route("/api/reg")
        def RegAPI(request):
            if request.method == "POST":
                data = request.get_json(force=False, silent=False, cache=True)
                citate = data["citate"]
                login = data["login"]
                email = data["email"]
                password = data["password"]
                citate = data["citate"]
                file = data['logo']
                if file and allowed_file(file.filename):
                    open( os.path.join(os.getcwd(), "classes\media", file.filename) , "w" ).close()
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(os.getcwd(), "classes\media", file.filename))
                    u = DBWorker.User().create(password=password, user_id=login, is_admin = 0, is_banned=0, logo_path = filename,citate = citate,
                                time_of_join= get_current_time(), email = email)
                    return jsonify([u.token, "201"], status=201)
                
                else:
                    return jsonify(["400", "bad request"], status=400)
            else:
                return jsonify(["400", "bad request"], status=400)
            

        #this API for work with topic
        @self.server.route("/api/topic")
        def ThreadAPI():
            if request.method == "GET":
                TopicId = request.args.get("TopicId", type= str)

                Messages = DBWorker.Message().AllJson(TopicId)

                TopicData = DBWorker.Topic().get(TopicId)

                return jsonify({"theme":TopicData.theme, "author":TopicData.author, "about":TopicData.about, "Msgs":Messages})
            elif request.method == "POST":
                data = request.get_json(force=False, silent=False, cache=True)
                tok = data['token']
                UsrLogin = DBWorker.user.GetViaToken(tok)

                #creating new thread
                theme = data["name"]
                name = data["theme"]
                about = data["about"]


                try:
                    a = DBWorker.Topic().create(theme, UsrLogin.UserId, about)
                    return 201
                except Exception as e:
                    return [str(e), 400]

                
        @self.server.route("/api/AllTopic")
        def AllTopic():
                Messages = DBWorker.Topic().AllJson()

                return Messages

        @self.server.route("/api/GetUserInfo")
        def GetUserInfo():
            if request.method == "GET":
                try:
                    data = request.args.get('token')
                    print(data)
                    user_data = DBWorker.User().GetViaTokenJson(data)  # Assuming this returns a dictionary
                    return jsonify(user_data)
                except:
                    return "0"
            return "0"  # Or you might want to return an error response here as well.
        

        @self.server.route("/DeleteTopic")
        def DeleteTopic():
            try:
                UserToken = request.cookies.get('token')
                Id = request.args.get('id')
                UserData = DBWorker.User().GetUserOnToken(UserToken)
                TopicData = DBWorker.Topic().GetViaToken(Id)

                if UserData.UserId == TopicData.author or UserData.IsAdmin:
                    DBWorker.topic.delete()
                    return render_template("info.html", message="Your deleted a thread")
                else:
                    return render_template("info.html", message="Your deleted a thread")
            except:
                return render_template("info.html", message="You dont have permession to delete thread")


        @self.server.route("/api/ForumInfo")
        def ForumInfo():

            NumOfTopic = len(DBWorker.Topic().AllJson())
            NumOfMessages = len(DBWorker.Message().AllJson_())
            NumsOfUsers = len(DBWorker.User().AllJson())

            

            return {"NumOfTopic":NumOfTopic, "NumOfMessages":NumOfMessages, "NumsOfUsers":NumsOfUsers, "Admin":AdminName, "ForumName": ForumName}
        
        @self.server.route("/ActivateEmail")
        def ActivateEmail():
            num = request.args.get('num')

            UserData = DBWorker.User().get(num=num)
            UserData.IsActivated = 1
            UserData.save()

            return render("info.html", message="Account is activated")
        


        SockIO.run(self.server, host=host,port=port, debug=IsDebug)