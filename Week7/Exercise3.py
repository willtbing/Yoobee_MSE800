'''
Exercise 3
A university employs different types of employees. All employees have a name and employee ID. 
However, lecturers have a teaching subject, administrators have a department, and technicians 
have a technical specialisation. Create suitable Python classes to represent these employees. 
Create objects for a lecturer, administrator, and technician and display their information.
'''
class employee:
    def __init__(self, name, id):
        self.name = name
        self.id = id
    def printinfo(self):
        print(f"Employee name: {self.name}")
        print(f"Employee id: {self.id}")
class lecturer(employee):
    def __init__(self, name, id, subject):
        super().__init__(name, id)
        self.subject = subject
    def printinfo(self):
        super().printinfo()
        print(f"Teaching subject: {self.subject}")
class administrator(employee):
    def __init__(self, name, id, department):
        super().__init__(name, id)
        self.department = department
    def printinfo(self):
        super().printinfo()
        print(f"Department: {self.department}")
class technician(employee):
    def __init__(self, name, id, tec_spec):
        super().__init__(name, id)
        self.tec_spec = tec_spec
    def printinfo(self):
        super().printinfo()
        print(f"Technical specialisation: {self.tec_spec}")
lecturer1 = lecturer("Alex", 1, "Python")
administrator1 = administrator("Bob", 2, "Department 1")
technician1 = technician("John", 3, "IT")
lecturer1.printinfo()
administrator1.printinfo()
technician1.printinfo()