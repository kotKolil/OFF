from classes.loggers import *
from pathlib import *
from classes.serv import *


a_logger = txt_log(p4th=Path.cwd(),filename="a.log")
a_logger.log_message("weagaf")
A = server() 