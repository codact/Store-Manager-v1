import psycopg2
from flask import jsonify
import datetime

from .db_models import Db


class Sales_Model():
    '''Initializes a sale'''

    def __init__(self, userId=None, product=None):
        if product and userId:
            self.userId = userId
            self.productId = product["id"]
        self.date = datetime.datetime.now()
        db = Db()
        db.createTables()
        self.conn = db.createConnection()

    def save(self):
        '''Saves a sale to sale records'''
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO sales(userId, productId, date) VALUES(%s,%s,%s)",
            (self.userId, self.productId, self.date),)
        self.conn.commit()
        self.conn.close()

    def get(self):
        db = Db()
        self.conn = db.createConnection()
        db.createTables()
        cursor = self.conn.cursor()
        sql = "SELECT * FROM sales"
        cursor.execute(sql)
        sales = cursor.fetchall()
        allsales = []
        for sale in sales:
            list_of_sales = list(sale)
            onesale = {}
            onesale["id"] = list_of_sales[0]
            onesale["userId"] = list_of_sales[1]
            onesale["productId"] = list_of_sales[2]
            onesale["date"] = list_of_sales[3]
            allsales.append(onesale)
        self.conn.commit()
        return allsales
    
    def checkSales(self):
        sale1 = Sales_Model()
        sales = sale1.get()
        return len(sales)