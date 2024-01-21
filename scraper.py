import requests
from bs4 import BeautifulSoup
from time import sleep
from product import Product
from price import Price

class Scraper:
    def __init__(self):
        self.url = 'https://www.jumbo.com'

    def create_product_price_from_element(self, element):
        image_div = element.find("div", _class="image-container")
        image_url = image_div.child['href']
        content = element.find('div', _class="content")
        title = content.find('a', _class='title-link')
        name = title.text
        product_url = title['href']
        price_container = element.find('div', _class="current-price")
        euros = price_container.find('span', _class="whole")
        cents = price_container.find('span', _class="fractional")
        product = Product(name, product_url, image_url, None)
        price = Price(float(euros + '.' + cents), None, product)
        return price


    def retrieve_products(self):
        products = []
        base_url = "https://www.jumbo.com/producten/?offSet="
        count = 0
        while True:
            page = requests.get(base_url + str(count * 24))
            sleep(3)
            soup = BeautifulSoup(page.content, 'html.parser')
            articles = soup.find_all("article", class_="product-container")
            if len(article) == 0:
                False
            for article in articles:
                products.append(self.create_product_price_from_element(article))

            count += 1
        return products

    

    