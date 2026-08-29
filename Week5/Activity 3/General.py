from Staff import Staff

class General(Staff):
    def __init__(self, id, name, tax_num, rate_of_pay):
        super().__init__(id, name, tax_num)
        self.rate_of_pay = rate_of_pay

    def info(self):
        print("General staff name:", self.name)
        print("General staff rate of pay:", self.rate_of_pay)
        print()