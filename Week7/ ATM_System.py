from abc import ABC, abstractclassmethod
class ATM(ABC):
    @abstractclassmethod
    def insert_card(self):
        pass
    @abstractclassmethod
    def enter_pin(self):
        pass
    @abstractclassmethod
    def check_balance(self):
        pass
    @abstractclassmethod
    def withdraw(self, amount):
        pass
class BankATM(ATM):
    def insert_card(self):
        print("Insert your card.")
    def enter_pin(self):
        print("Enter your pin")
    def check_balance(self):
        print("Your balance is...")
    def withdraw(self, amount):
        print(f"You want to withdraw: {amount} money")
BA1 = BankATM()
BA1.insert_card()
BA1.enter_pin()
BA1.check_balance()
BA1.withdraw(500)