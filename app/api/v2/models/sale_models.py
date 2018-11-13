import psycopg2
from flask import jsonify

from .main_model import InitializeConnection


class Sales_Model(InitializeConnection):
    '''Initializes a sale'''

    def __init__(self, email=None, product=None,
                 quantity=None, subtotals=None):
        InitializeConnection.__init__(self)
        if email or product or quantity or subtotals:
            self.email = email
            self.title = product["title"]
            self.quantity = quantity
            self.subtotals = subtotals

    def save(self):
        '''Saves a sale to sale records'''
        self.cursor.execute(
            """INSERT INTO sales(email, title, quantity, subtotals,
             date) VALUES(%s,%s,%s,%s,%s)""",
            (self.email, self.title, self.quantity,
             self.subtotals, self.date),)

    def get(self):
        sql = "SELECT * FROM sales"
        self.cursor.execute(sql)
        sales = self.cursor.fetchall()
        allsales = []
        for sale in sales:
            list_of_sales = list(sale)
            onesale = {}
            onesale["id"] = list_of_sales[0]
            onesale["email"] = list_of_sales[1]
            onesale["title"] = list_of_sales[2]
            onesale["quantity"] = list_of_sales[3]
            onesale["subtotals"] = list_of_sales[4]
            onesale["date"] = list_of_sales[5]
            allsales.append(onesale)

        return allsales

    def checkSales(self):
        sale1 = Sales_Model()
        sales = sale1.get()
        return len(sales)
