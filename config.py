import os
from pathlib import *

try:
    #here we getting variables of venv
    #if they exists, yes?
    2 / 0
    
except:
    #anyway, we are definig here variables

    LogPath = Path.cwd()
    LogFilename = "a.log"

    DBport = 8000
    DBpassword = ""
    DBuser = ""
    DBname = "main.db"
    DBhost = ""

    forum_name = "Awesome Forum"
    is_debug = True

    AdminUser = "tomfox"
    AdminPassword = "14037176"
    AdminName = "Abu"
    AdminCitate = "der mench is bose"
    AdminLogoPath = "/media/admin.png"
    