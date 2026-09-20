class student:
    def __init__(self, name):
        self.name = name
        self.marks = []

    def average(self):
        return sum(self.marks) / len(self.marks)

s = []
maxmarks = 0
first = ""
totalmarks = 0
for i in range(5):
    stu = student(input("Please enter student's name: "))
    for j in range(3):
        stu.marks.append(float(input(f"Enter mark {j+1}: ")))
    s.append(stu)
    print(stu.name, "'s average mark is: ", stu.average(), sep = "")
    if stu.average() < 50:
        print(stu.name, " failed in this subject.", sep = "")
    else:
        print(stu.name, " passed in this subject.", sep = "")
    if sum(stu.marks) > maxmarks:
        maxmarks = sum(stu.marks)
        first = stu.name
    totalmarks += sum(stu.marks)
    
print("class average mark is: ", totalmarks / (5 * 3), sep = "")
print(first, " has the highest mark: ", maxmarks, sep = "")
