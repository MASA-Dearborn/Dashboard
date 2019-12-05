# Database writer

import mysql.connector

class SQLInterface():
    def __init__(self, username, password, database):
        self.db = mysql.connector(host="localhost", user=username, passwd=password, database=database)
        self.cursor = self.db.cursor()

    def create_table(self, name, columns):
        inst = "CREATE TABLE "

        full_instruction = inst + ""

        self.cursor.execute(full_instruction)
    
    def insert(self, table, data):
        sql = "INSERT INTO " + table + " VALUES (%s, %s)"

        self.cursor.execute(sql, data)
        self.db.commit()

    def write(self):
        pass
