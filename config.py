import os
#settings for logger
logger_type = "console"
name_of_file = ""

#settings for BD
DBtype = ""
DBport = 5432
DBpassword = ""
DBuser = ""
DBname = "main.db"
DBhost = "127.0.0.1"

#settings for Forum
ForumName = "Awesome Forum"
IsDebug = True

#configuring Admin User
AdminUser = "admin"
AdminPassword = "1234567890"
AdminName = "anonim"
AdminCitate = ""
AdminLogoPath = "admin.png"

#configuring mail worker
MailSite = ""
MailPort = "587"
MailLogin = ""
MailPassword = ""

#configuring flask app
AppSecretKey = "1234567890"
JwtSecretKey = "1234567890"

#configurating app
APPport = 8000
APPhost = "127.0.0.1"

"""
explanation of PREFIX values creating

in python, function os.path.join() join parts of path to file or directory,
taking as a argument his parts
function os.getcwd() return path, where file run 
"""
TEMPLATE_PREFIX = os.path.join(os.getcwd(), "app", "templates", "")
MEDIA_PREFIX = os.path.join(os.getcwd(), "app", "media")
STATIC_PREFIX = os.path.join(os.getcwd(), "app", "static")