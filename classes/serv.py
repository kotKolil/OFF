from msilib.schema import SelfReg
from typing import Self
from flask import *
from flask import render_template as render
from .loggers import *


class server:

    def error_decorator(self,func):
        def wrapper():
            try:
                resultant = func()
                return resultant
            except Exception as e:
                self.__class_logger.log_message(str(e))
                return str(e)
        return wrapper

    def __init__(self, prt=8000, dbg=False, hst="127.0.0.1", class_logger = txt_log(p4th="/", filename="default.log")):

        #settings of server's behavior
        self.__hosT = hst
        self.__porT = prt
        self.__dbG = dbg
        self.__server = Flask(__name__)
        self.__class_logger = class_logger

        #serving static files
        @self.__server.route("/static/<path:path>")
        def static_files(request, path):
            return send_from_directory('static', path)

        #views
        @self.error_decorator
        @self.__server.route('/')
        def index():
            # print(v)
            return "<h3>It works!</h3>"
        
    def runserver(self):
        try:
            self.__server.run(port = self.__porT, debug = self.__dbG)
            print(f"server started on {self.__hosT}:{self.__porT}. Debug mode is {self.__dbG}")
        except Exception as e:
            print(f"Server not started with error {str(e)}")


        