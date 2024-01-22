from scraper import Scraper
from databaseActions import Db

s = Scraper()
db = Db()

s.retrieve_products(db)