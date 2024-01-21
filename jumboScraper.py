from scraper import Scraper
from databaseActions import Db

s = Scraper()
db = Db()

prices = s.retrieve_products()
for p in prices:
    print(p.toString())
    db.add_product(p.product)
    db.add_price(p)
Db.commit()