from abc import ABC, abstractmethod
# ==========================================
# 1. ABSTRACT PRODUCT
# ==========================================
class Button:
    @abstractmethod
    def gui(self):
        pass

class CheckBox:
    @abstractmethod
    def gui(self):
        pass
# ==========================================
# 2. CONCRETE PRODUCTS
# ==========================================
class Windowsbutton(Button):
    def gui(self):
        return "This is Windows button"
class Windowscheckbox(CheckBox):
    def gui(self):
        return "This is Windows checkbox"
class Macbutton(Button):
    def gui(self):
        return "This is Mac button" 
class Maccheckbox(CheckBox):
    def gui(self):
        return "This is Mac checkbox"
# ==========================================
# 3. ABSTRACT FACTORY / CREATOR
# ==========================================
class GUIFactory(ABC):
    @abstractmethod
    def create_button(self):
        pass
    @abstractmethod
    def create_checkbox(self):
        pass
# ==========================================
# 4. CONCRETE FACTORIES
# ==========================================
# Concrete Factory
class WindowsFactory(GUIFactory):
    def create_button(self):
        return Windowsbutton()
    def create_checkbox(self):
        return Windowscheckbox()

class MacFactory(GUIFactory):
    def create_button(self):
        return Macbutton()
    def create_checkbox(self):
        return Maccheckbox()
# ==========================================
# 5. CLIENT
# ==========================================
factory = WindowsFactory()
buttongui = factory.create_button()
print(buttongui.gui())
checkbox = factory.create_checkbox()
print(checkbox.gui())
