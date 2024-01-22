from msilib.schema import SelfReg
from typing import Self
from flask import *
from flask import render_template as render
from .loggers import *
from .forum import *
from .tools import *
from .abcd_classes import *


class server:




    def __init__(self,  class_logger, db, prt=8000, dbg=False, hst="127.0.0.1",):

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
        
        #index page
        @self.server.route('/')
        def index():
            return render("index.html")        

        #thread page
        @self.server.route('/thread/<string:thd_id>')
        def thread(thd_id):
            print(thd_id)
            return render("tread.html", thd_id=thd_id)
        
        @self.server.route('/topic/<string:mes_id>')
        def topic(mes_id):
            return render("detail.html")

    def runserver(self):

        self.server.run(host=self.hosT, port = self.porT, debug=self.dbG)


        