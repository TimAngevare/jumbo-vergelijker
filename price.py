from datetime import datetime
from product import Product

class Price:
    def __init__(self, price : float, date : str, product : Product):
        self.price=price
        self.product=product
        if date == None:
            self.date = datetime.today().strftime('%Y-%m-%d')
        else:
            self.date = date
    
    def toString(self):
        return f"Price of {self.product.name} on {self.date} is {self.price}"