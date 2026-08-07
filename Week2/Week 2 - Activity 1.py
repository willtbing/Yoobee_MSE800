class BMI_calculator():
    def calculate_bmi(self, weight, height):
        bmi = weight / (height ** 2)
        return bmi
print("Welcome to the BMI Calculator!")
weight = float(input("Enter your weight in kilograms: "))
height = float(input("Enter your height in meters: "))
bmi_calculator = BMI_calculator()
bmi_score = bmi_calculator.calculate_bmi(weight, height)
print(f"Your BMI score is: {bmi_score:.2f}")   