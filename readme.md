<H3 align="center">Object-Oriented Flask Forum </H3>
<hr>
I present to you my own web forum. You can register on it, create your own threads, and write messages in them that will appear in real-time without refreshing the page.




<img src="screenshot.jpg">
<H4>About the project structure</H4>
..OFF<p>
└───classes<p>
&emsp;├───media<p>
&emsp;├───static<p>
&emsp;├───templates<p>
This forum uses a class system to make the project safe and easy to maintain. All parts of the application (logger, database, business logic) are implemented as classes. When the application is started, the user passes data to the business logic, which starts web sockets and uses parts of the application to respond to incoming requests.

<H4>Classes</H4>

<ol>
 <li>sql_lite3_db & PostgresDb - responsible for interacting with the database, executing the given query, and returning the response. sqlite3_db takes only the database name, PostgresDb takes the port, password, database name, and host. Both classes have the method execute_query(), which takes a query string to the database and returns the query result. </li>
 <li>
 
 txt_log & json_log - log information provided in files. Both classes take the file name (filename) and the path to it (path) as input. They have the log_message() method, which takes text as input.

 </li>

 <li>
server - a class representing the business logic, 
accepting requests and starting the main application loop. 
Takes class_logger - logger class, 
db - database class, frm - forum class, 
prt - port on which the application will accept requests, 
dbg - boolean value determining the application's debugging mode.
forum - responsible for threads, takes db - database,
name - name. Has methods all() - returns all threads ever created, 
get - get a thread by its id,
delete - delete a thread, update - update thread information.
 </li>


 <H4>Containerization of the application</H4>
 In the application folder, there is a Dockerfile. If you are using PostgresSQL, you need to set environment variables 
 from which information for connecting to the database is taken.
 <p>
 Execute in the application folder: 

 ```
 sudo docker build - t forum .
 ```
 
 Once the build is complete, execute:

 ```
 sudo docker run forum
 ```

</ol>