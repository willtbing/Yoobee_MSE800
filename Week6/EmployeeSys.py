is_logged_in = input("If user has logged in enter 1, else enter 0.\n") == "1"
def login_required(func):
    def wrapper(*args, **kwargs):
        if is_logged_in == True:
            result = func(*args, **kwargs)
            return result
        else:
            print("Please login first")
    return wrapper

@login_required
def view_salary():
    print("Your salary is ...")

@login_required
def view_person_details():
    print("Your detailed information ...")

@login_required
def download_report():
    print("Here is your report")

view_salary()
view_person_details()
download_report()