'''
Exercise 5
A hospital wants to develop a system to manage information about its staff and patients. Every 
person in the hospital has a name. A doctor is a person and has a doctor ID, while a nurse is also a 
person and has a nurse ID. A senior nurse can have both the characteristics of a nurse and 
additional information related to their role, such as a ward they supervise. Design and implement 
suitable Python classes to represent these relationships. Create a SeniorNurse object and display 
all relevant information. Use constructors and super() where appropriate. Finally, identify the type 
of inheritance used and draw a class diagram before implementing the solution.
'''
class person:
    def __init__(self, name):
        self.name = name
    def printinfo(self):
        print(f"Name: {self.name}")
class nurse(person):
    def __init__(self, name, nurseid):
        super().__init__(name)
        self.nurseid = nurseid
    def printinfo(self):
        super().printinfo()
        print(f"Nurse id: {self.nurseid}")
class seniornurse(nurse):
    def __init__(self, name, nurseid, ward):
        super().__init__(name, nurseid)
        self.ward = ward
    def printinfo(self):
        super().printinfo()
        print(f"Ward: {self.ward}")
sn1 = seniornurse("Alex", 1, 5)
sn1.printinfo()
