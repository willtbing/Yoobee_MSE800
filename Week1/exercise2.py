weight = float(input("Enter your weight in kilograms: "))
height = float(input("Enter your height in meters: "))
# BMI score = An individual's weight in kilograms by the square of the height in meters
bmi = weight / (height ** 2)
print(f"Your BMI score is: {bmi:.2f}")