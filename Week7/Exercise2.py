'''
Exercise 2
A university wants to develop a student information system. Every person in the university has a 
name. A student is a person and has an additional student ID. A postgraduate student is a student 
and has an additional research topic. Design and implement suitable Python classes for this 
system. Create a postgraduate student object and display the person's name, student ID, and 
research topic. Use super() where appropriate.
'''
class person:
    def __init__(self, name):
        self.name = name
    def printinfo(self):
        print(f"Person name: {self.name}")
class student(person):
    def __init__(self, name, studentid):
        super().__init__(name)
        self.studentid = studentid
    def printinfo(self):
        super().printinfo()
        print(f"Student id: {self.studentid}")
class postgraduatestudent(student):
    def __init__(self, name, studentid, research_topic):
        super().__init__(name, studentid)
        self.research_topic = research_topic
    def printinfo(self):
        super().printinfo()
        print(f"Research topic: {self.research_topic}")
ps1 = postgraduatestudent("Pei Wu", 1, "Software engineer")
ps1.printinfo()
    

