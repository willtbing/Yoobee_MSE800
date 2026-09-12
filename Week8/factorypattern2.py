from abc import ABC, abstractmethod
# ==========================================
# 1. ABSTRACT PRODUCT
# ==========================================
class Notification:
    @abstractmethod
    def send(self):
        pass
# ==========================================
# 2. CONCRETE PRODUCTS
# ==========================================
class email(Notification):
    def send(self):
        return "send by email"
class sms(Notification):
    def send(self):
        return "send by sms"
class push(Notification):
    def send(self):
        return "send by push notification" 
# ==========================================
# 3. ABSTRACT FACTORY / CREATOR
# ==========================================
class Factory(ABC):
    @abstractmethod
    def create_msg(self):
        pass
# ==========================================
# 4. CONCRETE FACTORIES
# ==========================================
# Concrete Factory
class EmailCreate(Factory):
    def create_msg(self):
        return email()

class SMSCreate(Factory):
    def create_msg(self):
        return sms()
class PushCreate(Factory):
    def create_msg(self):
        return push()
# ==========================================
# 5. CLIENT
# ==========================================
factory = EmailCreate()
msg = factory.create_msg()
print(msg.send())
