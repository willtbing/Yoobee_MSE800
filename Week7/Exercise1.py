'''
Exercise 1
A company wants to develop a simple employee management system. The system should store an 
employee's name and employee ID. A manager is also an employee, but a manager has additional 
information about the department they manage. Create suitable Python classes to represent this 
relationship. Use a constructor to initialise the required information and create a manager object 
to display all the details.
'''
class employee:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    def printinfo(self):
        print(f"Employee id: {self.id}")
        print(f"Employee name: {self.name}")
class manager(employee):
    def __init__(self, id, name, manage_department_id):
        super().__init__(id, name)
        self.manage_department_id = manage_department_id
    def printinfo(self):
        super().printinfo()
        print(f"Manage department id: {self.manage_department_id}")
e1 = employee(1, "Alex")
e1.printinfo()
e2 = manager(2, "Bob", 1)
e2.printinfo()

