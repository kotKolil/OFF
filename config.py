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
    DBhost = "127.0.0.1"

    ForumName = "Awesome Forum"
    IsDebug = True

    AdminUser = "tomfox"
    AdminPassword = "14037176"
    AdminName = "Abu"
    AdminCitate = "der mench is bose"
    AdminLogoPath = "admin.png"
    
    MailSite = "smtp.yandex.ru"
    MailPort = "587"
    MailLogin = ""
    MailPassword = ""

    AppSecretKey = "230597"
    JwtSecretKey = "230597"
