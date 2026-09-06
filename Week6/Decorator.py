import time
import functools
import datetime

# template
def decorator(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # do sth before the function
        value = func(*args, **kwargs)
        # do sth after the function
        return value

    return wrapper


def timer(func):
    """
    To evaluate the run-time of a function
    :param func:
    :return:
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        value = func(*args, **kwargs)
        end_time = time.time()
        run_time = end_time - start_time

        print(f"It took {run_time} seconds to run the function.")

        return value

    return wrapper


def morning(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        hour = datetime.datetime.now().hour
        if 6 < hour < 9:
            value = func(*args, **kwargs)
            return value
        else:
            raise Exception("Not in the morning!")

    return wrapper

def demo(a):
    def interval(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(a)
            value = func(*args, **kwargs)
            # do sth after the function
            return value

        return wrapper

    return interval

def separator(symbol):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # do sth before the function
            value = func(*args, **kwargs)
            print(symbol * 20)
            # do sth after the function
            return value

        return wrapper

    return decorator

class decorator():
    def __init__(self):
        pass

    def __call__(self):
        pass