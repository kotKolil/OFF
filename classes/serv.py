from msilib.schema import SelfReg
from typing import Self
from flask import *
from flask import render_template as render
from .loggers import *
from .forum import *
from .tools import *
from .abcd_classes import *


class server:

    __metaclass__ = ABCMeta



    def __init__(self, prt=8000, dbg=False, hst="127.0.0.1", class_logger = txt_log(p4th="/", filename="default.log")):

        #settings of server's behavior
        self.hosT = hst
        self.porT = prt
        self.dbG = dbg
        self.server = Flask(__name__)
        self.class_logger = class_logger




        #serving static files
        @self.__server.route("/static/<path:path>")
        def static_files(request, path):
            return send_from_directory('static', path)
        
        #views
        @self.error_decorator
        @self.__server.route('/')
        def index():
            print(v)
            return "<h3>It works!</h3>"



        