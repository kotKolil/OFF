from classes.loggers import *
from pathlib import *
from classes.serv import *


a_logger = txt_log(p4th=Path.cwd(),filename="a.log")
A = server()
A.runserver()