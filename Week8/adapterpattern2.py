class NewPayment:
    def otherpay(self):
        print("Others are paid by new payment.")
class ThirdpartyPayment:
    def specific_pay(self):
        print("Payment of $500 made using Old Payment System.")
class Adapter(NewPayment, ThirdpartyPayment):
    def pay(self):
        self.specific_pay()
        self.otherpay()
adapter = Adapter()
adapter.pay()