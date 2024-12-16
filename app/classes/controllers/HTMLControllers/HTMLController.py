import os
import sys

sys.path.append("...")

import sqlite3
from flask import render_template as render
from flask import *
from flask_jwt_extended import *
from app.classes.Serialisation.storage import *
from config import *
from app.classes.other.tools import *
from werkzeug.utils import secure_filename

class HTMLController:
    def __init__(self, server_object):
            self.server_object = server_object
            self.bp = Blueprint('HTML controller', __name__)
            self.register_routes()
    def register_routes(self):
        # Loop through all methods in the class
        for method_name in dir(self):
            method = getattr(self, method_name)
            if callable(method) and hasattr(method, 'route'):
                if hasattr(method, "methods"):
                    # Register the method as a route
                    self.bp.add_url_rule(method.route, view_func=method, methods=method.methods)
    @staticmethod
    def route(path, methods=['GET']):
        """Decorator to define route path and methods."""
        def decorator(func):
            func.route = path
            func.methods = methods
            return func
        return decorator

    #serving static files
    @route("/static/<path:path>")
    def static_files(self, path):
        return send_from_directory(STATIC_PREFIX, path)

    #serving media files
    @route("/media/<path:path>")
    def media_files(self,path):
        print(MEDIA_PREFIX)
        return send_from_directory(MEDIA_PREFIX, path)

    #index page
    @route('/')
    def index(self):
        return render("index.html")

    #topic page
    @route('/topic')
    def topic(self):
        return render("topic.html")

    @route("/topic/create", methods=['GET', 'POST'])
    def TopicCreate(self):
        if request.method == "GET":
            if decode_token(request.cookies.get("token").encode()):
                return render("CreateTopic.html")
            else:
                redirect("/auth/log")
        elif request.method == "POST":
            Name = request.form.get("name")
            Theme = request.form.get("theme")
            About = request.form.get("about")
            protected = request.form.get("protected")

            if decode_token(request.cookies.get("token")):

                JWTData = decode_token(request.cookies.get("token").encode())
                UserId = JWTData["sub"]

                UserData = self.server_object.DBWorker.User().get(user = UserId, format = "obj")

                if not  UserData.IsActivated:

                    return render("info.html", message = "you are not activated you account. Please, go to your e-mail and activate")

                if UserData.IsBanned:

                    return render("info.html", message = "you are banned on this forum. Please, contact with moderators")
                else:

                    try:

                        NewTopic = self.server_object.DBWorker.Topic().create(Theme, UserData.UserId, About, str( (protected == "on") * 1), format="obj")
                        return redirect("/")

                    except Exception as e:
                        return [0, str(e)]

            else:

                return render("info.html", message="you are not logged in. Please, log in or reg")

            # NewTopic = DBWorker.Topic().create(Theme, )


    #auth methods
    # structure of table user: password, user_id, is_admin, is_banned, logo_path, citate, time_of_join, token
    @route('/auth/reg', methods=["GET", "POST"])
    def reg(self):
        if request.method == "GET":
            if request.cookies.get("JWToken"):
                IsLogged = decode_token(request.cookies.get("token"))
            else:
                IsLogged = False
            if not IsLogged:
                return render("reg.html")
            else:
                return redirect("/")
        elif request.method == "POST":

            # getting data from POST request
            login = request.form.get("login")
            email = request.form.get("email")
            password = request.form.get("password")
            citate = request.form.get("citate")
            file = request.files.get('logo')

            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(os.getcwd(), "classes\media", file.filename))
                try:
                    u = self.server_object.DBWorker.User().create(password=password, email = email, user=login, is_admin = 0, is_banned=0, logo_path = filename,citate = citate, format = "obj")
                    TheWall = self.server_object.DBWorker.Topic().create(f"Private page of {u.UserId}", u.UserId, "The Wall", 0, format = "obj", TopicId = u.UserId)
                    self.server_object.MailWorker.SendMessage(email, f"Hello! Go to this link http://{self.server_object.host}:{self.server_object.port}/ActivateEmail?num={u.ActiveNum}", "Account Activating")
                    resp = make_response("go to your email to activate email", 200)

                    resp.mimetype = "text/plain"

                    JWToken = create_access_token(identity=u.UserId)

                    resp.set_cookie("token", JWToken)
                    return resp
                except sqlite3.IntegrityError:
                    return render_template("reg.html", message="Username already used")

            else:
                return "400",400


    #log method
    @route("/auth/log", methods=["GET", "POST"])
    def log(self):
        if request.method == "GET":
            if request.cookies.get("JWToken"):
                IsToken = decode_token(request.cookies.get("JWToken"))
            else:
                IsToken = False
            if not IsToken:
                return render("log.html")
            else:
                return redirect("/")
        elif request.method == "POST":

                login = request.form.get("login")
                password = request.form.get("password")
                u = self.server_object.DBWorker.User().get(token = generate_token(login, password), format = "obj")
                if u == 0:
                    return render("log.html", Text="Incorrect user or password")
                else:
                    resp = redirect("/")
                    JWToken = create_access_token(identity=u.UserId)
                    resp.set_cookie("token", JWToken)
                    return resp

    """
    
    entripoint for changing passowrd
    
    in GET method we return for password changing
    in POST method we get data from this form
    
    """
    @route("/auth/change_password", methods=["GET","POST", "PATCH"])
    def ChangePswd(self):

        if request.method == "GET":
            return render("change_pswd.html")
        elif request.method == "POST":
            user = request.form.get("user")
            email = request.form.get("email")
            NewPassword = request.form.get("NewPswd")

            UserData = self.server_object.DBWorker.User().get(user = user, format = "obj")
            if UserData != 0:
                self.server_object.MailWorker.SendMessage(email, f"""Please, go to this link 
                http://{self.server_object.host}:{self.server_object.port}/auth/action_change_password?num={UserData.ActiveNum}&NewPswd={NewPassword} 
to change password""", "password changing")
                return render("info.html", message = "check your email")
            else:
                return render("change_pswd.whtml", message = "invalid user")

    @route("/auth/action_change_password", methods = ["GET", "POST"])
    def PasswordChangeForm(self):
        if request.args.get("num") != None and request.args.get("NewPswd") != None:
            Num = request.args.get("num")
            NewPswd = request.args.get("NewPswd")
            UserData = self.server_object.DBWorker.User().get(num = Num, format = "obj")
            if isinstance(UserData, UserStorage) and str(UserData.ActiveNum) == Num:
                UserHash = generate_token(UserData.UserId, NewPswd)
                UserData.token = UserHash
                UserData.save()
                return render("info.html", message = "password updated.Please, log in system")

    #logging out
    @route("/auth/dislog", methods=["GET"])
    def dislog(self):
        resp = redirect("/")
        resp.set_cookie("token", "Null")
        return resp

    @route("/ActivateEmail")
    def ActivateEmail(self):
        num = request.args.get('num')

        UserData = self.server_object.DBWorker.User().get(num=num, format = "obj")


        if UserData.IsActivated == 1:
            return render("info.html", message="account is activated now")

        UserData.IsActivated = 1
        UserData.ActiveNum = 0

        UserData.save()

        self.server_object.MailWorker.SendMessage(UserData.email, "Congrutulasions! Account is activated!", "account status")

        return render("info.html", message="Account is activated")

    @route("/api/GetForumName")
    def ForumNameGet(self):
        return {"ForumName": self.server_object.ForumName}


    @route("/UserPage")
    def PageUser(self):
        return render_template("user_page.html")

    @route("/moderate/users")
    def UsersModerate(self):
        try:
            UserId = decode_token(request.cookies.get("token"))["sub"]
            UserData = self.server_object.DBWorker.User().get(user = UserId, format = "obj")
            if UserData.IsAdmin == 1:
                return render("user_moderation.html")
            else:
                return render_template("info.html", message = "HTTP 403. Access denied")
        except:
            return render_template("info.html", message="HTTP 403. Access denied")

    @route("/FAQ")
    def FuYo(self):
        return render("faq.html")