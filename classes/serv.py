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

# local classes
from .loggers import *
from .forum import *
from .tools import *
from .tools import *
from .user_class import *
from .topic import *
from .snippets import *
from .message import *

class server:

    def __init__(self,  class_logger, db, frm , prt=8000, dbg=True, hst="127.0.0.1", AdminUser = "", AdminName = "", AdminPassword = "", AdminCitate = "admin always right"):
        #settings of server's behavior
        self.hosT = hst
        self.porT = prt
        self.dbG = dbg
        self.server = Flask(__name__)
        self.server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        self.class_logger = class_logger
        self.frm = frm
        self.AdminName = AdminName
        self.AdminUser = AdminUser
        self.AdminPassword = AdminPassword
        self.AdminCitate = AdminCitate
        self.AdminToken = generate_token(self.AdminPassword, self.AdminUser)
        SockIO = SocketIO(self.server)

        try:
            user(password=self.AdminPassword, user_id=self.AdminUser, is_admin = 0, is_banned=0, logo_path = "admin.png",citate =  AdminCitate ,
                                time_of_join= get_current_time(), db = db, email = "admin@example.com", token = generate_token(self.AdminPassword, self.AdminUser) )
        except:
            pass

        """
            json-request must be: 
            {
            "UserToken":"Vobla222",
            "ThreadId" : "Vobla333",
            "Message" : "Hell to this world!",
            }

            json response must be:

            {
                "Message":"LoL oMg (it is HTML snippet, not plain text!)",
                "ThreadId": "vobla333"
            }
        """

        @SockIO.on("message")
        def my_event(message):

            try:
                UserToken = message["UserToken"]
                ThreadId = message["ThreadId"]
                Message = message["Message"]
                
                UserData = user.GetUserOnToken(UserToken, db)

                #cheking, do user banned or not
                if UserData[0][4] == "1":
                    emit("message", {"error":"user is banned"})

                else:
                    message(get_current_time(), Message, UserData[0][2], ThreadId, generate_id(), db)
                    emit("message", {"Message":MessageSnippet(UserData[0][5],UserData[0][2], Message, UserData[0][6]), "ThreadId":ThreadId}, broadcast=True)



                
            except IndexError:
                message(get_current_time(), Message, "Anonim", ThreadId, generate_id(), db)
                emit("message", {"Message":MessageSnippet("default.png","", Message, ""), "ThreadId":ThreadId}, broadcast=True)
            






        @SockIO.on("connect")
        def OnOpenEvent():
            pass



        #views, wich handle errors
        @self.server.errorhandler(404)
        def Handler404(e):

            tok = request.cookies.get('token')
            
            data = user.GetUserOnToken(tok, db)
            try:
                return render("index.html", forum=self.frm.name, TopicHtml="<H1>404. Page not found")      
            except:
                return render("index.html", forum=self.frm.name, logo_path="default.png")
            
            return render_template()



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
            return render("index.html", forum=self.frm.name)      


        #auth methods
        # structure of table user: password, user_id, is_admin, is_banned, logo_path, citate, time_of_join, token
        @self.server.route('/auth/reg', methods=["GET", "POST"])
        def reg():
            if request.method == "GET":
                # return page of registration
                tok = request.cookies.get('token')
                data = user.GetUserOnToken(tok, db)
                if len(data) > 0:
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
                        u = user(password=password, user_id=login, is_admin = 0, is_banned=0, logo_path = filename,citate = citate,
                                time_of_join= get_current_time(), db = db, email = email, token = generate_token(login, password) )
                        resp = redirect('/')
                        
                        resp.set_cookie("token", u.token)
                        return resp
                    except sqlite3.IntegrityError:
                        return render_template("reg.html", message="invalid username")
  
                else:
                    return "400 Bad Request"


        #log method
        @self.server.route("/auth/log", methods=["GET", "POST"])
        def log():
            if request.method == "GET":
                tok = request.cookies.get('token')
                data = user.GetUserOnToken(tok, db)
                if len(data) > 0:
                    return redirect("/")
                else:
                    return render_template("log.html")
            elif request.method == "POST":
                try:
                    login = request.form.get("login")
                    password = request.form.get("password")
                    u = user.get(login, password, db)[0]
                    resp = redirect("/")
                    resp.set_cookie("token", u[8])
                    return resp
                except IndexError:
                    return redirect("auth/log")
            

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
            elif request.method == "POST":
                text = request.form.get("Message")
                TopicId = request.args.get('id')
                tok = request.cookies.get('token')
                

                data = user.GetUserOnToken(tok, db)
                #TimeOfCreation, Text, UserId, ThreadId, MessageId, db:object
                messages(get_current_time, text, data[0][2], TopicId, generate_id(), db)

                return redirect(f"/topic?id={TopicId}")

        #topic create
        @self.server.route("/topic/create", methods = ["POST", "GET", "PATCH"])
        def TopicCreate():
            if request.method == "GET":

                tok = request.cookies.get('token')
                data = user.GetUserOnToken(tok, db)

                try:
                    return render_template("CreateTopic.html", forum=self.frm.name, logo_path = data[0][5], user=data[0][2])
                except:
                    return redirect("/auth/log")
            elif request.method == "POST":

                tok = request.cookies.get('token')
                data = user.GetUserOnToken(tok, db)
                
                #creating new thread
                theme = request.form.get("name")
                name = request.form.get("theme")
                about = request.form.get("about")

                

                a = topic(get_current_time(), theme, data[0][2], about,generate_id(), db)

                return redirect("/")
                
                
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

                UserData = user.GetUserOnToken(tok, db)

                messages(get_current_time(), Text, UserData[0][2], TopicId, generate_id(), db)

                return {"MessageSnippet":MessageSnippet(UserData[0][5],UserData[0][2], Text, UserData[0][6])}

        #this API is giving tokens for log in system
        @self.server.route("/api/auth")
        def ApiAuth(request):
            if request.method == "GET":
                data = request.get_json(force=False, silent=False, cache=True)
                if len(data) == 0:  
                    return jsonify(["400", "bad request"], status=400)
                
                pswd = data["pswd"]
                login = data["login"]
                data = user.get(login, pswd, db)
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
                    u = user(password=password, user_id=login, is_admin = 0, is_banned=0, logo_path = filename,citate = citate,
                                time_of_join= get_current_time(), db = db, email = email)
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

                Messages = messages.all_(TopicId, db)

                return jsonify({"theme":topic.get(db, TopicId)[0][1], "author":topic.get(db, TopicId)[0][2], "about":topic.get(db, TopicId)[0][3], "Msgs":Messages})
            elif request.method == "POST":
                data = request.get_json(force=False, silent=False, cache=True)
                tok = data['token']
                UsrLogin = user.GetUserOnToken(tok, db)

                #creating new thread
                theme = data["name"]
                name = data["theme"]
                about = data["about"]


                try:
                    a = topic(get_current_time(), theme, UsrLogin[0][8], about,generate_id(), db)
                    return 201
                except Exception as e:
                    return [str(e), 400]

                
        @self.server.route("/api/AllTopic")
        def AllTopic():
                Messages = topic.all_(db)

                return Messages

        #this API send info about user
        @self.server.route("/api/GetUserInfo")
        def GetUserInfo():
            if request.method == "GET":
                data = request.args.get('token')
                try:
                    return user.GetUserOnToken(data, db)
                except Exception as e:
                    return [400, str(e)]
            return [400]
        

        @self.server.route("/DeleteTopic")
        def DeleteTopic():
            try:
                UserToken = request.cookies.get('token')
                Id = request.args.get('id')
                UserData = user.GetUserOnToken(UserToken, db)
                TopicData = topic.get(db, Id)
                system("cls")
                print(UserData)
                print(TopicData)
                print(UserData[0][2])
                print(TopicData[0][2])
                print(TopicData[0][4])
                if UserData[0][2] == TopicData[0][2] or UserData[0][2] == AdminUser:
                    topic.delete(db, TopicData[0][4])
                    return render_template("info.html", message="Your deleted a thread")
                else:
                    return render_template("info.html", message="Your deleted a thread")
            except:
                return render_template("info.html", message="You dont have permession to delete thread")



        @self.server.route("/AdminPage")
        def AdminPage():
            UserToken = request.cookies.get('token')
            UserData = user.GetUserOnToken(UserToken, db)
            if self.AdminUser == UserData[0][2]:
                return render_template("admin.html")
            else:
                return render_template("info.html", message = "You dont have permession")






        
            

        SockIO.run(self.server, host=hst,port=prt, debug=dbg)



