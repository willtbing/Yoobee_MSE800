def read_int(prompt, minimum, maximum):
    while True:
        try:
            number = int(input(f"{prompt} between the range {minimum} and {maximum}: "))
        except ValueError:
            print("Please enter a whole number.")
        else:
            if number < minimum or number > maximum:
                print("The number is outside that range.")
            else:
                return number
            
print(read_int("Enter a number", 1, 10))
