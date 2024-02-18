#external classes
from msilib.schema import SelfReg
from typing import Self
from flask import *
from flask import render_template as render
from werkzeug.utils import secure_filename
from pathlib import *
import os
from pathlib import *

# local classes
from .loggers import *
from .forum import *
from .tools import *
from .abcd_classes import *
from .tools import *
from .user_class import *
from .topic import *
from .snippets import *

global topic


class server:




    def __init__(self,  class_logger, db, frm , prt=8000, dbg=False, hst="127.0.0.1"):

        #settings of server's behavior
        self.hosT = hst
        self.porT = prt
        self.dbG = dbg
        self.server = Flask(__name__)
        self.server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        self.class_logger = class_logger
        self.frm = frm
        app = Flask(__name__, static_folder="static")



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
            data  = self.frm.all()
            TopicsData = topic.all_(db)
            print(TopicsData)
            tok = request.cookies.get('token')
            data = db.excute_query(f"SELECT * FROM user WHERE token = '{tok}'")
            TopicString = """ """
            for i in TopicsData:
                TopicString += tt_snippet(title=i[1], description=i[3], topic_num=i[4])
            try:
                return render("index.html", forum=self.frm.name, TopicHtml = TopicString, logo_path = data[0][5], user=data[0][2])      
            except:
                return render("index.html")


        #auth methods
        # structure of table user: password, user_id, is_admin, is_banned, logo_path, citate, time_of_join, token
        @self.server.route('/auth/reg', methods=["GET", "POST"])
        def reg():
            print(request.method)
            if request.method == "GET":
                # return page of registration
                tok = request.cookies.get('token')
                data = db.excute_query(f"SELECT * FROM user WHERE token = '{tok}'")
                if len(data) > 0:
                    return redirect("/")
                else:
                    return render_template("reg.html")
            elif request.method == "POST":
                # getting data from POST request
                citate = "я люблю собак"
                login = request.form.get("login")
                email = request.form.get("email")
                password = request.form.get("password")
                citate = request.form.get("citate")
                file = request.files.get('logo')
                if file.filename == '': 
                    return redirect(request.url)
                if file and allowed_file(file.filename):
                    open( os.path.join(os.getcwd(), "classes\media", file.filename) , "w" ).close() 
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(os.getcwd(), "classes\media", file.filename))
                    u = user(password=password, user_id=login, is_admin = 0, is_banned=0, logo_path = filename,citate = citate,
                             time_of_join= get_current_time(), db = db, email = email)
                    resp = redirect('/')
                    resp.set_cookie("token", u.token)
                    return resp
                else:
                    return "400 Bad Request"


        #log method
        @self.server.route("/auth/log", methods=["GET", "POST"])
        def log():
            if request.method == "GET":
                tok = request.cookies.get('token')
                data = db.excute_query(f"SELECT * FROM user WHERE token = '{tok}'")
                if len(data) > 0:
                    return redirect("/")
                else:
                    return render_template("log.html")
            elif request.method == "POST":
                login = request.form.get("login")
                password = request.form.get("password")
                u = user.get(login, password, db)[0]
                resp = redirect("/")
                resp.set_cookie("token", u[8])
                return resp
            

        #logging out
        @self.server.route("/auth/dislog", methods=["GET"])
        def dislog():
            resp = redirect("/")
            resp.set_cookie("token", "Null")
            return resp
        

        #topic view
        @self.server.route("/topic", methods=["GET"])
        def Topic():
            
            tok = request.cookies.get('token')
            print(tok)
            data = db.excute_query(f"SELECT * FROM user WHERE token = '{tok}'")
            print(data)

            Id = request.args.get('id')
            return render_template("topic.html", forum=self.frm.name, logo_path = data[0][5], user=data[0][2])

        #topic create
        @self.server.route("/topic/create", methods = ["POST", "GET", "PATCH"])
        def TopicCreate():
            if request.method == "GET":

                tok = request.cookies.get('token')
                print(tok)
                data = db.excute_query(f"SELECT * FROM user WHERE token = '{tok}'")
                print(data)
                
                return render_template("CreateTopic.html", forum=self.frm.name, logo_path = data[0][5], user=data[0][2])
            elif request.method == "POST":

                tok = request.cookies.get('token')
                print(tok)
                data = db.excute_query(f"SELECT * FROM user WHERE token = '{tok}'")
                
                #creating new thread
                theme = request.form.get("name")
                name = request.form.get("theme")
                about = request.form.get("about")

                

                a = topic(get_current_time(), theme, data[0][2], about,generate_id(), db)
                
                
            else:
                return ["400"]

        
    def runserver(self):

        self.server.run(host=self.hosT, port = self.porT, debug=self.dbG)


        
