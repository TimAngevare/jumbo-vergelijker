from datetime import datetime

class price:
    def __init__(self, price, date, product):
        self.price=price
        self.product=product
        if date == None:
            self.date = datetime.today().strftime('%Y-%m-%d')
        else:
            self.date = date