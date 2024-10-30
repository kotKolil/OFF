<div style="text-align:center;padding:0px;margin:0px;"><img src = "assets/name.png" style = "width:100vw;padding:0px;margin:0px;" ></div>

<p>

### Description

OFF -  is free, open-source , web-forum engine on python 3.* on backend and JS on client-side,  with flexible settings, updating topic in real-time and system of moderation. It's easy in installing, using and moderating. This forum engine uses JWT-tokens to secure user data.
This forum uses a class system to make the project safe and easy to maintain. All parts of the application (logger, database, business logic) are implemented as classes.

</p>

### Classes

#### server

This class is implemention of Flask app, which serving requests.
Variables in `__init__` function, that class use:

| variable name | type of variable                                | purpose                                                                                                                            |
| ------------- | ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| ClassLogger   | ``class txt_logger()`` ``class json_logger() `` | defining class, that will log information                                                                                          |
| DBWorker      | ``class DB()``                                  | defining class, wich gives acess to tables in DB                                                                                   |
| port          | ``int``                                         | sets number of port, where will work flask app                                                                                     |
| IsDebug       | ``bool``                                        | setting mode of flask app. If IsDebug ``True`` server will show error traceback on user side and reloads app when code is changing |
| AdminUser     | ``str``                                         | setting UserId of forum admin                                                                                                      |
| AdminName     | ``str``                                         | setting psevodnim of forum admin                                                                                                   |
| AdminPassword | ``str``                                         | setting forum admin password                                                                                                       |
| AdminCitate   | ``str``                                         | setting forum admin citate                                                                                                         |
| AdminLogoPath | ``str``                                         | setting path to forum admin logo                                                                                                   |
| ForumName     | ``str``                                         | setting forum name, that will display on forum pages                                                                               |
| MailWorker    | ``class MailClient()``                          | setting class, via wich we will sends e-mails                                                                                      |
| AppSecretKey  | ``str``                                         | setting flask app secret key                                                                                                       |

#### URI Entripoints of Flask App in server class

