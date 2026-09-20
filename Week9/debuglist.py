marks = [65, 72, 80, 55, 90]
total = 0

breakpoint()

for mark in marks:
    total = total + mark

average = total / len(marks)
print("Average:", average)