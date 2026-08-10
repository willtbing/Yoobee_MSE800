#define class
class TemperatureConvert:
    # constructor to initialize the TemperatureConvert object
    def __init__(self, value):
        self.value = value;

   #convert Fahrenheit to Celsius
    def F2C(self, value):
        return round((value - 32) * 5 / 9, 2)

    #convert Celsius to Fahrenheit
    def C2F(self, value):
        return round(value * 9 / 5 + 32, 2)

#define main function
def main():
    #prompt the user to input the data according to the requirements
    userinput = input("Please enter the temperature with the correct 'C' or F' prefix (or 'exit' to finish).")
    while userinput != "exit":
        #get temperature value
        val = userinput[1:]
        #check if the value is valid
        if val.isdigit():
            #transfer the value from string into integer
            vald = int(val)
            #create the object res
            res = TemperatureConvert(vald)
            #according the first letter, choose the correct method
            if(userinput[0] == 'F'):
                value = res.F2C(vald)
                print(userinput + " degrees Fahrenheit is converted to " + str(value) + " degrees Celsius")
            elif(userinput[0] == 'C'):
                value = res.C2F(vald)
                print(userinput + " degrees Celsius is converted to " + str(value) + " degrees Fahrenheit")
            else:
                print("Invalid input.")
        else:
            print("Invalid input.")
        useinput = input("Please enter the temperature with the correct 'C' or F' prefix (or 'exit' to finish).")   

if __name__ == "__main__":
    main()