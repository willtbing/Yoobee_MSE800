class Observer:
    def update(self, price):
        pass
# Concrete Observer
class Person(Observer):
    def __init__(self, name):
        self.name = name
    def update(self, price):
        print(self.name, "received new price: ", price)
# Subject
class PriceMonitor:
    def __init__(self):
        self.observers = []
    def add_observer(self, observer):
        self.observers.append(observer)
    def notify(self, price):
        for observer in self.observers:
            observer.update(price)
# Create observers
person1 = Person("Ali")
person2 = Person("Sara")
# Create subject
price = PriceMonitor()
# Subscribe people
price.add_observer(person1)
price.add_observer(person2)
# Temperature changes
price.notify(105)