| URI                  | HTTP methods           | name of view function | purpose                                                                                     | format of json to API                                                                                                                                                                                                                                                                                                                                                      |
| -------------------- | ---------------------- | --------------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| /static/path:path    | GET                    | static_files          | serving static files, like CSS, JS or font files on /static entrypoint                      |                                                                                                                                                                                                                                                                                                                                                                            |
| /media/path:path     | GET                    | media_files           | serving media files from server, like users logos                                           |                                                                                                                                                                                                                                                                                                                                                                            |
| /                    | GET                    | index                 | returns main page of forum                                                                  |                                                                                                                                                                                                                                                                                                                                                                            |
| /topic               | GET                    | topic                 | return html content of topic page                                                           |                                                                                                                                                                                                                                                                                                                                                                            |
| /topic/create        | GET POST               | TopicCreate           | return page with topic creating form and servs POST request from submitted form             |                                                                                                                                                                                                                                                                                                                                                                            |
| /auth/reg            | GET POST               | reg                   | return page with registration form and servs POST request from submitted form               |                                                                                                                                                                                                                                                                                                                                                                            |
| auth/log             | GET POST               | log                   | return page with logging form and servs POST request from submitted form                    |                                                                                                                                                                                                                                                                                                                                                                            |
| /auth/dislog         | GET                    | dislog                | logging out current user (setting session token to Null)                                    |                                                                                                                                                                                                                                                                                                                                                                            |
| /api/user/ChangeLogo | POST                   | ChangeLogo            | changing logo of user from recieved token                                                   | 'logo' - file of new user logo, must be in request files,"token" - field of json, where sets user session token                                                                                                                                                                                                                                                      |
| /api/user/CheckToken | POST                   | CheckToken            | check validness of user session token                                                       | "JWToken" - field of json, where sets user session token, which we want to check                                                                                                                                                                                                                                                                                           |
| /api/user            | GET POST DELETE CREATE | MisatoKForever        | provides an API for users                                                                   | GET method - "JWToken" request arg set JWToken, on which we return user, "UserId" - request arg set user id wich data we want to get,CREATE - creating user - {"email": new user email, "UserId" - new user id, "password" -  new user password, "citate" - new user citate }, DELETE - delete user - {"JWToken" - session token of user, wich we want delete} |
| /ActivateEmail       | GET                    | ActivateEmail         | get num from request arg 'num' and, if it equal to user activate num, activate user account |                                                                                                                                                                                                                                                                                                                                                                            |
| /api/user/all        | GET                    | UserAll               | return list of forum users                                                                  |                                                                                                                                                                                                                                                                                                                                                                            |
| /api/topic           | GET POST DELETE        | ApiTopic              | provide API for topics                                                                      | GET - return topic data from request arg "TopicId",POST - {"token": user session token, "theme" - new topic theme, "about" - new topic about,DELETE - deleting topic - {"TopicId" - topic id which we want delete, "token" - user session token, admin of forum or creator of topic}                                                                           |
| /api/topic/all       | GET                    | AllTopic              | return list of topic on forum                                                               |                                                                                                                                                                                                                                                                                                                                                                            |
| /api/messages        | GET POST DELETE        | ApiMessage            | provide api to messages                                                                     | GET - return all messages of topic which id set in request arg "TopicId", POST - creating new message - {"token":user session token, "TopicId": id of topic, where creating message, "text": text of new message, DELETE -  deleting message - {"MessageId":id of message, wich we want create, "token": session token of message creator or forum admin}      |
| /api/messages/all    | GET                    | MessageAll            | return all messages from topic                                                              |                                                                                                                                                                                                                                                                                                                                                                            |
| /api/GetForumName    | GET                    | ForumNameGet          | return name of forum
|/UserPage|GET|PageUser|return html content of user page|
|/moderate/users|GET|UsersModerate|return html content of moderation page||

#### DB

This class is implementing DB and provide functions wich provide acess to tables. When ```class DB()``` is initialising, they use ```SQLite3``` or ```postgres``` to work different types of DB, setted in variable DBType in ```__init__``` function of ```class User()``` function in DB class. By variables of ```__init__``` DBType, path, host, port, name, user, password you can set params of connection to your DB

##### functions of ```class User()```

this function provide acess to user table

| function | description | params |
| --- | --- | --- |
| get |this function return user data in 1 type of format that set in format variable, user can be matched by setting variables   | user, password - getting user by him user and pasword, token - get user from his unique token made by hash from user and password, num - getting user  by his activating num  |
| all | this function return all users on forum |  |
|create| function, via that we creating new user| passowrd - str, user - str, is_admin - str, is_banned - str, logo_path - str, citate - str, format - set type of output data, see documentation next about ```class UserStorage()``` |

##### type of output data from functions ```DBClass.User()```

By format variable in function methods we can set format of output data from ```class User()```. If your set "json" in this variable, function will return dict, where keys is table fieds in DB, and values - is values of table fields in DB. If you set "obj", class return object of ```class UserStorage()```, where you can get data like this: <p>

```
UserData = DBClass.User().get(user="Treska",password = "1337")
UserId = UserData.UserId
```

You can change values of table field like here:

```
UserData = DBClass.User().get(user="Treska", password = "1337")
UserData.UserId = "tomfox"
UserData.save()
```

##### functions of ```DBClass.Topic()```

| function | description | params |
| --- | --- | --- |
| get  |  we are getting data about topic from DB | TopicId - str, id of topic that we want get, format - format of ouput data, "obj" or "json", it works like same variable in ```class User()```  |
| all | return all topic in forum  |  |
|delete | we are deleting data about topic from DB | TopicId - str, id of topic that we want delete |
|create| we are creating topic in DB| theme - string, theme of new topic, author - string, user id of author new topic, about - about of new topic, format - format of output data, work like same variable in ```class User()```|

##### function of ```DBClass.Message```



