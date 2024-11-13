<div style="text-align:center;padding:0px;margin:0px;"><img src = "assets/name.png" style = "width:100vw;padding:0px;margin:0px;" ></div>
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)  ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)   ![Static Badge](https://img.shields.io/badge/by_kotkolil-%D0%BF%D0%B8%D1%88%D0%B3%D0%BA%D1%89%D0%B0%D1%82%D0%BC%D0%B7%D1%8F?link=https%3A%2F%2Fgithub.com%2FkotKolil%2FkotKolil) <a href="https://github.com/your-username/your-repository">
  <img alt="Open Source" src="https://img.shields.io/badge/Open%20Source-blueviolet?style=flat-square">
  <img alt="Project" src="https://img.shields.io/badge/Project-lightgreen?style=flat-square">
</a>


# Contents
[TOC]



# Description

OFF -  is free, open-source , web-forum engine on python 3.* on backend and JS on client-side,  with flexible settings, updating topic in real-time and system of moderation. It's easy in installing, using and moderating. This forum engine uses JWT-tokens to secure user data.
This forum uses a class system to make the project safe and easy to maintain. All parts of the application (logger, database, business logic) are implemented as classes.

# Starting and configuring an app
## Starting

1. You need to download latest version of python from www.python.org/downloads

2. Run downloaded file

3. during python installation, it is common to check the box "add python to path".

4. When python is installed, open terminal or shell

6. in terminal, go to root directory of OFF project

7. in terminal run this command to install libraries for app: 

   ```
   pip install -r r.txt
   ```

   

8. in terminal run this command  to run the app:

   ​	```python main.py```

   congratulations, you have launched the application

#### variable in config.py types

in config.py 3 types of variable: integer, string and boolean

| variable type | values  | example |
| ---- | ---- | ---- |
| str | characters(A-Z, a-z), numbers(0-9) and special characters    | ``"lorum ipsum dolor sit ammet"`` |
| bool | True or False | ``True``, ``False`` |
| int | zero, positive or negative whole numbers without a fractional part and having unlimited precision | ``1337`` ``-10`` ``13.7`` |

## configuring app

### overview

to configure up, you may change values in config.py. All necessary variables, that app uses, defined in this file. Variable defined in python syntax or in  environment variable's. If syntax will be wrong, app doesn't start

### list of variables in environment or in config.py, that you can configure

|name of variable|standart value|purpose| variable type|
| ---- | ---- | ---- |----|
| logger_type | console | Sets type of logger in app | string |
| name_of_file | "" (empty string) | sets name of file, where will be store logging data |string|
| DBtype | "" (empty string) | sets type of db, that using in app;  may be sets "postgresql" or "sqlite3". On empty strings, app will set DB type "sqlite3" and name of DB "main.db" |string|
| DBport | 5432 | sets port of gost, where DB is placed |integer|
| DBpassword | "" (empty string) | set DB password, where app will connect |string|
| DBuser | "" empty string | sets user of DB, where app will connect |string|
| DBname | "" empty string | sets name of DB, where app will connect |string|
| DBhost | "" empty string | sets host, where DB is placed |string|
| ForumName | "Awesome Forum" | set name of forum, thats will displayed on pages |string|
| IsDebug | True | on or off debug mode of app |Boolean|
| AdminUser | "admin" | sets name of forum admin account |string|
| AdminPassword | "1234567890" | sets password of forum admin account |string|
| AdminName | "anomin" | sets admin nickname, that will displays instead of AdminUser |string|
|AdminCitate|""|sets citate, that will display under admin messages|string|
|AdminLogoPath|"admin.png"|sets name of file, placed on "/media", thats will display on admin's accounts|string|
|MailSite|""|sets host address of smpt server, that will be mail worker in app sends request|string|
|MailPort|""|sets port of smpt server, that will be mail worker in app sends request|string|
|MailLogin|""|sets login of smpt server user, that will be mail worker in  app sends requests|string|
|MailPassword|""|sets  password of smpt server user, that will be mail worker in app send requests|string|
|AppSecretKey|""|sets variable ``'SECRET_KEY'`` in flask app|string|
|JwtSecretKey|""|sets JWT tokens secret key|string|
|APPport|8000|sets port of app, where it will be recieve|integer|
|APPhost|"0.0.0.0"|sets host , will app will be placed|string|
|||||

​	

## Starting app with Docker

to run app with Docker, follow this instruction:

1.  Go to root directory of OFF project
2. Run in shell command ``sudo docker build OFF ..``
3. Run in shell command ``sudo docker run OFF``

# How to use forum

## How log in system

To log in system, you need to do this things:

1.  Go to /auth/log or click on "log in" in bottom

2. Enter you login and password

3. Click on button "log in" under input fields

4. If all data correct, you will be replaced to main page

5. If you entered wrong data, will spawn text "Incorrect user or password". You must return to step number 2 and enter right data

   

## How register in system

To register in system, you need to do this things:

1. Go to /auth/reg or click on "log in" in bottom "reg in"

2. Enter you data in form

3. Click on "reg in"

4. go to email, that your enter in form

5. You must be recieve  a letter with link, that will activate your account. Go to it

   Congrulations! You are registred on forum

   

## How create topic on forum

To create topic on forum, you need to do this things:

1. You must be logged in system. Check, do you authorised on forum

2. Click to create topic on main page of Forum or go to /topic/create

3. If you get error "Token has expired", please log in system

4. Fill form
5. Field Is Secured disable sending message in your topic from other users
6. Click to button

   

Congrulations! You are created topic on forum

## How send message on forum

To send message on forum, you need to do this things:

1. You must be logged in system. Check, do you authorised on forum

2. Go to topic, in that you want send message

3. Type your message in form on top

4. Click on button  near

5. If message not send, you are not logged in. Please, log in 

   Congrulations! You are created topic on forum

## How delete message or topic

to delete topic or message, you can use buttons near message form in topic or button in messsage

​	If you not logged in or not moderator, you can`t delete messsage or topic

## How to get on your personal page

to go on your personal page, you may click on link personal page on toolbar in bottom of page
On you personal page displayed your info and you can send message or make a posts on a "Wall", how
in topic page

## How to reply to message in topic

To reply to message in topic, you can use button "reply" in message block. After your click button, html content of that message will be in text of your answer 

## How use moderation page

**moderators only!**

to moderate users on forum, you must go to /moderate/users. If you not moderator, you will get 403 HTTP error. But, if you are have moderator status, you will see this page:

![moderate](C:\Users\Treska\Documents\projects\OFF\assets\moderate.PNG)

to get user, you must enter his id in input field and press on  button "get user". Page will change:

![moderateuser](C:\Users\Treska\Documents\projects\OFF\assets\moderateuser.PNG)

On page will display all info about user. You can change his rights via checkboxes.  When you finish, press on button "save info".  Info will send to forum, and if everything is all,  message display and user data updates:

![moderatemessage](C:\Users\Treska\Documents\projects\OFF\assets\moderatemessage.PNG)

For example, i moved user to moderator

![image-20241113175758303](C:\Users\Treska\AppData\Roaming\Typora\typora-user-images\image-20241113175758303.png)

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


| URI                   | HTTP methods           | name of view function | purpose                                                      | format of json to API                                        |
| --------------------- | ---------------------- | --------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| /static/path:path     | GET                    | static_files          | serving static files, like CSS, JS or font files on /static entrypoint |                                                              |
| /media/path:path      | GET                    | media_files           | serving media files from server, like users logos            |                                                              |
| /                     | GET                    | index                 | returns main page of forum                                   |                                                              |
| /topic                | GET                    | topic                 | return html content of topic page                            |                                                              |
| /topic/create         | GET POST               | TopicCreate           | return page with topic creating form and servs POST request from submitted form |                                                              |
| /auth/reg             | GET POST               | reg                   | return page with registration form and servs POST request from submitted form |                                                              |
| auth/log              | GET POST               | log                   | return page with logging form and servs POST request from submitted form |                                                              |
| /auth/dislog          | GET                    | dislog                | logging out current user (setting session token to Null)     |                                                              |
| /api/user/ChangeLogo  | POST                   | ChangeLogo            | changing logo of user from recieved token                    | 'logo' - file of new user logo, must be in request files,"token" - field of json, where sets user session token |
| /api/user/CheckToken  | POST                   | CheckToken            | check validness of user session token                        | "JWToken" - field of json, where sets user session token, which we want to check |
| /api/user             | GET POST DELETE CREATE | MisatoKForever        | provides an API for users                                    | GET method - "JWToken" request arg set JWToken, on which we return user, "UserId" - request arg set user id wich data we want to get,<BR>CREATE - creating user - {"email": new user email, "UserId" - new user id, "password" -  new user password, "citate" - new user citate }, <BR>DELETE - delete user - {"JWToken" - session token of user, wich we want delete} |
| /ActivateEmail        | GET                    | ActivateEmail         | get num from request arg 'num' and, if it equal to user activate num, activate user account |                                                              |
| /api/user/all         | GET                    | UserAll               | return list of forum users                                   |                                                              |
| /api/topic            | GET POST DELETE PATCH  | ApiTopic              | provide API for topics                                       | GET - return topic data from request arg "TopicId",<br>POST - {"token": user session token, "theme" - new topic theme, "about" - new topic about,<br>DELETE - deleting topic - {"TopicId" - topic id which we want delete, "token" - user session token, admin of forum or creator of topic}, <br>PATCH - {"UserToken" - auth token of topic author or admin, "TopicId" - id of topic, that you want to change,  "TopicTheme" - new theme of topic, "TopicAbout" - new about of topic } |
| /api/topic/all        | GET                    | AllTopic              | return list of topic on forum                                |                                                              |
| /api/messages         | GET POST DELETE        | ApiMessage            | provide api to messages                                      | GET - return all messages of topic which id set in request arg "TopicId",  <br>POST - creating new message - {"token":user session token, "TopicId": id of topic, where creating message, "text": text of new message, <br>DELETE -  deleting message - {"MessageId":id of message, wich we want create, "token": session token of message creator or forum admin},<br> PATCH -  {"text" - new text of message,  "MsgId" -  id of message, "UserToken" - auth token of message author or admin} |
| /api/messages/all     | GET                    | MessageAll            | return all messages from topic                               |                                                              |
| /api/GetForumName     | GET                    | ForumNameGet          | return name of forum                                         |                                                              |
| /UserPage             | GET                    | PageUser              | return html content of user page                             |                                                              |
| /moderate/users       | GET                    | UsersModerate         | return html content of moderation page                       |                                                              |
| /api/user/change/user | PATCH                  | UserChange            | change user password and id or quote<br>To change qoute, set qoute and send<br>To change User Id  and password, set quote = "" and set new  user and password | to change quote - {"citate": new quote}<br>to change user and password - {"user": new user id, "NewPassword" : new password", citate:""} |

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

# Structure of project

Structure have this structure (opened in PyCharm Community Edition 2023.3.5):



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

