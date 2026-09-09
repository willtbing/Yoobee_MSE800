class payment:
    def make_payment(self):
        return "Some payment method"
class CreditCard(payment):
    def make_payment(self):
        return "Pay by Credit Card"
class PayPal(payment):
    def make_payment(self):
        return "Pay by PayPal"
class Bank_Transfer(payment):
    def make_payment(self):
        return "Pay by Bank Transfer"
# Polymorphic behavior
payments = [CreditCard(), PayPal(), Bank_Transfer()]
for pay in payments:
    print(pay.make_payment())