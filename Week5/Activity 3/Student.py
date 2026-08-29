from Person import Person

class Student(Person):
    def __init__(self, id, name):
        super().__init__(id, name)

    def info(self):
        print("Student id:", self.id)
        print("Student name:", self.name)
        print()