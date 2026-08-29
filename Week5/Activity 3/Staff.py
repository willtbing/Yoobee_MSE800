from Person import Person

class Staff(Person):
    def __init__(self, id, name, tax_num):
        super().__init__(id, name)
        self.tax_num = tax_num

    def info(self):
        print("Staff id:", self.id)
        print("Staff name:", self.name)
        print("Staff tax_num:", self.tax_num)
        print()