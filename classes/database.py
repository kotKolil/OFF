from abc import *
import sqlite3
import psycopg2 as psql

class sql_lite3_db():

    def __init__(self,db_name=""):
        super().__init__(name=db_name)

    def excute_query(self, query):
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
        cursor.close()

        #TODO convert result to list
        return result
    

class PostgresDb:
    def __init__(self, port=5432, password="admin", user="admin", name="",host="127.0.0.1"):
        self.port = port
        self.password = password
        self.user = user
        self.name = name
        self.host  = host

    def execute_query(self, query):
        connection = psql.connect(user=self.user,port=self.port,password=self.password,database=self.name,host=self.host)
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
        cursor.close()
        return result



