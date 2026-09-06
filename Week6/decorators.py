import time
def timing_decorator (func):
    def wrapper ():
        start_time = time.time ()
        result = func()
        end_time = time.time()
        print(f"Elapsed time: {end_time - start_time}")
        return result
    return wrapper

def start_end_decorator (func):
    def wrapper(*args, **kwargs):
        print("=================function start================")
        result = func(*args, **kwargs)
        print("=================function end================")
        return result
    return wrapper


#多个decorator的顺序不同，结果不同
@timing_decorator
@start_end_decorator
def say_hello():
    print("hello")

#say_hello()

@start_end_decorator
def square(num):
    print(num ** 2)

n = int(input("Input the num, then I will calculate the square of it.\n"))
result = square(n)
print(result)