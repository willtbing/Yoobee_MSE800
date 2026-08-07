def Fibonacci(n):
    n1=0
    n2=1
    result = n2
    while n>-1:
        print(result)
        result = n1 + n2
        n1 = n2
        n2 = result
        n -= 1

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

n = int(input("Input any number to see the Fibonacci sequence up to that number: "))
Fibonacci(n)
fact = factorial(n)
print(f"The factorial of {n} is: {fact}")