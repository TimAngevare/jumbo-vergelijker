from price import Price

class Product:
    def __init__(self, name : str, url : str, image_url : str, id : int, price : Price) -> None:
        self.price = price
        self.id = id
        self.name = name
        self.url = url
        self.image_url = image_url

    def toString(self):
        return f"Most recent Price of {self.name} on {self.price.date} is {self.price.price}"