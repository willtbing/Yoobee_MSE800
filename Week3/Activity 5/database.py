import sqlite3
from Customer import Customer
from ExchangeRate import ExchangeRate
from ExchangeTransaction import ExchangeTransaction

DATABASE_NAME = "/Users/wupei/Documents/GitHub/YoobeeMSE800/Week3/Activity 5/Activity 5.db"

def create_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

#create table functions
def create_customer_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer(
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL
        ) 
    """)
    conn.commit()
    conn.close()

def create_currency_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS currency(
            currency_id INTEGER PRIMARY KEY AUTOINCREMENT,
            currency_code TEXT NOT NULL UNIQUE,
            currency_name TEXT NOT NULL,
            symbol TEXT NOT NULL
        ) 
    """)
    conn.commit()
    conn.close()

def create_exchange_rate_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exchange_rate(
            rate_id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_currency_id INTEGER NOT NULL,
            to_currency_id INTEGER NOT NULL,
            rate REAL NOT NULL CHECK (rate > 0),
            effective_date TEXT NULL,
            FOREIGN KEY (from_currency_id) REFERENCES currency(currency_id),
            FOREIGN KEY (to_currency_id) REFERENCES currency(currency_id),
            CHECK (from_currency_id != to_currency_id)
        ) 
    """)
    conn.commit()
    conn.close()

def create_transaction_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exchange_transaction(
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            rate_id INTEGER NOT NULL,
            amount REAL NOT NULL CHECK (amount > 0),
            converted_amount REAL NOT NULL CHECK (converted_amount > 0),
            transaction_date TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
            FOREIGN KEY (rate_id) REFERENCES exchange_rate(rate_id)
        ) 
    """)
    conn.commit()
    conn.close()

#add data functions           
def add_customer(first_name, last_name, email, phone):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
                        INSERT INTO customer (first_name, last_name, email, phone) 
                        VALUES (?, ?, ?, ?)
                        """, (first_name, last_name, email, phone))
        conn.commit()
        print("Customer added successfully.")
        new_id = cursor.lastrowid
        return new_id
    except sqlite3.IntegrityError as e:
        print("Failed to add Customer:", e)
        return None
    finally:
        conn.close()
    
def add_currency(currency_code, currency_name, symbol):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
                        INSERT INTO currency (currency_code, currency_name, symbol) 
                        VALUES (?, ?, ?)
                        """, (currency_code, currency_name, symbol))
        conn.commit()
        print("Currency added successfully.")
    except sqlite3.IntegrityError as e:
        print("Failed to add Currency:", e)
    finally:
        conn.close()   

def add_exchange_rate(from_currency_id, to_currency_id, rate, effective_date):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
                        INSERT INTO exchange_rate (from_currency_id, to_currency_id, rate, effective_date) 
                        VALUES (?, ?, ?, ?)
                        """, (from_currency_id, to_currency_id, rate, effective_date))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print("Failed to add Exchange_rate:", e)
    finally:
        conn.close()   

def add_transaction(customer_id, rate_id, amount, converted_amount, transaction_date):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
                        INSERT INTO exchange_transaction (customer_id, rate_id, amount, converted_amount, transaction_date) 
                        VALUES (?, ?, ?, ?, ?)
                        """, (customer_id, rate_id, amount, converted_amount, transaction_date))
        conn.commit()
        print("Transaction recorded successfully.")
    except sqlite3.IntegrityError as e:
        print("Failed to add Exchange_transaction:", e)
    finally:
        conn.close()

#get data functions
def get_customer(customer_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT customer_id, first_name, last_name, email, phone
        FROM customer
        WHERE customer_id = ?
    """, (customer_id,))
    customer = cursor.fetchone()
    conn.close()
    if customer:
        return Customer(customer[0], customer[1], customer[2], customer[3], customer[4])
    return None

def get_customer_by_email(email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT customer_id, first_name, last_name, email, phone
        FROM customer
        WHERE email = ?
    """, (email,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Customer(row[0], row[1], row[2], row[3], row[4])
    return None 

def get_currency_id(currency_code):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT currency_id
        FROM currency
        WHERE currency_code = ?
        """, (currency_code,))
    data = cursor.fetchone()
    conn.close()
    if data:
        return data[0]
    return None

def get_exchange_rate(from_currency_id, to_currency_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT rate_id,
               from_currency_id,
               to_currency_id,
               rate,
               effective_date
        FROM exchange_rate
        WHERE from_currency_id = ?
          AND to_currency_id = ?
        ORDER BY effective_date DESC
        LIMIT 1
    """, (from_currency_id, to_currency_id))
    data = cursor.fetchone()
    conn.close()
    if data:
        return ExchangeRate(data[0], data[1], data[2], data[3], data[4])
    return None

def get_transactions(customer_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT transaction_id, customer_id, rate_id, amount, converted_amount, transaction_date
        FROM exchange_transaction
        WHERE customer_id = ?
    """, (customer_id,))
    rows = cursor.fetchall()
    conn.close()
    transactions = []
    for row in rows:
        transaction = ExchangeTransaction(row[0], row[1], row[2], row[3], row[4], row[5])
        transactions.append(transaction)    
    return transactions