'''
Design ER diagram and develop a database for the money exchange project (with at least three entities and OOP style). 
In a README file, clearly describe how many tables you have created and justify why each table is necessary. 
Once completed, share the link to your GitHub repository. 
Project scope: The Money Exchange System should allow a exchange business to manage customers, currencies, exchange rates, and currency exchange transactions
'''
from Customer import Customer
from ExchangeRate import ExchangeRate
from ExchangeTransaction import ExchangeTransaction
import database

# User interaction functions
def user_check_exchange_rate():
    from_currency_code = input("Please enter the currency code you want to exchange from: ").strip().upper()
    from_currency_id = database.get_currency_id(from_currency_code)
    if from_currency_id is None:
        print("From currency not found.")
        return
    to_currency_code = input("Please enter the currency code you want to exchange to: ").strip().upper()
    to_currency_id = database.get_currency_id(to_currency_code)
    if to_currency_id is None:
        print("To currency not found.")
        return
    exchange_rate = database.get_exchange_rate(from_currency_id, to_currency_id)
    if exchange_rate:
        print(
            f"The exchange rate from "
            f"{from_currency_code} "
            f"to "
            f"{to_currency_code} "
            f"is: {exchange_rate.rate}"
        )
    else:
        print("Exchange rate not found.")

def user_exchange_currency(customer_id):
    from_currency_code = input("Please enter the currency code you want to exchange from: ").strip().upper()
    from_currency_id = database.get_currency_id(from_currency_code)
    to_currency_code = input("Please enter the currency code you want to exchange to: ").strip().upper()
    to_currency_id = database.get_currency_id(to_currency_code)
    if from_currency_id is None:
        print("From currency not found.")
        return
    if to_currency_id is None:
        print("To currency not found.")
        return
    try:
        amount = float(input("Please enter the amount you want to exchange: "))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Invalid amount.")
        return
    exchange_rate = database.get_exchange_rate(from_currency_id, to_currency_id)
    if exchange_rate is None:
        print("Exchange rate not found.")
        return
    converted_amount = exchange_rate.calculate(amount)
    print(
        f"The converted amount is "
        f"{converted_amount} {to_currency_code}"
    )
    transaction_date = input("Please enter the transaction date (YYYY-MM-DD): ")
    database.add_transaction(customer_id, exchange_rate.rate_id, amount, converted_amount, transaction_date)

def user_exchange_history(customer_id):
    transactions = database.get_transactions(customer_id)
    if transactions:
        for transaction in transactions:
            print(transaction)
    else:
        print("No transactions found.")

def user_operate(customer_id):
    while True:
        print("\n--- Main Menu ---")
        print("1. Check exchange rate")
        print("2. Exchange currency")
        print("3. Check exchange history")
        print("4. Exit")
        user_input = input("Please select an option: ").strip()
        if user_input == '1':
            user_check_exchange_rate()
        elif user_input == '2':
            user_exchange_currency(customer_id)
        elif user_input == '3':
            user_exchange_history(customer_id) 
        elif user_input == '4':
            print("Thank you for using the Money Exchange System. Goodbye!")
            break
        else:
            print("Invalid input.")

def user_signup():
    first_name = input("Please enter your first name: ")
    last_name = input("Please enter your last name: ")
    email = input("Please enter your email address: ")
    phone = input("Please enter your phone number: ")
    customer_id = database.add_customer(first_name, last_name, email, phone)
    if customer_id:
        print(
            f"Your customer ID is {customer_id}. "
            f"Please remember it."
        )
        user_operate(customer_id)

def user_forget_id():
    email = input("Please enter your email address to look up your ID: ")
    customer = database.get_customer_by_email(email)
    if customer:
        print(
            f"Your customer ID is: "
            f"{customer.customer_id}"
        )
        return customer.customer_id
    print("Customer not found.")
    return None

def user_login(customer_id):
    customer = database.get_customer(customer_id)
    if customer:
        print(f"Welcome back, "
            f"{customer.first_name}"
            f" {customer.last_name}!")
        user_operate(customer_id)
    else:
        print("Customer not found.")

# add sample data to the database
def add_sample_data():
    # Add currencies
    database.add_currency(
        "NZD",
        "New Zealand Dollar",
        "$"
    )
    database.add_currency(
        "USD",
        "United States Dollar",
        "$"
    )
    database.add_currency(
        "AUD",
        "Australian Dollar",
        "$"
    )
    database.add_currency(
        "EUR",
        "Euro",
        "€"
    )

    # Add customers
    database.add_customer(
        "John",
        "Smith",
        "john.smith@email.com",
        "0211234567"
    )
    database.add_customer(
        "Alice",
        "Brown",
        "alice.brown@email.com",
        "0212345678"
    )

    # Get currency IDs
    nzd_id = database.get_currency_id("NZD")
    usd_id = database.get_currency_id("USD")
    aud_id = database.get_currency_id("AUD")
    eur_id = database.get_currency_id("EUR")

    # Add exchange rates
    if nzd_id and usd_id:
        database.add_exchange_rate(nzd_id, usd_id, 0.5900, "2026-08-21")
        database.add_exchange_rate(usd_id, nzd_id, 1.6949, "2026-08-21")
    if nzd_id and aud_id:
        database.add_exchange_rate(nzd_id, aud_id, 0.9100, "2026-08-21")
        database.add_exchange_rate(aud_id, nzd_id, 1.0989, "2026-08-21")
    if nzd_id and eur_id:
        database.add_exchange_rate(nzd_id, eur_id, 0.5000, "2026-08-21")
        database.add_exchange_rate(eur_id, nzd_id, 2.0000, "2026-08-21")

def main():
    # Create tables
    database.create_customer_table()
    database.create_currency_table()
    database.create_exchange_rate_table()
    database.create_transaction_table()

    add_sample_data()

    # User access and operate
    customerid = input("Please enter your customer id. \n" \
    "If you do not have a membership number, enter 0. \n" \
    "If you forget your customer id, enter '*'. \n").strip()
    
    if customerid == '0':
        user_signup()
    elif customerid == '*':
        cid = user_forget_id()
        if cid:
            user_operate(cid)
    else:
        try:
            customer_id = int(customerid)
            user_login(customer_id)
        except ValueError:
            print("Invalid customer ID.")

if __name__ == "__main__":
    main()