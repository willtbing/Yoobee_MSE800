class account:
    def __init__(self,  id, name, balance):
        self.id = id
        self.name = name
        self.balance = balance
    def account_detail(self):
        print(f"Account number: {self.id}")
        print(f"Customer name: {self.name}")
        print(f"Account balance: {self.balance}")
    def deposit(self, amount):
        self.balance += amount
        return self.balance
    def withdraw(self, amount):
        if amount<=self.balance:
            self.balance-=amount
            return self.balance
        else:
            return False
class savingaccount(account):
    def __init__(self, id, name, balance, interestrate, interest = 0):
        super().__init__(id, name, balance)
        self.interestrate = interestrate
    def calinterestrate(self):
        self.interest = self.balance * self.interestrate
    def account_detail(self):
        print("This is a Savings Account")
        super().account_detail()
        self.calinterestrate()
        print(f"Interest: {self.interest}")
sc1 = savingaccount("SA1001", "John", 5000, 0.05)
sc1.deposit(1000)
sc1.withdraw(500)
sc1.account_detail()
    