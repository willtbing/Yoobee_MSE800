import cProfile

def calculate():
    total = 0
    for i in range(1_000_000):
        total += i
    return total

cProfile.run("calculate()")