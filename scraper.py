import requests
from bs4 import BeautifulSoup
from product import Product
from price import Price

class Scraper:
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15',
                                              'Accept-Language' : 'en-US,en;q=0.9',
                                              'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'}

    def __init__(self):
        self.url = 'https://www.jumbo.com'

    def get_product_containers(self, url):
        page = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        articles = soup.find_all("article", class_="product-container")
        return articles

    def create_product_price_from_element(self, element, id):
        image_div = element.find("div", {"class" : "product-image"})
        image_url = image_div.find('img')['src']

        content = element.find('div', {"class":"content"})
        title = content.find('a', {"class":'title-link'})
        name = title.text
        product_url = self.url + title['href']
        
        price_container = element.find('div', {"class":"current-price"})
        euros = price_container.find('span', {"class":"whole"}).text
        cents = price_container.find('sup', {"class":"fractional"}).text
        
        price = Price(float(euros + '.' + cents), None)
        product = Product(name, product_url, image_url, id, price)
        return product


    def retrieve_products(self, db):
        products = []
        base_url = self.url = "/producten/?offSet="
        pageCount = 0
        id_count = db.get_last_id() + 1
        while True:
            url = base_url + str(pageCount * 24)
            articles = self.get_product_containers(url)
            if len(articles) == 0:
                break
            for article in articles:
                products.append(self.create_product_price_from_element(article, id_count))
                id_count += 1
            if pageCount % 8 == 0:
                db.insert_product_prices_list(products)
                products = []
            pageCount += 1

    

    