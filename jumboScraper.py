import databaseActions as db
import product
import price

db = db.db()
# product = product.product("banana", "https://banana.com", "https://banana.com/image")
# db.add_product(product)
product = db.get_product_with_id('2')
print(product.name)
