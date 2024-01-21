from msilib.schema import SelfReg
from typing import Self
from flask import *
from flask import render_template as render
from .loggers import *
from .forum import *
from .tools import *
from .abcd_classes import *


class server:




    def __init__(self, prt=8000, dbg=False, hst="127.0.0.1", class_logger = txt_log(p4th="/", filename="default.log"), db=sql_lite3_db("main.db"), frm=forum(db=sql_lite3_db("main.db"), name="Forum")):

        #settings of server's behavior
        self.hosT = hst
        self.porT = prt
        self.dbG = dbg
        self.server = Flask(__name__)
        self.class_logger = class_logger


        app = Flask(__name__, static_folder="static")


        #serving static files
        @self.server.route("/static/<path:path>")
        def static_files(request, path):
            print(path)
            return send_from_directory('static', path)
        
        #views
        @self.server.route('/')
        def index():
            return render("index.html")
        

        @self.server.route('/#<str:name>')
        def thread_view(name):
            return name
        
        @self.server.route('/topic/#<name>')
        def topic_view(name):
            return name

    def runserver(self):

        self.server.run(host=self.hosT, port = self.porT, debug=self.dbG)


        