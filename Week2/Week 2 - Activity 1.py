class BMI_calculator():
    def __init__(self, weight, height):
        self.weight = weight
        self.height = height

    def calculate_bmi(self):
        bmi = self.weight / (self.height ** 2)
        return bmi
print("Welcome to the BMI Calculator!")
weight = float(input("Enter your weight in kilograms: "))
height = float(input("Enter your height in meters: "))
bmi_calculator = BMI_calculator(weight, height)
bmi_score = bmi_calculator.calculate_bmi()
print(f"Your BMI score is: {bmi_score:.2f}")   