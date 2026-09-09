'''
Exercise 4
A university needs to maintain information about students from two different areas: academic 
information and contact information. Academic information includes the student's programme 
and GPA, while contact information includes the student's email address and phone number. 
Create suitable Python classes so that a student can have information from both areas. Create a 
student object and display all of the student's academic and contact information.
'''
class academicinfo:
    def __init__(self, programme, gpa):
        self.programme = programme
        self.gpa = gpa
    def printinfo(self):
        print(f"Student's programme: {self.programme}")
        print(f"Student's gpa: {self.gpa}")
class contactinfo:
    def __init__(self, email, phone):
        self.email = email
        self.phone = phone
    def printinfo(self):
        print(f"Student's Email: {self.email}")
        print(f"Student's phone number: {self.phone}")
class studentinfo(contactinfo, academicinfo):
    def __init__(self, name, id, email, phone, programme, gpa):
        self.name = name
        self.id = id
        contactinfo.__init__(self, email, phone)
        academicinfo.__init__(self, programme, gpa)
    def printinfo(self):
        print(f"Student's name: {self.name}")
        print(f"Student's id: {self.id}")
        contactinfo.printinfo(self)
        academicinfo.printinfo(self)
stu1 = studentinfo("Pei WU", 1, "willtbing@sina.com", "02108787438", "Software Engineer", 4.0)
stu1.printinfo()