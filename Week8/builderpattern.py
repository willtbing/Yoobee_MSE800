class travel:
    def __init__(self, destination, hotel, transport, mealplan, activities, insurance):
        self.destination = destination
        self.hotel = hotel
        self.transport = transport
        self.mealplan = mealplan
        self.activities = activities
        self.insurance = insurance
    def show(self):
        print("The destination is ", self.destination)
        print("The hotel is ", self.hotel)
        print("The transport is ", self.transport)
        print("The mealplan is ", self.mealplan)
        print("The activities are ", self.activities)
        print("The insurance is included. ", self.insurance)
class travelbuilder():
    def __init__(self):
        self.destination = ""
        self.hotel = ""
        self.transport = ""
        self.mealplan = ""
        self.activities = []
        self.insurance = ""
    def setdestination(self, destination):
        self.destination = destination
        return self
    def sethotel(self, hotel):
        self.hotel = hotel
        return self
    def settransport(self, transport):
        self.transport = transport
        return self
    def setmealplan(self, mealplan):
        self.mealplan = mealplan
        return self
    def setactivities(self, activities):
        self.activities = activities
        return self
    def setinsurance(self, insurance):
        self.insurance = insurance
        return self
    def builder(self):
        return travel(
            self.destination,
            self.hotel,
            self.transport,
            self.mealplan,
            self.activities,
            self.insurance,
        )
t1 = travelbuilder()\
        .setdestination("Auckland")\
        .sethotel("5-star")\
        .settransport("Flight")\
        .setmealplan("Full Board")\
        .setactivities("City Tour")\
        .setinsurance("Yes")\
        .builder()
t1.show()