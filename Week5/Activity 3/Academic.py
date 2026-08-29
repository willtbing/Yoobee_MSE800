from Staff import Staff

class Academic(Staff):
    def __init__(self, id, name, tax_num, publications):
        super().__init__(id, name, tax_num)
        self.publications = publications

    def info(self):
        print("Lecturer name:", self.name)
        print("The number of publications:", self.publications)
        print()