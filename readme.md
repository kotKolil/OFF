![name](documentation\assets\name.png)

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)  ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)   ![Static Badge](https://img.shields.io/badge/by_kotkolil-%D0%BF%D0%B8%D1%88%D0%B3%D0%BA%D1%89%D0%B0%D1%82%D0%BC%D0%B7%D1%8F?link=https%3A%2F%2Fgithub.com%2FkotKolil%2FkotKolil)

## Description

**OFF** is a free, open-source web forum engine built on Python 3.x for the backend and JavaScript for the  client-side. It features flexible settings, real-time topic updates, and a robust moderation system. This forum engine utilizes JWT tokens to  secure user data and employs a class-based architecture to ensure  maintainability.

## Starting and Configuring the App

## Starting

1. Download the latest version of Python from [python.org/downloads](http://www.python.org/downloads).

2. Run the downloaded installer.

3. During installation, check the box to "Add Python to PATH".

4. After installation, open your terminal or command line interface.

5. Navigate to the root directory of the OFF project.

6. Install dependencies by running:

   

```
bash
pip install -r requirements.txt
```



Start the application with:

1. ```
   bash
   python main.py
   ```

   

   Congratulations! You have successfully launched the application.

## Variables in `config.py`

There are three types of variables in `config.py`:

| Variable Type | Values                                                       | Example                        |
| ------------- | ------------------------------------------------------------ | ------------------------------ |
| `str`         | Characters (A-Z, a-z), numbers (0-9), and special characters | `"lorum ipsum dolor sit amet"` |
| `bool`        | True or False                                                | `True`, `False`                |
| `int`         | Whole numbers without a fractional part                      | `1337`, `-10`, `13`            |

## Configuring the App

To configure the app, modify values in `config.py`. All necessary variables are defined in this file, which can be set  using either Python syntax or environment variables. Ensure proper  syntax; otherwise, the app will not start.

## List of Configurable Variables

| Variable Name   | Default Value       | Purpose                                                     | Variable Type |
| --------------- | ------------------- | ----------------------------------------------------------- | ------------- |
| `logger_type`   | `console`           | Sets the type of logger used in the app                     | string        |
| `name_of_file`  | `""` (empty string) | Sets the name of the file where logging data will be stored | string        |
| `DBtype`        | `""` (empty string) | Sets the database type; defaults to `"sqlite3"` if empty    | string        |
| `DBport`        | `5432`              | Sets the port for the database                              | integer       |
| `DBpassword`    | `""` (empty string) | Sets the database password                                  | string        |
| `DBuser`        | `""` (empty string) | Sets the database user                                      | string        |
| `DBname`        | `""` (empty string) | Sets the name of the database                               | string        |
| `DBhost`        | `""` (empty string) | Sets the host for the database                              | string        |
| `ForumName`     | `"Awesome Forum"`   | Name displayed on forum pages                               | string        |
| `IsDebug`       | `True`              | Enables or disables debug mode                              | boolean       |
| `AdminUser`     | `"admin"`           | Sets name of forum admin account                            | string        |
| `AdminPassword` | `"1234567890"`      | Sets password for admin account                             | string        |
| `AdminName`     | `"anomin"`          | Displays admin nickname instead of AdminUser                | string        |
| `AdminCitate`   | `""`                | Sets citation displayed under admin messages                | string        |
| `AdminLogoPath` | `"admin.png"`       | File name displayed on admin accounts                       | string        |
| `MailSite`      | `""`                | SMTP server address for sending emails                      | string        |
| `MailPort`      | `""`                | SMTP server port                                            | integer       |
| `MailLogin`     | `""`                | SMTP server user login                                      | string        |
| `MailPassword`  | `""`                | SMTP server user password                                   | string        |
| `AppSecretKey`  | `""`                | Flask app secret key                                        | string        |
| `JwtSecretKey`  | `""`                | JWT tokens secret key                                       | string        |
| `APPport`       | `8000`              | Port for receiving requests                                 | integer       |
| `APPhost`       | `"0.0.0.0"`         | Host where app will run                                     | string        |

## Using Docker

To run OFF using Docker:

1. Navigate to the root directory of the OFF project.

2. Build the Docker image:

   

```
bash
sudo docker build -t OFF .
```



Run the Docker container:

1. ```
   bash
   sudo docker run -p 8000:8000 OFF
   ```

   

## Testing the App

Before testing, ensure that the application is running. Navigate to the "tests" directory in the OFF root folder and execute:

- For Windows:

  

```
bash
test.bat
```



For UNIX systems:

- ```
  bash
  ./test.sh
  ```

  

If tests pass, your configuration is correct. If issues arise, please create an issue on GitHub at [kotKolil/OFF](https://github.com/kotKolil/OFF).

## User Guide

## Logging In

1. Go to `/auth/log`, or click "Log In" at the bottom.
2. Enter your username and password.
3. Click "Log In".
4. If successful, you'll be redirected to the main page; otherwise, an error message will prompt you to retry.

## Registering an Account

1. Go to `/auth/reg`, or click "Register" at the bottom.
2. Fill out the registration form.
3. Click "Register".
4. Check your email for an activation link.

## Creating a Topic

1. Ensure you are logged in.
2. Click "Create Topic" on the main page or navigate to `/topic/create`.
3. Fill out the form and submit.

## Sending Messages

1. Ensure you are logged in.
2. Go to a topic where you wish to post a message.
3. Type your message and submit it.

## Deleting Messages or Topics

To delete a message or topic, use buttons near message forms in  topics or buttons within messages. Note that only logged-in users or  moderators can delete messages or topics.

## Accessing Your Personal Page

Click on "Personal Page" in the toolbar at the bottom of any page  to view your information and send messages or make posts on your wall.

## Replying to Messages in a Topic

To reply to a message in a topic, click "Reply" in that message's block; this will include its HTML content in your response.

## Moderation Page (Moderators Only)

To moderate users on forums, navigate to `/moderate/users`. Enter a user's ID in the input field and press "Get User". You can change their rights via checkboxes and save changes.

## API Documentation

OFF provides a comprehensive API for user management, topic handling, and message operations.

## User API Endpoints

## 1. Check Token

- **Endpoint:** `/api/user/CheckToken`

- **Method:** POST

- **Description:** Validates provided JWT token.

- **Request Body:**

  

- ```
  json
  { "JWToken": "string" }
  ```

  

- **Response:** 200 OK: Valid token. 400 Bad Request: Invalid token.

## 2. Generate Token

- **Endpoint:** `/api/user/generate_token`

- **Method:** POST

- **Description:** Generates a new JWT token based on provided credentials.

- **Request Body:**

  

- ```
  json
  { "user": "string", "password": "string" }
  ```

  

- **Response:** 201 Created: Returns JWT token if credentials are valid. 400 Bad Request: Invalid credentials.

## User Management Endpoints

## Get User Information

- **Endpoint:** `/api/user`
- **Method:** GET
- **Description:** Retrieves user information based on JWT token or UserId.
- **Parameters:** Optional query parameter for JWT validation (`JWToken`) Optional query parameter for fetching user data directly (`UserId`)
- **Response:** 200 OK: Returns user data if found. 404 Not Found: User data not found.

## Create New User

- **Endpoint:** `/api/user`

- **Method:** POST

- **Description:** Creates a new user account with provided details.

- **Request Body:**

  

- ```
  json
  { "email": "string", "UserId": "string", "password": "string", "citate": "string" }
  ```

  

- **Response:** 201 Created: Successful account creation; prompts email activation. 400 Bad Request: User already exists or request body is invalid.

## Delete User Account

- **Endpoint:** `/api/user`

- **Method:** DELETE

- **Description:** Deletes a user account based on provided JWT token and user identifier.

- **Request Body:**

  

- ```
  json
  { "JWToken": "string", "user": "string" }
  ```

  

- **Response:** 201 Created: Successful deletion of user account. 403 Forbidden: No permission to delete account. 404 Not Found: Specified user does not exist.

## Topic API Endpoints

## Topic Management Endpoints

## Get Topic

- **Method:** GET
- **Description:** Retrieves a specific topic by its ID.
- **Parameters:** Query parameter specifying TopicId to retrieve.

## Create Topic

- **Method:** POST
- **Description:** Creates a new topic with provided details.

## Update Topic

- **Method:** PATCH
- **Description:** Updates existing topic's details.

## Delete Topic

- **Method:** DELETE
- **Description:** Deletes specific topic based on its ID.

## Message API Endpoints

## Message Management Endpoints

## Get Messages

- **Method:** GET
- **Description:** Retrieves messages based on specified topic or message ID.

## Create Message

- **Method:** POST
- **Description:** Creates a new message within specified topic.

## Delete Message

- **Method:** DELETE
- **Description:** Deletes specific message by its ID if authorized.

This documentation serves as a comprehensive guide for developers  interacting with OFF Forum Engine, ensuring clarity and ease of use when implementing features related to forum management and API interactions. For further assistance or contributions, please visit our GitHub  repository at [kotKolil/OFF](https://github.com/kotKolil/OFF) and on web-site https://kotkolil.github.io/OFF/.
