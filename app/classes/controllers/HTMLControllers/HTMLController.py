import sys

sys.path.append("...")
import sqlite3
from flask import render_template as render
from flask import *
from flask_jwt_extended import *
from app.classes.Serialisation.TableFieldsStorage import *
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

    # serving static files
    @route("/static/<path:path>")
    def static_files(self, path):
        return send_from_directory(STATIC_PREFIX, path)

    # serving media files
    @route("/media/<path:path>")
    def media_files(self, path):
        print(MEDIA_PREFIX)
        return send_from_directory(MEDIA_PREFIX, path)

    # index page
    @route('/')
    def index(self):
        return render("index.html")

    # topic page
    @route('/topic')
    def topic(self):
        return render("topic.html")

    @route("/topic/create", methods=['GET', 'POST'])
    def TopicCreate(self):
        if request.method == "GET":
            if decode_token(request.cookies.get("token").encode()):
                return render("CreateTopic.html")
            else:
                return redirect("/auth/log")
        elif request.method == "POST":
            theme = request.form.get("theme")
            about = request.form.get("about")
            protected = request.form.get("protected")
            if decode_token(request.cookies.get("token")):
                jwt_data = decode_token(request.cookies.get("token").encode())
                user_id = jwt_data["sub"]
                user_data = self.server_object.DBWorker.user().get(username=user_id, format="obj")
                if not user_data.IsActivated:
                    return render("info.html",
                                  message="you are not activated you account. Please, go to your e-mail and activate")
                if user_data.IsBanned:
                    return render("info.html", message="you are banned on this forum. Please, contact with moderators")
                else:
                    try:
                        self.server_object.DBWorker.topic().create(theme, user_data.UserId, about,
                                                                   str((protected == "on") * 1), format="obj")
                        return redirect("/")
                    except Exception as e:
                        return [0, str(e)]
            else:
                return render("info.html", message="you are not logged in. Please, log in or reg")

    @route('/auth/reg', methods=["GET", "POST"])
    def reg(self):
        if request.method == "GET":
            if request.cookies.get("JWToken"):
                is_logged = decode_token(request.cookies.get("token"))
            else:
                is_logged = False
            if not is_logged:
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
                file.save(os.path.join(os.getcwd(), MEDIA_PREFIX, file.filename))
                try:
                    u = self.server_object.DBWorker.user().create(password=password, email=email,
                                                                  username=login, is_admin=0,
                                                                  is_banned=0, logo_path=filename,
                                                                  citate=citate, format="obj")
                    self.server_object.DBWorker.topic().create(
                        "Private page of {}".format(u.UserId), u.UserId,
                        "The Wall", 0, format="obj", TopicId=u.UserId)
                    self.server_object.MailWorker.send_message(email,
                                                              """Hello! Go to this link http://{}:{}/ActivateEmail?num={}""".format(
                                                                  self.server_object.host,
                                                                  self.server_object.port,
                                                                  u.ActiveNum),
                                                              "Account Activating")
                    resp = make_response(render("info.html", message = "Please, go to your email and activate account"))
                    jw_token = create_access_token(identity=u.UserId)
                    resp.set_cookie("token", jw_token)
                    return resp
                except sqlite3.IntegrityError:
                    return render_template("reg.html", message="Username already used")
            else:
                return "400", 400

    @route("/auth/log", methods=["GET", "POST"])
    def log(self):
        if request.method == "GET":
            if request.cookies.get("JWToken"):
                is_token = decode_token(request.cookies.get("JWToken"))
            else:
                is_token = False
            if not is_token:
                return render("log.html")
            else:
                return redirect("/")
        elif request.method == "POST":
            login = request.form.get("login")
            password = request.form.get("password")
            u = self.server_object.DBWorker.user().get(token=generate_token(login, password), format="obj")
            if u == 0:
                return render("log.html", Text="Incorrect user or password")
            else:
                resp = redirect("/")
                jw_token = create_access_token(identity=u.UserId)
                resp.set_cookie("token", jw_token)
                return resp

    """ entrypoint for changing password 
    in GET method we return for password changing 
    in POST method we get data from this form """

    @route("/auth/change_password", methods=["GET", "POST", "PATCH"])
    def ChangePassword(self):
        if request.method == "GET":
            return render("change_password.html")
        elif request.method == "POST":
            user = request.form.get("user")
            email = request.form.get("email")
            new_password = request.form.get("NewPassword")
            user_data = self.server_object.DBWorker.user().get(user=user, format="obj")
            if user_data != 0:
                self.server_object.MailWorker.SendMessage(email,
                                                          "Please, go to this link... http://{}:{}/"
                                                          "auth/action_change_password?num={}&NewPassword={}".format(
                                                              self.server_object.host,
                                                              self.server_object.port,
                                                              user_data.ActiveNum,
                                                              new_password),
                                                          "password changing")
                return render("info.html", message="check your email")
            else:
                return render("change_password.html", message="invalid user")

    @route("/auth/action_change_password", methods=["GET", "POST"])
    def PasswordChangeForm(self):
        if request.args.get("num") and request.args.get("NewPassword"):
            num = request.args.get("num")
            new_password = request.args.get("NewPassword")
            user_data = self.server_object.DBWorker.user().get(num=num, format="obj")
            if isinstance(user_data, UserStorage) and str(user_data.ActiveNum) == num:
                user_hash = generate_token(user_data.UserId, new_password)
                user_data.token = user_hash
                user_data.save()
                return render("info.html", message="password updated. Please, log in system")

    # logging out
    @route("/auth/dislog", methods=["GET"])
    def dislog(self):
        resp = redirect("/")
        resp.set_cookie("token", "Null")
        return resp

    @route("/ActivateEmail")
    def ActivateEmail(self):
        num = request.args.get('num')
        self.server_object.logger.info(num)
        user_data = self.server_object.DBWorker.user().get(num=num, format="obj")
        self.server_object.logger.info(user_data.__dict__)
        if user_data.IsActivated == 1:
            return render("info.html", message="account is activated now")

        user_data.IsActivated = 1
        user_data.ActiveNum = 0
        user_data.save()

        self.server_object.MailWorker.send_message(user_data.email,
                                                  "Congratulations! Account is activated!",
                                                  "account status")

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
            user_id = decode_token(request.cookies.get("token"))["sub"]
            user_data = self.server_object.DBWorker.user().get(user=user_id, format="obj")

            if user_data.IsAdmin == 1:
                return render("user_moderation.html")

            else:
                return render_template("info.html", message="HTTP 403. Access denied")

        except Exception:
            return render_template("info.html", message="HTTP 403. Access denied")

    @route("/FAQ")
    def FuYo(self):
        return render("faq.html")
