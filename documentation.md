<div style="text-align:center;padding:0px;margin:0px;"><img src = "assets/name.png" style = "width:100vw;padding:0px;margin:0px;" ></div>


# Contents
[TOC]



# Description

OFF -  is free, open-source , web-forum engine on python 3.* on backend and JS on client-side,  with flexible settings, updating topic in real-time and system of moderation. It's easy in installing, using and moderating. This forum engine uses JWT-tokens to secure user data.
This forum uses a class system to make the project safe and easy to maintain. All parts of the application (logger, database, business logic) are implemented as classes.

# Starting and setting up app
## Starting

1. You need to download latest version of python from www.python.org/downloads

2. Run downoladed file

3. during python installation, it is common to check the box "add python to path".

4. When python is installed 

5.  open terminal or shell

6. in terminal, go to root directory of OFF project

7. in terminal run this command to install libraries for app: 

   ```
   pip install -r r.txt
   ```

   

8. in terminal run this command  to run the app:

   ​	```python main.py```

   congratulations, you have launched the application

# Classes

## server

### description

This class is implementation of Flask app, which serving requests.

### variables in ``__init__`` function



Variables in `__init__` function, that class uses:


| variable name | type of variable                                | purpose                                                      |
| ------------- | ----------------------------------------------- | ------------------------------------------------------------ |
| ClassLogger   | ``class txt_logger()`` ``class json_logger() `` | defining class, that will log information                    |
| DBWorker      | ``class DB()``                                  | defining class, wich gives acess to tables in DB             |
| port          | ``int``                                         | sets number of port, where will work flask app               |
| IsDebug       | ``bool``                                        | setting mode of flask app. If IsDebug``True`` server will show error traceback on user side and reloads app when code is changing |
| AdminUser     | ``str``                                         | setting UserId of forum admin                                |
| AdminName     | ``str``                                         | setting psevodnim of forum admin                             |
| AdminPassword | ``str``                                         | setting forum admin password                                 |
| AdminCitate   | ``str``                                         | setting forum admin citate                                   |
| AdminLogoPath | ``str``                                         | setting path to forum admin logo                             |
| ForumName     | ``str``                                         | setting forum name, that will display on forum pages         |
| MailWorker    | ``class MailClient()``                          | setting class, via which we will sends e-mails               |
| AppSecretKey  | ``str``                                         | setting flask app secret key                                 |

### URI Entripoints of Flask App in server class


