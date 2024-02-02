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
            tok = request.cookies.get('token')
            print(tok)
            data = db.excute_query(f"SELECT * FROM user WHERE token = '{tok}'")
            print(data)

            try:
                return render("index.html", forum=self.frm.name, logo_path = data[0][4], user=data[0][1])      
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
                    u = user(password=password, user_id=login, is_admin = 0, is_banned=0, logo_path = filename,citate = citate, time_of_join= get_current_time(), db = db)
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
                data = db.excute_query(f"SELECT * FROM user WHERE user_id = '{login}' and password = '{password}' ")[0]
                resp = redirect("/")
                resp.set_cookie("token", data[7])
                return resp
            

        #logging out
        @self.server.route("/auth/dislog", methods=["GET"])
        def dislog():
            resp = redirect("/")
            resp.set_cookie("token", "Null")
            return resp
        

        #topic view
        @self.server.route("/topic", methods=["GET", "POST"])
        def topic():
            request.args.get('id')
            if request.method == "GET":
                return render_template("topic.html")

        
    def runserver(self):

        self.server.run(host=self.hosT, port = self.porT, debug=self.dbG)


        