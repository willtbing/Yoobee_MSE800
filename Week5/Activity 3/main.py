from Person import Person
from Student import Student
from Staff import Staff
from General import General
from Academic import Academic

def main():
    #input sample data
    Person1 = Person(1, "Jim")
    Person2 = Person(2, "Tom")

    Student1 = Student(3, "Kate")
    Student2 = Student(4, "Marry")

    Staff1 = Staff(5, "John", "CD3443")
    Staff2 = Staff(6, "Peter", "JI8945")

    General1 = General(7, "Robot", "CJ5252", 52452)
    General2 = General(8, "Amy", "NJ5429",82424)

    Academic1 = Academic(9, "Julie", "NE5829", 19)
    Academic2 = Academic(10, "Mike", "YU5213", 57)

    #output information
    Person1.info()
    Person2.info()

    Student1.info()
    Student2.info()

    Staff1.info()
    Staff2.info()

    General1.info()
    General2.info()

    Academic1.info()
    Academic2.info()

if __name__ == "__main__":
    main()
