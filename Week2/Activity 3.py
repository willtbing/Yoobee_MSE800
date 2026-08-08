class Student:
    # constructor to initialize the student object
    def __init__(self, name, age, address, id):
        self.name = name
        self.age = age
        self.address = address
        self.student_id = id

    # method to display student information
    def display_info(self):
        print(f"Name: {self.name}, Age: {self.age}, Address: {self.address}, Student ID: {self.student_id}")

    # static method to sort a list of students by age
    @staticmethod
    def sort_students_by_age(students):
        return sorted(students, key= lambda student: student.age)

def main():
    # define a list to hold Student objects
    Students = []
    # input unknown number of students
    while True:
        name = input("Enter student's name (or 'exit' to finish): ")
        if name.lower() == 'exit':
            break
        age = int(input("Enter student's age: "))
        address = input("Enter student's address: ")
        student_id = input("Enter student's ID: ")

        stu = Student(name, age, address, student_id)
        Students.append(stu)
    # sort the students by age
    sorted_students = Student.sort_students_by_age(Students)
    # display the sorted list of students
    print("\nSorted list of students by age:")
    for student in sorted_students:
        student.display_info() 

if __name__ == "__main__":
    main()