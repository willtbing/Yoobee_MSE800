class Food:
    def Order(self):
        pass
class Pizza(Food):
    def Order(self):
        print("Here is your pizza")
class Burger(Food):
    def Order(self):
        print("Here is your burger")
class Pasta(Food):
    def Order(self):
        print("Here is your pasta") 
class FoodOrderFactory:
    @staticmethod
    def CreatOrder(FoodType):
        if FoodType == "Pizza":
            return Pizza()
        elif FoodType == "Burger":
            return Burger()
        else:
            return Pasta()
foodorder = FoodOrderFactory.CreatOrder("Burger")
foodorder.Order()
