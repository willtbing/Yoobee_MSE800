class OutOfStockError(Exception):
    """Raised when trying to sell more items than are in stock."""


def calculate_price(price, quantity, discount=0.0):
    if price <= 0:
        raise ValueError("price must be positive")
    if quantity <= 0:
        raise ValueError("quantity must be positive")
    if not 0 <= discount < 1:
        raise ValueError("discount must be between 0 and 1")
    return price * quantity * (1 - discount)


class Product:
    def __init__(self, name, price, stock=0):
        self.name = name
        self.price = price
        self.stock = stock

    @property
    def in_stock(self):
        return self.stock > 0

    def sell(self, quantity):
        if quantity > self.stock:
            raise OutOfStockError(
                f"Cannot sell {quantity} {self.name}: only {self.stock} left"
            )
        self.stock -= quantity

    def restock(self, quantity):
        if quantity <= 0:
            raise ValueError("restock quantity must be positive")
        self.stock += quantity


class Inventory:
    def __init__(self):
        self.products = []

    def add(self, product):
        self.products.append(product)

    def cheapest_in_stock(self):
        available = [p for p in self.products if p.in_stock]
        if not available:
            return None
        return min(available, key=lambda p: p.price)
