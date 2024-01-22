import psycopg2
from os import getenv
from product import Product
from price import Price
from typing import List

class Db:
    insert_query = """INSERT INTO %s VALUES('%s')"""
    create_commands = ["""
    CREATE TABLE product (
                product_id SERIAL PRIMARY KEY,
                product_name VARCHAR(255) NOT NULL,
                image_url VARCHAR(255)
            )""",
    """
    CREATE TABLE prijs (
                prijs_id SERIAL PRIMARY KEY,
                prijs_value DECIMAL(10,2) NOT NULL,
                product_id INTEGER NOT NULL,
                date_change DATE NOT NULL,
                FOREIGN KEY (product_id) 
                    REFERENCES product (product_id)
                    ON DELETE CASCADE);"""]
    
    def __init__(self):
        self.conn = psycopg2.connect(
        host="localhost",
        database="jumbo",
        user="postgres",
        password=getenv('DATABASE_PASSWORD'))
        self.cur = self.conn.cursor()

    def create(self):
        for command in self.create_commands:
            try:
                self.cur.execute(command)
            except Exception as e:
                print(e)
        self.cur.close()
        self.conn.commit()

    def add_price(self, price : Price, product_id : int):
        self.cur.execute(self.insert_query, ("prices(product_id, price, change_date)", str(product_id) + "','" + str(price.price) + "','" + price.date))  

    def add_product(self, product : Product):
        self.cur.execute(self.insert_query, ("products(product_name, image_url, url)", product.name + "','" + product.image_url + "','" + product.url))

    def get_product_id(self, product : Product):
        self.cur.execute("SELECT product_id FROM products WHERE product_name LIKE '" + product.name + "'")
        result = self.cur.fetchone()
        product.id = result[0]
    
    def get_product_with_name(self, name : str) -> Product:
        self.cur.execute("SELECT * FROM products WHERE product_name LIKE '" + name + "'")
        result = self.cur.fetchone()
        new_product = Product(result[1], result[3], result[2], result[0], None)
        return new_product

    def get_product_with_id(self, _id : int) -> Product:
        self.cur.execute("SELECT * FROM products WHERE product_id =" + str(_id))
        result = self.cur.fetchone()
        new_product = Product(result[1], result[3], result[2], result[0], None)
        return new_product
    
    def get_last_id(self) -> int:
        self.cur.execute(" SELECT product_id FROM products ORDER BY product_id DESC LIMIT 1")
        result = self.cur.fetchone()
        if result is None:
            return 0
        return int(result[0])
    
    def insert_product_prices_list(self, products : List[Product]):
        try:
            for product in products:
                print(product.toString())
                self.add_product(product)
            self.commit()
            for product in products:
                self.add_price(product.price, product.id)
            self.commit()
        except Exception as e:
            print(e)

    def commit(self):
        self.conn.commit()