| URI                  | HTTP methods           | name of view function | purpose                                                      | format of json to API                                        |
| -------------------- | ---------------------- | --------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| /static/path:path    | GET                    | static_files          | serving static files, like CSS, JS or font files on /static entrypoint |                                                              |
| /media/path:path     | GET                    | media_files           | serving media files from server, like users logos            |                                                              |
| /                    | GET                    | index                 | returns main page of forum                                   |                                                              |
| /topic               | GET                    | topic                 | return html content of topic page                            |                                                              |
| /topic/create        | GET POST               | TopicCreate           | return page with topic creating form and servs POST request from submitted form |                                                              |
| /auth/reg            | GET POST               | reg                   | return page with registration form and servs POST request from submitted form |                                                              |
| auth/log             | GET POST               | log                   | return page with logging form and servs POST request from submitted form |                                                              |
| /auth/dislog         | GET                    | dislog                | logging out current user (setting session token to Null)     |                                                              |
| /api/user/ChangeLogo | POST                   | ChangeLogo            | changing logo of user from recieved token                    | 'logo' - file of new user logo, must be in request files,"token" - field of json, where sets user session token |
| /api/user/CheckToken | POST                   | CheckToken            | check validness of user session token                        | "JWToken" - field of json, where sets user session token, which we want to check |
| /api/user            | GET POST DELETE CREATE | MisatoKForever        | provides an API for users                                    | GET method - "JWToken" request arg set JWToken, on which we return user, "UserId" - request arg set user id wich data we want to get,CREATE - creating user - {"email": new user email, "UserId" - new user id, "password" -  new user password, "citate" - new user citate }, DELETE - delete user - {"JWToken" - session token of user, wich we want delete} |
| /ActivateEmail       | GET                    | ActivateEmail         | get num from request arg 'num' and, if it equal to user activate num, activate user account |                                                              |
| /api/user/all        | GET                    | UserAll               | return list of forum users                                   |                                                              |
| /api/topic           | GET POST DELETE        | ApiTopic              | provide API for topics                                       | GET - return topic data from request arg "TopicId",POST - {"token": user session token, "theme" - new topic theme, "about" - new topic about,DELETE - deleting topic - {"TopicId" - topic id which we want delete, "token" - user session token, admin of forum or creator of topic} |
| /api/topic/all       | GET                    | AllTopic              | return list of topic on forum                                |                                                              |
| /api/messages        | GET POST DELETE        | ApiMessage            | provide api to messages                                      | GET - return all messages of topic which id set in request arg "TopicId", POST - creating new message - {"token":user session token, "TopicId": id of topic, where creating message, "text": text of new message, DELETE -  deleting message - {"MessageId":id of message, wich we want create, "token": session token of message creator or forum admin} |
| /api/messages/all    | GET                    | MessageAll            | return all messages from topic                               |                                                              |
| /api/GetForumName    | GET                    | ForumNameGet          | return name of forum                                         |                                                              |
| /UserPage            | GET                    | PageUser              | return html content of user page                             |                                                              |
| /moderate/users      | GET                    | UsersModerate         | return html content of moderation page                       |                                                              |

## DB

### description

This class is implementing DB and provide functions which provide access to tables. When class DB() is initialising, they use ```SQLite3``` or ```postgres``` to work different types of DB, settled in variable DBType in ```__init__``` function of ```class User()``` function in DB class. By variables of ```__init__``` DBType, path, host, port, name, user, password you can set params of connection to your DB

###  ```User()``` function

#### description

this function giving access to User table in DB. 

Definition:

```python
DBClass = DB(DBType = "sqlite3", path = "main.db")
UserClass = DBClass.User()
```

#### functions


| function | description                                                                                                              | params                                                                                                                                                                              |
| -------- | ------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| get      | this function return user data in 1 type of format that set in format variable, user can be matched by setting variables | user, password - getting user by him user and pasword, token - get user from his unique token made by hash from user and password, num - getting user  by his activating num        |
| all      | this function return all users on forum                                                                                  |                                                                                                                                                                                     |
| create   | function, via that we creating new user                                                                                  | passowrd - str, user - str, is_admin - str, is_banned - str, logo_path - str, citate - str, format - set type of output data, see documentation next about```class UserStorage()``` |

#### type of output data

By format variable in function methods we can set format of output data from ```class User()```. If your set "json" in this variable, function will return dict, where keys is table fieds in DB, and values - is values of table fields in DB. If you set "obj", class return object of ```class UserStorage()```, where you can get data like this: <p>

```python
UserData = DBClass.User().get(user="Treska",password = "1337")
UserId = UserData.UserId
```

#### changing data

Your can change data via changing class variables, like here:

</p>

```python
UserData = DBClass.User().get(user="Treska", password = "1337")
UserData.UserId = "tomfox"
UserData.save()
```

### ```Topic()``` function

#### description

this function provide access to topic table in DB. Definition:

```python
Db = DB()
Topic = Db.Topic()
```

#### functions


| function | description                              | params                                                                                                                                                                                     |
| -------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| get      | we are getting data about topic from DB  | TopicId - str, id of topic that we want get, format - format of ouput data, "obj" or "json", it works like same variable in```class User()```                                              |
| all      | return all topic in forum                |                                                                                                                                                                                            |
| delete   | we are deleting data about topic from DB | TopicId - str, id of topic that we want delete                                                                                                                                             |
| create   | we are creating topic in DB              | theme - string, theme of new topic, author - string, user id of author new topic, about - about of new topic, format - format of output data, work like same variable in```class User()``` |

#### type of output data

``Topic()`` return data like ```User()```. You also can set type of data in "format" variable in ```_init()__```   (```"json"```, dictation  or ```"obj"```, object of ```class TopicStorage()``` ).

Examples:

```python
DBClass = DB(DBType = "sqlite3", path = "main.db")
TopicTable = DBWorker.Topic()
#getting data
TopicDataObj = TopicTable(TopicId = "1337foobazz", format = "obj")
print(TopicDataObj.theme)
TopicDataJson = TopicTable(TopicId = "1337foobazz", format = "json")
print(TopicDataJson["theme"])
```

#### changing data 

You can change data about topic via class variables, like here:

```python
DBClass = DB(DBType = "sqlite3", path = "main.db")
TopicTable = DBWorker.Topic()
#getting data
TopicDataObj = TopicTable(TopicId = "1337foobazz", format = "obj")
#changing data
TopicDataObj.theme = "coocking"
TopicDataObj.save()
```

### ```Message()``` function

#### description

this function provide access to messages table in DB. Definition:

```python
DBClass = DB()
MessageClass = DBClass.Message()
```

#### functions

|   function     | description     |  params    |
| :----- | :--- | :--- |
| get | This function return all messages from topic or message. If you set TopicId, function will return list with all message from that topic. If your set MessageId, function will return data of single message | TopicId: string, MessageId: string, format: string |
| all | this function return all messages on forum | format:string                                                |
| delete | this function delete message, which id is given              | MessageId: string                                            |
| create | this function create message from given data. Return object of class ```MessageStorage()``` | TopicId:  string, author: string, text: string,  format: string |

#### type of output data

``Message()`` return data like ```User()```. You also can set type of data in "format" variable in ```_init()__```   (```"json"```, dictation  or ```"obj"```, object of ```class MessagesStorage()``` ).

example:

```python
#defining DB() obj
DBClass = DB(DBType = "sqlite3", path = "main.db")
#setting obj of Message()
MessageClass = DBClass.Message()
#getting single message as a obj
SingleMessageObj = MessageClass( MessageId = "1337foobazz", format = "obj")
print(SingleMessage.text)
#getting single message as a dictation(json)
SingleMessageJson = MessageClass( MessageId = "1337foobazz", format = "json")
print(SingleMessage["text"])
#getting all messages from topic like list of objects
ListOfMsgObj = MessageClass( TopicId = "1488foobar", format = "obj")
#iterating list
for MsgObj in ListOfMsgObj:
    print(MsgObj.text)
```

#### changing data

You can change data about topic via class variables, like here:

```python
#defining DB() obj
DBClass = DB(DBType = "sqlite3", path = "main.db")
#setting obj of Message()
MessageClass = DBClass.Message()
#getting single message as a obj
SingleMessageObj = MessageClass( MessageId = "1337foobazz", format = "obj")
#changing data
SingleMessageObj.text = "lorum ipsum dolor sit ammet consecutor"
SingleMessageObj.save()
```

## Logger

### description

```class Loger(object)``` uses for  logging data in console, txt or json files. He takes 2 arguments - logger_type and name_of_file.  In logger_type your can specify 3 type of string - "console", "text" and "json", otherwise you will get ```TypeError```. In name_of_file you set name of file, where debug data will be written. If your use console logger, you may not set  give name_of_file.

### examples

#### using console logger

```python
#creating logger object
LoggerWorker = Logger(logger_type="console")
#logging info
LoggerWorker.info("connection estabilished")
#logging warning
LoggerWorker.warning("invalid http headers")
#logging error
LoggerWorker.error("kernel panik")
```

console output:

![consoleoutput](C:\Users\Treska\Documents\projects\OFF\assets\consoleoutput.PNG)

also you can using console logger without defining object of  ```class Logger()```, from ```@staticmethod```, giving parameters text and level:

```python
#logging info
ConsoleLog.log(text = "connection estabilished", level = "info")
#logging warning
ConsoleLog.log(text = "invalid http headers", level = "warning")
#logging error
ConsoleLog.log(text = "kernel panik", level = "error")
```

#### using txt logger

```python
#creating logger object
LoggerWorker = Logger(logger_type="txt", filename = "logs.txt")
#logging info
LoggerWorker.info("connection estabilished")
#logging warning
LoggerWorker.warning("invalid http headers")
#logging error
LoggerWorker.error("kernel panik")
```

output in logs.txt

![txtoutput](C:\Users\Treska\Documents\projects\OFF\assets\txtoutput.PNG)

#### using json logger

```python
#creating logger object
LoggerWorker = Logger(logger_type="json", name_of_file = "logs")
#logging info
LoggerWorker.info("connection estabilished")
#logging warning
LoggerWorker.warning("invalid http headers")
#logging error
LoggerWorker.error("kernel panik")
```

output in log.json:

![jsonouput](C:\Users\Treska\Documents\projects\OFF\assets\jsonouput.PNG)

## tools.py

in this file defined some frequently used functions that uses in project

### ``allowed_file(filename)``

This function checking safety of  file extension. This function use ``ALLOWED_EXTENSIONS`` from settings.py

This function return ``True`` or ``False``

### ``generate_token(s1, s2)``

this function generate hash for 2 strings, using sha256 algorithm. In input you must give s1 and s2 - string, that  your want to make hash

In OFF this function uses for protecting password in DB

example:

```python
hash_string = generate_token(s1="treska", s2 = "1337")
print(hash_string) #d5ada9cf2348e84f5e7387844a9526fd859666cd8a8a95e479ccaac211633b3f
```

``get_current_time()``

this function return current time in string format YYYY-MM-DD HH:MM:SS

example:

![timeoutput](C:\Users\Treska\Documents\projects\OFF\assets\timeoutput.PNG)

### ``generate_id()``

this function uses for generate unique values for id of topics and message

usage:

![randomoutput](C:\Users\Treska\Documents\projects\OFF\assets\randomoutput.PNG)

# Client-side (Frontend)

## description

In the App uses system of rendering page via template with ninja2 and JS, which loads data from app API, JQuery to manipulate with DOM objects

## Base.html

This template is base for  pages in OFF. If you do not like theme of site, you can change base.html and main.css to change design

On this page via ``fetch()`` loads data about user. If user not logged in, sets "anonym" and standard logo of user. Also loads data about forum  and his current state

## info.html

this template rendering on base.html and uses for displays error or information

## static files

### /media

on this path saves user logotypes

### /static

on this path placed static files like JS scripts, CSS files and font files

#### main.js

in this file defined this functions for working with API:

##### ``getQueryParam()``

this function get argument name and return value of parameter with same name from URI 

##### ``getCookie()``

this function get cookie name and return value of cookie with same name

##### ``UserDataGet()``

This function is fast way to get data about user from his session token from app API. If variable token is invalid, function return ``"0"``

``IsLogged()``

this function is fast way to get about user state. If users`s session token invalid, function return  ``false``, if valid - ``true``

##### ``DeleteTopic()``

this function need 2 arguments - UserToken and TopicId. If user session token, given in UserToken is valid, topic with id as a TopicId deletes. If invalid, this function alert message "you do not have permissions to delete this topic".

``DeleteTopic()``

his function need 2 arguments - UserToken and MsgId. If user session token, given in UserToken is valid, message with id as a MsgId deletes. If invalid, this function alert message "you do not have permissions to delete this message".

