import psycopg2
import os
from flask import jsonify

from instance.config import Config


class Db(object):
    def __init__(self):
        self.db_name = Config.DB_NAME
        self.db_host = Config.DB_HOST
        self.db_user = Config.DB_USER
        self.db_password = Config.DB_PASSWORD
        self.conn = None

    def createConnection(self):
        try:
            if Config.APP_SETTINGS == "testing":
                self.conn = psycopg2.connect(database="test_db")
            elif Config.APP_SETTINGS == "development":
                self.conn = psycopg2.connect(
                    database=self.db_name, host=self.db_host, password=self.db_password)
            else:
                self.conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
            return self.conn

        except:
            return jsonify({"error": "failed to connect"})

    def createTables(self):
        cursor = self.createConnection().cursor()
        tables = [
            """CREATE TABLE IF NOT EXISTS users(
                id serial PRIMARY KEY,
                email varchar(255) NOT NULL,
                password varchar(255) NOT NULL,
                role varchar(10) NOT NULL
                )
            """,

            """CREATE TABLE IF NOT EXISTS products(
                id serial PRIMARY KEY,
                 title varchar(250) NOT NULL,
                 category varchar NOT NULL,
                  price float(45) NOT NULL,
                  quantity int NOT NULL,
                  minimum_stock varchar(255) NOT NULL,
                  description varchar(255) NOT NULL,
                  date varchar(255) NOT NULL)
                  """,

            """
            CREATE TABLE IF NOT EXISTS sales(
                id serial PRIMARY KEY,
                userId int REFERENCES users(id) NOT NULL,
                productId int REFERENCES products(id),
                date varchar(255) NOT NULL)
            """
        ]
        try:
            for table in tables:
                cursor.execute(table)
        except Exception as e:
            print(e)
            return "error"
        self.conn.commit()
        self.conn.close()

    def destroy_tables(self):
        cursor = self.createConnection().cursor()
        sql = [" DROP TABLE IF EXISTS users CASCADE",
               " DROP TABLE IF EXISTS products CASCADE",
               " DROP TABLE IF EXISTS sales CASCADE"
               ]
        for string in sql:
            cursor.execute(string)
        self.conn.commit()
        self.conn.close()
