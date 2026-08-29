class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def info(self):
        print("Person id:", self.id)
        print("Person name:", self.name)
        print()