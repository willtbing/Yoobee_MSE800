'''
#demo1
try:
    value = int(input("Input a non-zero integer number.\n"))
    result = 100 / value
except ValueError:
    print("Not a number")
except ZeroDivisionError:
    print("Cannot divide by zero")

try:
    value = int(input("Input a non-zero integer number.\n"))
    result = 100 / value
except (ValueError, ZeroDivisionError) as e:
    print(e)

#demo2
try:
    cars = {"A1": "Toyota"}
    print(cars["B2"])
except KeyError as e: # e is a variable that refers to the actual exception object
    print("Type:", type(e).__name__) # name of the exception class as a string
    print("Detail:", e)

#demo3
def my_function(a, b):
    return a/b

num1 = int(input("Input the first number.\n"))
num2 = int(input("Input the second number.\n"))
try:
    my_function(num1,num2)
except ZeroDivisionError as e:
    print(e)
else:
    print("Everything worked OK")
finally:
    print("Always runs")

#demo4
def read_first_line(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.readline().strip()
    except FileNotFoundError:
        print(f"File not found: {path}")
    except PermissionError:
        print(f"No permission to read: {path}")
    return None
'''

#demo5
def calculate_discount(price):
    if price < 0:
        raise ValueError("Price cannot be negative")
    if price == 0:
        raise ValueError("Price cannot be zero")
    discount = price * 0.10
    return discount

try:
    price = float(input("Enter the price: "))
    discount = calculate_discount(price)
    print("Discount:", discount)
    print("Final price:", price - discount)
except ValueError as e:
    print("Error type:", type(e).__name__)
    print("Error message:", e)

