# Customer class to represent a customer in the system
class Customer:
    # Initialize a new Customer instance
    def __init__(self, customer_id, first_name, last_name, email, phone):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        
    # Return a string representation of the Customer instance
    def __str__(self):
        return (
            f"Customer ID: {self.customer_id}, "
            f"Name: {self.first_name} {self.last_name}, "
            f"Email: {self.email}, "
            f"Phone: {self.phone}"
        )