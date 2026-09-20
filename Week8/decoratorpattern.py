class car:
    def cost(self):
        return 25000
    def description(self):
        return "Car"
class cardecorator:
    def __init__(self, car):
        self.car = car
    def cost(self):
        return self.car.cost()
class GPS(cardecorator):
    def cost(self):
        return self.car.cost() + 500
class Sunroof(cardecorator):
    def cost(self):
        return self.car.cost() + 1000
class LeatherSeats(cardecorator):
    def cost(self):
        return self.car.cost() + 1500
class Sound(cardecorator):
    def cost(self):
        return self.car.cost() + 800
c = Sound(LeatherSeats(Sunroof(GPS(car()))))
print(c.cost())