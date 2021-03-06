from flask import abort

from .main_model import InitializeConnection


class Product_Model(InitializeConnection):
    '''Inittializes a new product'''

    def __init__(self, data=None):
        InitializeConnection.__init__(self)
        self.data = data

    def save(self):
        '''Method to save a product by appending it to existing
        products table'''
        self.cursor.execute(
            """INSERT INTO products(title,category_id,price,quantity,
            minimum_stock,description, date) VALUES(%s,%s,%s,%s,%s,%s,%s)""",
            (self.data["title"].strip(), self.data["category_id"].strip(),
             self.data["price"],
             self.data["quantity"],
             self.data["minimum_stock"],
             self.data["description"].strip(), self.date),
        )
        self.cursor.execute("SELECT id FROM products WHERE title = %s",
                            (self.data["title"],))
        row = self.cursor.fetchone()
        self.id = row[0]

    def update(self, productId):
        '''Method is meant to update a product by editing its details in the
        products table'''
        self.productId = productId
        self.cursor.execute("SELECT id FROM products WHERE title = %s",
                            (self.data["title"],))
        row = self.cursor.fetchone()
        if not row or row[0] == self.productId:
            self.cursor.execute(
                """UPDATE products SET title = %s, category_id = %s, price = %s,
                        quantity = %s, minimum_stock = %s, description = %s,
                         date = %s
                        where id= %s
                        """,
                (self.data["title"].strip(), self.data["category_id"].strip(),
                 self.data["price"], self.data["quantity"],
                 self.data["minimum_stock"], self.data["description"].strip(),
                 self.date, self.productId)
            )
        else:
            abort(403, "Product title already exists, try another one")

    def get(self):
        sql = "SELECT * FROM products"
        self.cursor.execute(sql)
        products = self.cursor.fetchall()
        allproducts = []
        for product in products:
            list_of_items = list(product)
            self.cursor.execute(
                "SELECT * FROM categories WHERE id =%s",
                (list_of_items[2],)
            )
            category_details = self.cursor.fetchone()
            oneproduct = {}
            oneproduct["id"] = list_of_items[0]
            oneproduct["title"] = list_of_items[1]
            oneproduct["category"] = category_details[1]
            oneproduct["price"] = list_of_items[3]
            oneproduct["quantity"] = list_of_items[4]
            oneproduct["minimum_stock"] = list_of_items[5]
            oneproduct["description"] = list_of_items[6]
            allproducts.append(oneproduct)
        return allproducts

    def get_category_products(self, title):
        self.cursor.execute(
            "SELECT * FROM products where category_id =%s",
            (title,)
        )
        products = self.cursor.fetchall()
        allproducts = []
        for product in products:
            list_of_items = list(product)
            oneproduct = {}
            oneproduct["id"] = list_of_items[0]
            oneproduct["title"] = list_of_items[1]
            oneproduct["category_id"] = list_of_items[2]
            oneproduct["price"] = list_of_items[3]
            oneproduct["quantity"] = list_of_items[4]
            oneproduct["minimum_stock"] = list_of_items[5]
            oneproduct["description"] = list_of_items[6]
            allproducts.append(oneproduct)
        return allproducts

    def delete(self, productId):
        self.productId = productId
        self.cursor.execute(
            "DELETE from products where id = %s",
            (self.productId,)
        )

    def updateQuanitity(self, quantity, product_id):
        '''Method is meant to update a product by editing its details in the
        products table'''
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """UPDATE products SET quantity = %s WHERE id = %s""", (
                quantity, product_id,)
        )
