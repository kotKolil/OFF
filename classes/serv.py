import collections
import sqlite3
from flask import *
from flask import Flask, request
from flask import render_template as render
from flask_jwt_extended import *
from flask_socketio import *
from werkzeug.utils import secure_filename

from classes.loggers import *
from classes.storage import *
from classes.tools import *


class Server:

    def __init__(self, class_loger, db_worker, port=8000, is_debug=True, host="127.0.0.1", admin_user="", admin_name="",
                 admin_password="",
                 admin_citate="admin always right", admin_logo_path="/media/admin.png", forum_name="Forum",
                 mail_worker: object = "", app_secret_key="", jwt_secret_key="", logger=Logger()):
        # settings of Server's behavior
        self.host = host
        self.port = port
        self.IsDebug = is_debug
        self.server = Flask(__name__)
        self.jwt = JWTManager(self.server)
        self.server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        self.server.config['SECRET_KEY'] = app_secret_key
        self.server.config['JWT_SECRET_KEY'] = jwt_secret_key
        self.ClassLogger = class_loger
        self.admin_name = admin_name
        self.AdminUser = admin_user
        self.admin_password = admin_password
        self.AdminCitate = admin_citate
        self.AdminToken = generate_token(self.admin_password, self.AdminUser)
        self.AdminLogoPath = admin_logo_path
        self.forum_name = forum_name

        self.MailWorker = mail_worker
        self.logger = logger

        socket_io = SocketIO(self.server)

        # creating Admin Account
        try:
            admin_akk = db_worker.User().create(
                admin_password, "", admin_user, 1, 0, "admin.png", admin_citate, data_format="obj"
            )
            admin_akk.IsActivated = 1
            admin_akk.save()

        except sqlite3.IntegrityError:
            self.logger.warning("Admin user Already Exists")

        @socket_io.on("TopicDelete")
        def topic_delete(message):

            decoder = json.JSONDecoder()
            message = decoder.decode(message)

            user_token = decode_token(message["JWToken"])["sub"]
            topic_id = message["TopicId"]

            user_data = db_worker.User().get(user=user_token, data_format="obj")
            topic_data = db_worker.topic().get(topic_id=topic_id, data_format="obj")

            if user_data.user_id == topic_data.author or user_data.IsAdmin == 1:
                db_worker.topic().delete(topic_id=topic_id)
                db_worker.Message().delete(topic_id=topic_id)
                emit("TopicDelete", {"TopicId": topic_data.topic_id}, broadcast=True)

        @socket_io.on("MessageDelete")
        def topic_delete(message):

            decoder = json.JSONDecoder()
            message = decoder.decode(message)

            user_token = decode_token(message["JWToken"])["sub"]
            message_id = message["MessageId"]

            user_data = db_worker.User().get(user=user_token, data_format="obj")
            msg_data = db_worker.Message().get(message_id=message_id, data_format="obj")

            if user_data.user_id == msg_data.author or user_data.IsAdmin == 1:
                db_worker.Message().delete(message_id=message_id)
                emit("MsgDel", {"MessageId": message_id}, broadcast=True)

        @socket_io.on("message")
        def my_event(message):

            # try:
            decoder = json.JSONDecoder()
            message = decoder.decode(message)

            jwt_data = decode_token(message["JWToken"])
            user_id = jwt_data["sub"]
            topic_id = message["TopicId"]
            message = message["message"]

            user_data = db_worker.User().get(user=user_id, data_format="obj")
            topic_data = db_worker.topic().get(topic_id=topic_id, data_format="obj")

            if user_data.IsBanned != 1 and user_data.IsActivated == 1 and topic_data.protected != 1:

                result = db_worker.Message().create(topic_id=topic_id, author=user_id, text=message, data_format="json")

                user_data.numOfPosts += 1
                user_data.save()

                emit('NewMessage', result, broadcast=True)
            elif user_data.user_id == topic_data.author and topic_data.protected == 1:

                result = db_worker.Message().create(topic_id=topic_id, author=user_id, text=message, data_format="json")

                user_data.numOfPosts += 1
                user_data.save()

                emit('NewMessage', result, broadcast=True)

            else:
                emit('NewMessage', 401, broadcast=False)

            # except Exception  as e:
            #     return emit('message', e, broadcast=False)

        @socket_io.on("connect")
        def OnOpenEvent():
            self.logger.info("WebSockets connection established")
            emit("message", {"info": "WebSockets connection established"})

        # views, which handle errors
        @self.server.errorhandler(404)
        def Handler404() -> render:
            return render("info.html", message="HTTP 404.Page Not Found", code=404)

        # in this place we are registering error handlers
        self.server.register_error_handler(404, Handler404)

        # serving static files
        @self.server.route("/static/<path:path>")
        def static_files(path):
            return send_from_directory('static', path)

        # serving media files
        @self.server.route("/media/<path:path>")
        def media_files(path):
            return send_from_directory('media', path)

        # index page
        @self.server.route('/')
        def index():
            return render("index.html")

            # topic page

        @self.server.route('/topic')
        def topic():
            return render("topic.html")

        @self.server.route("/topic/create", methods=['GET', 'POST'])
        def topicCreate():
            if request.method == "GET":
                if decode_token(request.cookies.get("token")):
                    return render("CreateTopic.html")
                else:
                    redirect("/auth/log")
            elif request.method == "POST":
                theme = request.form.get("theme")
                about = request.form.get("about")
                protected = request.form.get("protected")

                if decode_token(request.cookies.get("token")):

                    jwt_data = decode_token(request.cookies.get("token"))
                    user_id = jwt_data["sub"]

                    user_data = db_worker.User().get(user=user_id, data_format="obj")

                    if not user_data.IsActivated:
                        return render("info.html",
                                      message="you are not activated you account. Please, go to your e-mail and "
                                              "activate")

                    if user_data.IsBanned:

                        return render("info.html",
                                      message="you are banned on this forum. Please, contact with moderators")
                    else:

                        try:

                            db_worker.topic().create(theme, user_data.user_id, about,
                                                     str((protected == "on") * 1), data_format="obj")
                            return redirect("/")

                        except Exception as e:
                            return [0, str(e)]

                else:

                    return render("info.html", message="you are not logged in. Please, log in or reg")

                # NewTopic = db_worker.Topic().create(Theme, )

        # auth methods
        # structure of table user: password, user_id, is_admin, is_banned, logo_path, citate, time_of_join, token
        @self.server.route('/auth/reg', methods=["GET", "POST"])
        def reg():
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
                    file.save(os.path.join(os.getcwd(), "classes\media", file.filename))
                    try:
                        u = db_worker.User().create(password=password, email=email, user=login, is_admin=0, is_banned=0,
                                                    logo_path=filename, citate=citate, data_format="obj")
                        db_worker.topic().create("Private page of {}".format(u.user_id), u.user_id,
                                                 "The Wall", 0,
                                                 data_format="obj", topic_id=u.user_id)
                        mail_worker.SendMessage(email,
                                                (
                                                    "Hello! Go to this link http://{}:{}/ActivateEmail?num={}\", "
                                                    "\"Account \n"
                                                    "Activating".format(host, port, u.active_num)
                                                ))
                        resp = make_response("go to your email to activate email", 200)
                        resp.mimetype = "text/plain"

                        jwt_token = create_access_token(identity=u.user_id)

                        resp.set_cookie("token", jwt_token)
                        return resp
                    except sqlite3.IntegrityError:
                        return render_template("reg.html", message="Username already used")

                else:
                    return "400", 400

        # log method
        @self.server.route("/auth/log", methods=["GET", "POST"])
        def log():
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
                u = db_worker.User().get(token=generate_token(login, password), data_format="obj")
                if u == 0:
                    return render("log.html", Text="Incorrect user or password")
                else:
                    resp = redirect("/")
                    jwt_token = create_access_token(identity=u.user_id)
                    resp.set_cookie("token", jwt_token)
                    return resp

        """
        
        entrypoint for changing password
        
        in GET method we return for password changing
        in POST method we get data from this form
        
        """

        @self.server.route("/auth/change_password", methods=["GET", "POST", "PATCH"])
        def change_password():

            if request.method == "GET":
                return render("change_password.html")
            elif request.method == "POST":
                user = request.form.get("user")
                email = request.form.get("email")
                new_password = request.form.get("new_password")

                user_data = db_worker.User().get(user=user, data_format="obj")
                if user_data != 0:
                    mail_worker.SendMessage(email,
                                            """Please, go to this link 
                                            http://{}:{}/auth/action_change_password?num={}&new_password={} 
                    to change password""".format(host, port, user_data.active_num, new_password),
                                            "password changing")
                    return render("info.html", message="check your email")

                else:
                    return render("change_password.html", message="invalid user")

        @self.server.route("/auth/action_change_password", methods=["GET", "POST"])
        def passwordChangeForm():
            """

            :return:
            """
            if request.args.get("num") is not None and request.args.get("new_password") is not None:
                num = request.args.get("num")
                new_password = request.args.get("new_password")
                user_data = db_worker.User().get(num=num, data_format="obj")
                if isinstance(user_data, UserStorage) and str(user_data.active_num) == num:
                    user_hash = generate_token(user_data.user_id, new_password)
                    user_data.token = user_hash
                    user_data.save()
                    return render("info.html", message="password updated.Please, log in system")

        # logging out
        @self.server.route("/auth/dislog", methods=["GET"])
        def dislog():
            resp = redirect("/")
            resp.set_cookie("token", "Null")
            return resp

        @self.server.route("/api/user/CheckToken", methods=["POST"])
        def CheckToken():
            jwt_token = request.json["JWToken"]
            if decode_token(jwt_token):
                return [1]
            else:
                return [0]

        @self.server.route("/api/user/generate_token", methods=["POST"])
        def GenerateToken():
            if request.method == "POST":
                user = request.json["user"]
                password = request.json["password"]

                user_hash = generate_token(user, password)

                user_data = db_worker.User().get(token=user_hash, data_format="obj")
                logger.info(user_data)

                if type(user_data) is not int:
                    jwt_token = create_access_token(identity=user_data.user_id)
                    return {"JWToken": jwt_token}, 201
                else:
                    return "400", 400
            else:
                return "400", 400

        @self.server.route("/api/user", methods=["GET", "POST", "CREATE", "DELETE"])
        def MisatoKForever():
            if request.method == "GET":
                jwt_token = request.args.get("JWToken")
                user_id = request.args.get("UserId")
                if jwt_token is not None:
                    if decode_token(jwt_token):
                        user_id = decode_token(jwt_token)["sub"]
                        data = db_worker.User().get(user=user_id, data_format="json")
                        if type(data) is not int:
                            return data
                        else:
                            return "404", 404
                    else:
                        return "400", 400
                elif user_id is not None:
                    data = db_worker.User().get(user=user_id, data_format="json")
                    if type(data) is not int:
                        return data
                    else:
                        return "404", 404

                else:
                    return "400", 400

            elif request.method == "POST":
                request_data = request.json

                if request_data:

                    email = request_data["email"]
                    user_id = request_data["UserId"]
                    password = request_data["password"]
                    citate = request_data["citate"]

                    user_data = db_worker.User().get(user=user_id, data_format="ojb")
                    if user_data == 0:

                        u = db_worker.User().create(password=password, email=email, user=user_id, is_admin=0,
                                                    is_banned=0, logo_path="default.png", citate=citate,
                                                    data_format="obj")
                        mail_worker.SendMessage(
                            TargetMail=email,
                            text="""Hello! Go to this link http://{}:{}/ActivateEmail?num={} 
                        to activate your account""".format(host, app, u.active_num),
                            theme="account activating"
                        )
                        return "201", 201
                    else:
                        return "400", 400
                else:
                    return "400", 400
            elif request.method == "DELETE":
                request_data = request.json
                user0 = decode_token(request_data["JWToken"])["sub"]
                user0 = db_worker.User().get(user=user0, data_format="obj")
                user = request_data["user"]
                if user0 == user or user0.IsAdmin:
                    db_worker.User().delete(user=user)
                    return "200,200"
                else:
                    return "403", 403

        @self.server.route("/api/user/change/user", methods=["POST"])
        def UserChange():

            data = request.json

            user_id_from_token = decode_token(data["token"])["sub"]
            citate = data["citate"]

            user_data = db_worker.User().get(user=user_id_from_token, data_format="obj")
            logger.info(user_data.__dict__)

            if user_data.user_id != "":

                # if citate is not set, we are changing password and user id
                if citate == "":

                    password = data["password"]
                    new_user_id = data['NewUserId']

                    # creating new hash from user and password
                    user_data.user_id = new_user_id
                    user_data.token = generate_token(new_user_id, password)
                    user_data.save()

                    # change all topics, create by user
                    all_user_topic = db_worker.topic().all(data_format="obj")
                    if not isinstance(all_user_topic, collections.abc.Iterable):
                        all_user_topic.author = new_user_id
                        all_user_topic.save()

                    else:
                        for _ in all_user_topic:
                            if _.author == user_id_from_token:
                                _.author = new_user_id
                                _.save()

                    # change all messages, create by user
                    all_user_msg = db_worker.Message().all(data_format="obj")
                    if not isinstance(all_user_msg, collections.abc.Iterable):
                        all_user_topic.author = new_user_id

                    else:
                        for msg in all_user_msg:
                            if msg.author == user_id_from_token:
                                msg.author = new_user_id
                                msg.save()

                    return "201", 201

                else:
                    user_data.citate = citate
                    user_data.save()
                    return "201", 201

        @self.server.route("/api/user/change/admin", methods=["POST"])
        def AdminUserChange():

            try:

                data = request.json

                adminuser_id = decode_token(data['AdminToken'])["sub"]
                user_id = data['UserId']
                is_banned = data["IsBanned"]
                is_admin = data["IsAdmin"]

                admin_user_data = db_worker.User().get(user=adminuser_id, data_format="obj")
                simple_user_data = db_worker.User().get(user=user_id, data_format="obj")
                if admin_user_data.IsAdmin == 1:

                    if simple_user_data.user_id != "" and simple_user_data.user_id != self.AdminUser:
                        simple_user_data.IsBanned = is_banned
                        simple_user_data.IsAdmin = is_admin
                        simple_user_data.save()
                        return "201", 201
                    else:
                        return "404", 404

                else:
                    return "403", 403

            except IndexError or KeyError:

                return "400", 400

        @self.server.route("/ActivateEmail")
        def ActivateEmail():
            num = request.args.get('num')

            user_data = db_worker.User().get(num=num, data_format="obj")

            if user_data.IsActivated == 1:
                return render("info.html", message="account is activated now")

            user_data.IsActivated = 1
            user_data.active_num = 0

            user_data.save()

            mail_worker.SendMessage(user_data.email, "Congratulations! Account is activated!", "account status")

            return render("info.html", message="Account is activated")

        @self.server.route("/api/user/all")
        def UserAll():
            if type(db_worker.User().all(data_format="json")) != list:
                return [db_worker.User().all(data_format="json")]

            return db_worker.User().all(data_format="json")

        @self.server.route("/api/topic", methods=["GET", "POST", "DELETE", "PATCH"])
        def api_topic():
            if request.method == "GET":
                topic_id = request.args.get("TopicId")
                return db_worker.topic().get(topic_id=topic_id, data_format='json')
            elif request.method == "POST":
                request_data = request.get_json()
                user_id = decode_token(request_data["token"])["sub"]

                if request_data and user_id:
                    theme = request_data["theme"]
                    about = request_data["about"]
                    is_protected = request_data["is_protected"]

                    topic_created = db_worker.topic().create(theme, user_id, about, is_protected, data_format="obj")
                    return db_worker.topic().get(topic_id=topic_created.topic_id, data_format="json")

                else:
                    return 400

            elif request.method == "DELETE":
                request_data = request.get_json()

                topic_id = request_data["TopicId"]
                user_id = decode_token(request_data["token"])["sub"]

                user_data = db_worker.User().get(user=user_id, data_format="obj")
                topic_data = db_worker.topic().get(topic_id=topic_id, data_format="obj")
                if topic_data.author == user_id or user_data.IsAdmin == 1:
                    db_worker.topic().delete(topic_id=topic_id)
                    return "200", 200
                else:
                    return "403", 403

            elif request.method == "PATCH":

                # try:

                request_data = request.get_json()

                user_id = decode_token(request_data["token"])["sub"]
                topic_id = request_data["TopicId"]

                _ = db_worker.topic().get(topic_id=topic_id, data_format="obj")
                user = db_worker.User().get(user=user_id, data_format="obj")
                if _.author == user_id or user.IsAdmin == 1:
                    _.theme = request_data["theme"]
                    _.about = request_data["about"]
                    _.save()

                    return "201", 201

                # except:
                #
                #     return "400", 400

        @self.server.route("/api/topic/all")
        def all_topic():
            if type(db_worker.topic().all(data_format="json")) != list:
                return [db_worker.topic().all(data_format="json")]
            return db_worker.topic().all(data_format="json")

        @self.server.route("/api/messages", methods=["GET", "POST", "DELETE", "PATCH"])
        def ApiMessage():
            if request.method == "GET":
                topic_id = request.args.get("TopicId")
                message_id = request.args.get("MessageId")
                logger.info(topic_id)
                logger.info(message_id)
                if topic_id is not None:
                    if type(db_worker.Message().get(topic_id=topic_id, data_format='json')) != list:
                        return [db_worker.Message().get(topic_id=topic_id, data_format='json')]
                    return db_worker.Message().get(topic_id=topic_id, data_format='json')
                elif message_id is not None:
                    message_data = db_worker.Message().get(message_id=message_id, data_format="json")
                    if message_data is not []:
                        return message_data, 200
                    return '404', 404

            elif request.method == "POST":
                request_data = request.get_json()
                self.logger.info(text=request_data)
                user_id = decode_token(request_data["token"])["sub"]
                topic_data = db_worker.topic().get(topic_id=request_data["TopicId"], data_format="obj")
                if not topic_data:
                    return "404", 404
                if request_data and user_id and topic_data.protected != 1:
                    topic_id = request_data["TopicId"]
                    text = request_data["text"]
                    new_message = db_worker.Message().create(topic_id, user_id, text, data_format="json")
                    return new_message, 201
                elif topic_data.author == user_id and topic_data.protected == 1:
                    topic_id = request_data["TopicId"]
                    text = request_data["text"]
                    new_message = db_worker.Message().create(topic_id, user_id, text, data_format="json")
                    return new_message, 201
                else:
                    return "403", 403
            elif request.method == "DELETE":
                request_data = request.get_json()

                message_id = request_data["MessageId"]
                user_id = decode_token(request_data["token"])["sub"]

                user_data = db_worker.User().get(user=user_id, data_format='obj')
                msg_data = db_worker.Message().get(message_id=message_id, data_format='obj')
                if msg_data.author == user_id or user_data.IsAdmin == 1:
                    db_worker.Message().delete(message_id=message_id)
                    return "200", 201
                else:
                    return "403", 403

            elif request.method == "PATCH":

                request_data = request.get_json()

                text = request_data['text']
                message_id = request_data["MsgId"]
                user_id = decode_token(request_data["token"])["sub"]

                msg_data = db_worker.Message().get(message_id=message_id, data_format="obj")

                if user_id == msg_data.author or user_id == admin_user:
                    msg_data.text = text
                    msg_data.save()

                    return "201", 201

                return "403", 403

        @self.server.route("/api/messages/all")
        def MessageAll():
            return db_worker.Message().all(data_format="json")

        @self.server.route("/api/GetForumName")
        def forum_nameGet():
            return {"forum_name": self.forum_name}

        @self.server.route("/UserPage")
        def PageUser():
            return render_template("user_page.html")

        @self.server.route("/moderate/users")
        def UsersModerate():
            user_id = decode_token(request.cookies.get("token"))["sub"]
            user_data = db_worker.User().get(user=user_id, data_format="obj")
            if user_data.IsAdmin == 1:
                return render("user_moderation.html")
            else:
                return render_template("info.html", message="HTTP 403. Access denied")

        @self.server.route("/FAQ")
        def FuYo():
            return render("faq.html")

        socket_io.run(self.server, host=host, port=port, debug=is_debug, allow_unsafe_werkzeug=True)
