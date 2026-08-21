# ExchangeRate class to represent an exchange rate in the system
class ExchangeRate:
    # Initialize a new ExchangeRate instance
    def __init__(self, rate_id, from_currency_id, to_currency_id, rate, effective_date):
        self.rate_id = rate_id
        self.from_currency_id = from_currency_id
        self.to_currency_id = to_currency_id
        self.rate = rate
        self.effective_date = effective_date

    # Calculate the converted amount based on the exchange rate
    def calculate(self, amount):
        return round(amount * self.rate, 2)