class Department:
    def __init__(self, department_name, head):
        self.departmentname = department_name
        self.head = head
    def show_department(self):
        print(f"Department name: {self.departmentname}")
        print(f"Head: {self.head}")
class University:
    def __init__(self, name):
        self.name = name
        self.department = Department("CS", "Nike")
    def show_university(self):
        print(f"University Name: {self.name}")
        self.department.show_department()
u1 = University("Southeast University")
u1.show_university()