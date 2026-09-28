import cProfile

def slow_function():
    total = 0
    for i in range(500_000):
        total += i * i
    return total

def fast_function():
    return sum(range(500_000))

def main():
    slow_function()
    fast_function()

cProfile.run("main()")