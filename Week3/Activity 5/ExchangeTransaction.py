# ExchangeTransaction class to represent a currency exchange transaction in the system
class ExchangeTransaction:
    # Initialize a new ExchangeTransaction instance
    def __init__(self, transaction_id, customer_id, rate_id, amount, converted_amount, transaction_date):
        self.transaction_id = transaction_id
        self.customer_id = customer_id
        self.rate_id = rate_id
        self.amount = amount
        self.converted_amount = converted_amount
        self.transaction_date = transaction_date
        
    # Return a string representation of the ExchangeTransaction instance
    def __str__(self):
        return (
            f"Transaction ID: {self.transaction_id} | "
            f"Customer ID: {self.customer_id} | "
            f"Rate ID: {self.rate_id} | "
            f"Amount: {self.amount} -> Converted: {self.converted_amount} | "
            f"Date: {self.transaction_date}"
        )