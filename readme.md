<div style="text-align:center;padding:0px;margin:0px;"><img src = "assets/name.png" style = "width:100vw;padding:0px;margin:0px;" ></div>



### Description

OFF -  is free, open-source , web-forum engine on python 3.* on backend and JS on client-side,  with flexible settings, updating topic in real-time and system of moderation. It's easy in installing, using and moderating. This forum engine uses JWT-tokens to secure user data.
This forum uses a class system to make the project safe and easy to maintain. All parts of the application (logger, database, business logic) are implemented as classes.


# Starting and setting up app

## Starting

1. You need to download latest version of python from www.python.org/downloads
2. Run downoladed file
3. during python installation, it is common to check the box "add python to path".
4. When python is installed
5. open terminal or shell
6. in terminal, go to root directory of OFF project
7. in terminal run this command to install libraries for app:


``pip install -r r.txt``
8. in terminal run this command  to run the app:

​	```python main.py```

congratulations, you have launched the application

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

   	```python main.py```

   congratulations, you have launched the application

#### variable in config.py types

in config.py 3 types of variable: integer, string and boolean

| variable type | values                                                       | example                           |
| ------------- | ------------------------------------------------------------ | --------------------------------- |
| str           | characters(A-Z, a-z), numbers(0-9) and special characters    | ``"lorum ipsum dolor sit ammet"`` |
| bool          | True or False                                                | ``True``, ``False``               |
| int           | zero, positive or negative whole numbers without a fractional part and having unlimited precision | ``1337`` ``-10`` ``13.7``         |

## configuring app

### overview

to configure up, you may change values in config.py. All necessary variables, that app uses, defined in this file. Variable defined in python syntax or in  environment variable's. If syntax will be wrong, app doesn't start

### list of variables in environment or in config.py, that you can configure

| name of variable | standart value    | purpose                                                      | variable type |
| ---------------- | ----------------- | ------------------------------------------------------------ | ------------- |
| logger_type      | console           | Sets type of logger in app                                   | string        |
| name_of_file     | "" (empty string) | sets name of file, where will be store logging data          | string        |
| DBtype           | "" (empty string) | sets type of db, that using in app;  may be sets "postgresql" or "sqlite3". On empty strings, app will set DB type "sqlite3" and name of DB "main.db" | string        |
| DBport           | 5432              | sets port of gost, where DB is placed                        | integer       |
| DBpassword       | "" (empty string) | set DB password, where app will connect                      | string        |
| DBuser           | "" empty string   | sets user of DB, where app will connect                      | string        |
| DBname           | "" empty string   | sets name of DB, where app will connect                      | string        |
| DBhost           | "" empty string   | sets host, where DB is placed                                | string        |
| ForumName        | "Awesome Forum"   | set name of forum, thats will displayed on pages             | string        |
| IsDebug          | True              | on or off debug mode of app                                  | Boolean       |
| AdminUser        | "admin"           | sets name of forum admin account                             | string        |
| AdminPassword    | "1234567890"      | sets password of forum admin account                         | string        |
| AdminName        | "anomin"          | sets admin nickname, that will displays instead of AdminUser | string        |
| AdminCitate      | ""                | sets citate, that will display under admin messages          | string        |
| AdminLogoPath    | "admin.png"       | sets name of file, placed on "/media", thats will display on admin's accounts | string        |
| MailSite         | ""                | sets host address of smpt server, that will be mail worker in app sends request | string        |
| MailPort         | ""                | sets port of smpt server, that will be mail worker in app sends request | string        |
| MailLogin        | ""                | sets login of smpt server user, that will be mail worker in  app sends requests | string        |
| MailPassword     | ""                | sets  password of smpt server user, that will be mail worker in app send requests | string        |
| AppSecretKey     | ""                | sets variable ``'SECRET_KEY'`` in flask app                  | string        |
| JwtSecretKey     | ""                | sets JWT tokens secret key                                   | string        |
| APPport          | 8000              | sets port of app, where it will be recieve                   | integer       |
| APPhost          | "0.0.0.0"         | sets host , will app will be placed                          | string        |
|                  |                   |                                                              |               |

​	

## Starting app with Docker

to run app with Docker, follow this instruction:

1.  Go to root directory of OFF project
2. Run in shell command ``sudo docker build OFF ..``
3. Run in shell command ``sudo docker run OFF``

If you hative some troubles with app,  read documention in documentation.md or on address , or create issue
