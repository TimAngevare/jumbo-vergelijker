import psycopg2
from os import getenv
from product import Product
from price import Price

class Db:

    def create(self):
        commands = ["""
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
        for command in commands:
            try:
                self.cur.execute(command)
            except Exception as e:
                print(e)
        self.cur.close()
        self.conn.commit()

    def __init__(self):
        self.conn = psycopg2.connect(
        host="localhost",
        database="jumbo",
        user="postgres",
        password=getenv('DATABASE_PASSWORD'))
        self.cur = self.conn.cursor()

    def add_price(self, price : Price):
        self.cur.execute("INSERT INTO prices(product_id, price, change_date) VALUES('" + price.product.id + "','" + price.price + "','" + price.date +  "')")  

    def add_product(self, product : Product):
        self.cur.execute("INSERT INTO products(product_name, image_url, url) VALUES('" + product.name + "','" + product.image_url + "','" + product.url +  "')")

    def get_product_id(self, product : Product):
        self.cur.execute("SELECT product_id FROM products WHERE product_name LIKE '" + product.name + "'")
        result = self.cur.fetchone()
        product.id = result[0]
    
    def get_product_with_name(self, name : str):
        self.cur.execute("SELECT * FROM products WHERE product_name LIKE '" + name + "'")
        result = self.cur.fetchone()
        new_product = Product(result[1], result[3], result[2], result[1])
        return new_product
    
    def get_product_with_id(self, _id : int):
        self.cur.execute("SELECT * FROM products WHERE product_id = '" + _id + "'")
        result = self.cur.fetchone()
        new_product = Product(result[1], result[3], result[2], result[1])
        return new_product

    def commit(self):
        self.conn.commit()