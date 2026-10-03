'''try:
    print("A")
    x = int("abc")
    print("B")
except ValueError:
    print("C")
finally:
    print("D")'''

'''def f():
    try:
        return "try"
    finally:
        print("cleanup")
 
print(f())'''

'''try:
    nums = [1, 2, 3]
    print(nums[5])
except (IndexError, KeyError) as e:
    print(type(e).__name__)
else:
    print("no error")'''

try:
    print(10 / 2)
except ZeroDivisionError:
    print("zero")
else:
    print("ok")