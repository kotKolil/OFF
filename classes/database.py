import sqlite3
import psycopg2 as psql

class sql_lite3_db:

    def __init__(self,db_name=""):
        self.name = name

    def execute_query(self, query):
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
        cursor.close()

        #TODO convert result to list
        return result
    

class postgres_db:
    def __init__(self, port=5432, password="admin", user="admin", name="",host="127.0.0.1"):
        self.port = port
	self.password = password
	self.user = user
	self.name = name
	self.host = host
	#initialisng database


    def execute_query(self, query):
        connection = psql.connect(user=self.user,
                                  port=self.port,
                                  password=self.password,
                                  database=self.name,
                                  host=self.host)
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
        cursor.close()
        return result



