# Target
class NewPayment:
    def pay(self):
        print("Others are paid by new payment.")
# Adaptee
class ThirdpartyPayment:
    def specific_pay(self):
        print("Payment of $500 made using Old Payment System.")
# Adapter
class Adapter(NewPayment):
    def __init__(self, adaptee):
        self.adaptee = adaptee
    def pay(self):
        self.adaptee.specific_pay()
        super().pay()
# Client
adaptee = ThirdpartyPayment()
adapter = Adapter(adaptee)
adapter.pay()