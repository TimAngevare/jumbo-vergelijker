from datetime import datetime

class Price:
    def __init__(self, price : float, date : str):
        self.price=price
        if date == None:
            self.date = datetime.today().strftime('%Y-%m-%d')
        else:
            self.date = date