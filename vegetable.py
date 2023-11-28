class InvalidPrice(Exception):
    pass

class InvalidQuantity(Exception):
    pass

def validate_price(func):
    def wrapper1(self, new_price):
        if new_price > 0 and isinstance(new_price, (int,float)):
            return func(self, new_price)
        else:
            raise InvalidPrice('Enter a valid price.')
    return wrapper1

def validate_stock(func):
    def wrapper2(self, qty):
        if isinstance(qty, (float,int)):
            return func(self, qty)
        else:
            raise InvalidQuantity('Enter a valid quantity.')
    return wrapper2

class Vegetable():
    def __init__(self, name = None, category = None, price = None, stock = None):
        self._name = name
        self._category = category
        self._price = price
        self._stock = stock

    def update(self, name = None, type = None, price = None, stock = None):
        if name:
            self._name = name
        if type:
            self._category = type
        if price:
            self._price = price
        if stock:
            self._stock = stock

    @property
    def price(self):
        return self._price

    @price.setter
    @validate_price
    def price(self, new_price):
        self._price = new_price

    @property
    def stock(self):
        return self._stock
    
    @stock.setter
    @validate_stock
    def stock(self, qty):
        self._stock = qty


if __name__ == '__main__':
    try:
        carrot = Vegetable(name="Carrot", category="Root", price=1.5, stock=100)

        # Display the initial details
        print(f"Vegetable: {carrot._name}")
        print(f"Category: {carrot._category}")
        print(f"Price: {carrot.price}")
        print(f"Stock: {carrot.stock}")

        carrot.price = 5
        print(f"Price: {carrot.price}")

        #carrot.price = -2 

        carrot.stock = 20
        print(f"Stock: {carrot.stock}")

        carrot.stock = 'ghwi'

    except (InvalidPrice, InvalidQuantity) as e:
        print(f"Error: {e}")
