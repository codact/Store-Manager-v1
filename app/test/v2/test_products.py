from .base_test import *


class TestProducts(TestsForApi):
    def test_for_empty_keys_product_title_registration(self):
        '''Tests for an empty product title key registration'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "": "infinix1",
                                         "category": "phones",
                                         "price": 536,
                                         "quantity": 5,
                                         "Minimum_stock": 2,
                                         "description": "great products to have at home while sleeping"
                                     }),
                                     headers=self.admin_header)
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "'title' is a required property")
        self.assertEqual(resp.status_code, 400)

    def test_for_empty_keys_product_category_registration(self):
        '''Tests for an empty product category key registration'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "infinix2",
                                         "": "phones",
                                         "price": 536,
                                         "quantity": 5,
                                         "Minimum_stock": 2,
                                         "description": "great products to have at home while sleeping"
                                     }),
                                     headers=self.admin_header)
        response = json.loads(resp.data)
        self.assertEqual(
            response["message"], "'category' is a required property")
        self.assertEqual(resp.status_code, 400)

    def test_for_empty_keys_product_price_registration(self):
        '''Tests for an empty product price key registration'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "infinix3",
                                         "category": "phones",
                                         "": 536,
                                         "quantity": 5,
                                         "Minimum_stock": 2,
                                         "description": "great products to have at home while sleeping"
                                     }),
                                     headers=self.admin_header)
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "'price' is a required property")
        self.assertEqual(resp.status_code, 400)

    def test_for_empty_keys_product_quantity_registration(self):
        '''Tests for an empty product quantity key registration'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "infinix4",
                                         "category": "phones",
                                         "price": 536,
                                         "": 5,
                                         "Minimum_stock": 2,
                                         "description": "great products to have at home while sleeping"
                                     }),
                                     headers=self.admin_header)
        response = json.loads(resp.data)
        self.assertEqual(
            response["message"], "'quantity' is a required property")
        self.assertEqual(resp.status_code, 400)

    def test_for_empty_keys_product_minimum_stock_registration(self):
        '''Tests for an empty product minimum_stock key registration'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "infinix5",
                                         "category": "phones",
                                         "price": 536,
                                         "quantity": 5,
                                         "": 2,
                                         "description": "great products to have at home while sleeping"
                                     }),
                                     headers=self.admin_header)
        response = json.loads(resp.data)
        self.assertEqual(
            response["message"], "'minimum_stock' is a required property")
        self.assertEqual(resp.status_code, 400)

    def test_for_empty_keys_product_description_registration(self):
        '''Tests for an empty product description key registration'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "infinix6",
                                         "category": "phones",
                                         "price": 536,
                                         "quantity": 5,
                                         "minimum_stock": 2,
                                         "": "great products to have at home while sleeping"
                                     }),
                                     headers=self.admin_header)
        response = json.loads(resp.data)
        self.assertEqual(
            response["message"], "'description' is a required property")
        self.assertEqual(resp.status_code, 400)

    def test_for_duplicate_product_registration(self):
        '''Test for duplicate product registration'''
        resp = self.test_client.post("/api/v2/products",
                                     data=self.product,
                                     headers=self.admin_header)
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Product already exists")
        self.assertEqual(resp.status_code, 400)

    def test_product_minimum_stock_more_than_quantity(self):
        '''Test for minimum stock more than quantity'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "infinix7",
                                         "category": "phones",
                                         "price": 3000,
                                         "quantity": 1,
                                         "minimum_stock": 5,
                                         "description": "great phone to have at home daily"
                                     }),
                                     headers=self.admin_header)
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "Minmum stock cant be more than quantity")
        self.assertEqual(resp.status_code, 400)

    def test_product_details_negative(self):
        '''Test for product price, quantity, and minimum stock negation'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "infinix9",
                                         "category": "phones",
                                         "price": -3000,
                                         "quantity": -1,
                                         "minimum_stock": -5,
                                         "description": "great phone to have at home in any situation"
                                     }),
                                     headers=self.admin_header)
        response = json.loads(resp.data)
        self.assertEqual(
            response["message"], "Price, quantity or minmum stock cant be negative")
        self.assertEqual(resp.status_code, 400)

    def test_product_description_less_than_20_chars(self):
        '''Test for short product descriptions'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "infinixa",
                                         "category": "phones",
                                         "price": 3000,
                                         "quantity": 10,
                                         "minimum_stock": 5,
                                         "description": "great"
                                     }),
                                     headers=self.admin_header)
        response = json.loads(resp.data)
        self.assertEqual(
            response["message"], "Product description cant be less than 20 characters")
        self.assertEqual(resp.status_code, 400)

    def test_for_empty_product_entries(self):
        '''Test for empty/no product entries'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({}),
                                     headers=self.admin_header)
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "'title' is a required property")
        self.assertEqual(resp.status_code, 400)

    def test_if_price_is_converted_to_a_float(self):
        '''Test for product creation using wrong data types'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "Mandazi",
                                         "category": "food",
                                         "price": 12050,
                                         "quantity": 23,
                                         "minimum_stock": 2,
                                         "description": "Great product to possess at school"
                                     }),
                                     headers=self.admin_header)
        response = json.loads(resp.data)
        self.assertEqual(response["Message"], "Successfully added")
        self.assertEqual(resp.status_code, 201)

    def test_for_successful_product_registration(self):
        '''Tests for a successful product registration'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "infinixq",
                                         "category": "phones",
                                         "price": 3000,
                                         "quantity": 10,
                                         "minimum_stock": 5,
                                         "description": "great products to have at hoome"
                                     }),
                                     headers=self.admin_header)
        response = json.loads(resp.data)
        self.assertEqual(response["Message"], "Successfully added")
        self.assertEqual(resp.status_code, 201)

    def test_for_product_registration_attendant(self):
        '''Tests for a product registration by a sales attendant'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "infinixw",
                                         "category": "phones",
                                         "price": 3000,
                                         "quantity": 10,
                                         "minimum_stock": 5,
                                         "description": "great products to have at hoome"
                                     }),
                                     headers=self.attendant_header)
        response = json.loads(resp.data)
        self.assertEqual(response["Message"], "You must be an admin")
        self.assertEqual(resp.status_code, 403)

    def test_for_token_missing_product_registration(self):
        '''Test for the functionality of token based authentication'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "infinixe",
                                         "category": "phones",
                                         "price": 3000,
                                         "quantity": 10,
                                         "minimum_stock": 5,
                                         "description": "great products to have at hoome"
                                     }),
                                     headers={
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "Token Missing, Login to get one")
        self.assertEqual(resp.status_code, 401)

    def test_getting_all_products_success(self):
        '''Test for getting all products'''
        resp = self.test_client.get("/api/v2/products",
                                    headers=self.admin_header)
        self.assertEqual(resp.status_code, 200)

    def test_getting_one_product_successful(self):
        '''Test for getting one product'''
        resp = self.test_client.get("/api/v2/products/1",
                                    headers=self.attendant_header)
        self.assertEqual(resp.status_code, 200)

    def test_getting_one_sale_wrong_id(self):
        '''Test for getting one product using wrong id'''
        resp = self.test_client.get("/api/v2/products/5",
                                    headers=self.attendant_header)
        self.assertEqual(resp.status_code, 404)

    def test_for_wrong_product_delete(self):
        '''Tests for a successful product deleting'''
        resp = self.test_client.delete("/api/v2/products/10",
                                       headers=self.admin_header)
        response = json.loads(resp.data)
        self.assertEqual(
            response["Message"], "No product/products found")
        self.assertEqual(resp.status_code, 404)

    def test_for_product_creation_data_types(self):
        '''Test for product creation using wrong data types'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": 1212,
                                         "category": "phones",
                                         "price": 10000,
                                         "quantity": 100,
                                         "minimum_stock": 12,
                                         "description": "This is a great product to have while in camping sites"
                                     }),
                                     headers=self.admin_header)
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "1212 is not of type 'string'")
        self.assertEqual(resp.status_code, 400)

    def test_post_product_wrong_data_types_category(self):
        '''Test for product creation using wrong data types in category'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "Reebok",
                                         "category": 455,
                                         "price": 10000,
                                         "quantity": 100,
                                         "minimum_stock": 12,
                                         "description": "This is a great product to have while in camping sites"
                                     }),
                                     headers=self.admin_header)
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "455 is not of type 'string'")
        self.assertEqual(resp.status_code, 400)

    def test_post_product_wrong_data_types_price(self):
        '''Test for product creation using wrong data types in price'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "Reebok1",
                                         "category": "food",
                                         "price": "food",
                                         "quantity": 100,
                                         "minimum_stock": 12,
                                         "description": "This is a great product to have while in camping sites"
                                     }),
                                     headers=self.admin_header)
        response = json.loads(resp.data)
        self.assertEqual(
            response["message"], "'food' is not of type 'number'")
        self.assertEqual(resp.status_code, 400)

    def test_post_product_wrong_data_types_quantity(self):
        '''Test for product creation using wrong data types in quantity'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "Reebok2",
                                         "category": "food",
                                         "price": 1000,
                                         "quantity": "ASas",
                                         "minimum_stock": 12,
                                         "description": "This is a great product to have while in camping sites"
                                     }),
                                     headers=self.admin_header)
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "'ASas' is not of type 'integer'")
        self.assertEqual(resp.status_code, 400)

    def test_post_product_wrong_data_types_minimum_stock(self):
        '''Test for product creation using wrong data types in minimum stock'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "Reebok3",
                                         "category": "food",
                                         "price": 10000,
                                         "quantity": 10,
                                         "minimum_stock": "jemo",
                                         "description": "This is a great product to have while in camping sites"
                                     }),
                                     headers=self.admin_header)
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "'jemo' is not of type 'integer'")
        self.assertEqual(resp.status_code, 400)
