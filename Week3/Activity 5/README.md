# Week 3 — Activity 5: Money Exchange System

This README documents the Week3 / Activity 5 implementation for a simple Money Exchange System. It describes the database tables created, why each table is necessary, the relationships between them, and the structure and responsibilities of each program file in this directory.

Folder contents (key files):

- [main.py](</Users/wupei/Documents/GitHub/YoobeeMSE800.worktrees/week3-activity5-readme-docs/Week3/Activity 5/main.py>)
- [database.py](</Users/wupei/Documents/GitHub/YoobeeMSE800.worktrees/week3-activity5-readme-docs/Week3/Activity 5/database.py>)
- [Customer.py](</Users/wupei/Documents/GitHub/YoobeeMSE800.worktrees/week3-activity5-readme-docs/Week3/Activity 5/Customer.py>)
- [ExchangeRate.py](</Users/wupei/Documents/GitHub/YoobeeMSE800.worktrees/week3-activity5-readme-docs/Week3/Activity 5/ExchangeRate.py>)
- [ExchangeTransaction.py](</Users/wupei/Documents/GitHub/YoobeeMSE800.worktrees/week3-activity5-readme-docs/Week3/Activity 5/ExchangeTransaction.py>)
- [Activity 5.db](</Users/wupei/Documents/GitHub/YoobeeMSE800.worktrees/week3-activity5-readme-docs/Week3/Activity 5/Activity 5.db>) (SQLite database file)
- [ER diagram.svg](</Users/wupei/Documents/GitHub/YoobeeMSE800.worktrees/week3-activity5-readme-docs/Week3/Activity 5/ER diagram.svg>)


## Database: tables, purposes and justification

Total tables created: 4

1) customer
- Purpose: store registered customer records.
- Key fields: customer_id (PK), first_name, last_name, email (UNIQUE), phone.
- Why needed: Customers must be identifiable and contactable. Transactions must link to customers for audit and business reporting.

2) currency
- Purpose: master list of supported currencies.
- Key fields: currency_id (PK), currency_code (UNIQUE), currency_name, symbol.
- Why needed: Normalises currency metadata so that currency names/codes are stored once and referenced elsewhere. Avoids duplication and simplifies adding/removing supported currencies.

3) exchange_rate
- Purpose: store exchange rates between currencies, including effective dates.
- Key fields: rate_id (PK), from_currency_id (FK -> currency.currency_id), to_currency_id (FK -> currency.currency_id), rate (REAL, >0), effective_date.
- Why needed: Exchange rates change over time and may differ per currency pair. Storing rates separately allows historical auditing and selecting the correct rate used for a transaction.

4) exchange_transaction
- Purpose: ledger of currency exchange transactions.
- Key fields: transaction_id (PK), customer_id (FK -> customer.customer_id), rate_id (FK -> exchange_rate.rate_id), amount, converted_amount, transaction_date.
- Why needed: Records every exchange with links to the customer and the exact exchange rate used, enabling accurate receipts and audit trails.


## Relationships between tables

- customer (1) ←——— (many) exchange_transaction
  - Each transaction is performed by one customer; a customer can have many transactions.

- currency (1) ←— (many) exchange_rate (via from_currency_id)
- currency (1) ←— (many) exchange_rate (via to_currency_id)
  - Each exchange_rate references two currency rows (source and target). A currency can appear in many rate pairs.

- exchange_rate (1) ←——— (many) exchange_transaction
  - Each transaction records which exchange_rate (rate_id) was used. This preserves the exact multiplier and effective_date used for that transaction.

These relationships are implemented using SQLite FOREIGN KEY constraints in [database.py](</Users/wupei/Documents/GitHub/YoobeeMSE800.worktrees/week3-activity5-readme-docs/Week3/Activity 5/database.py>):
- exchange_rate.from_currency_id -> currency.currency_id
- exchange_rate.to_currency_id -> currency.currency_id
- exchange_transaction.customer_id -> customer.customer_id
- exchange_transaction.rate_id -> exchange_rate.rate_id


## Program files: structure and content

Below is a per-file description describing the purpose, main classes/functions, and expected behavior. Links point to the files in this folder.

1) [main.py](</Users/wupei/Documents/GitHub/YoobeeMSE800.worktrees/week3-activity5-readme-docs/Week3/Activity 5/main.py>)
- Purpose: user-facing script that provides a CLI for the Money Exchange System.
- Key imports: Customer, ExchangeRate, ExchangeTransaction classes and database helper module.
- Major functions:
  - user_check_exchange_rate(): prompts for source and target currency codes, looks up IDs via database.get_currency_id, and displays the latest exchange rate fetched with database.get_exchange_rate.
  - user_exchange_currency(customer_id): gets currencies and amount from user, validates input, finds rate, calculates converted amount via ExchangeRate.calculate(), and records the transaction via database.add_transaction().
  - user_exchaange_history(customer_id): retrieves transactions for a customer via database.get_transactions() and prints each.
  - user_operate(customer_id): main menu loop for logged-in customers (options: check rate, exchange, history, exit).
  - user_signup(): gathers customer details and creates a customer using database.add_customer(), then enters user_operate().
  - user_forget_id(): finds a customer by email via database.get_customer_by_email() and returns their customer_id.
  - user_login(customer_id): fetches customer via database.get_customer() and enters user_operate().
  - add_sample_data(): helper to populate currencies, customers and example exchange rates used for demo/testing.
  - main(): creates tables by calling the database.create_* functions, adds sample data, and accepts initial user ID input to route the user to signup/login/lookup.
- Notes: Input validation is done for numeric amount and presence of currencies and rates. Transactions are stored with the provided transaction_date string.

2) [database.py](</Users/wupei/Documents/GitHub/YoobeeMSE800.worktrees/week3-activity5-readme-docs/Week3/Activity 5/database.py>)
- Purpose: encapsulates all SQLite database interactions (schema creation, CRUD operations, lookups).
- Important constants: DATABASE_NAME — absolute path to the SQLite file used by this script.
- Connection helper:
  - create_connection(): opens sqlite3 connection and ensures PRAGMA foreign_keys = ON.
- Schema creation functions (called from main.py):
  - create_customer_table()
  - create_currency_table()
  - create_exchange_rate_table() — includes checks: rate > 0 and from != to.
  - create_transaction_table() — ensures amount and converted_amount > 0 and contains FKs.
- Data manipulation functions:
  - add_customer(first_name, last_name, email, phone) -> returns new customer_id or None on failure.
  - add_currency(currency_code, currency_name, symbol)
  - add_exchange_rate(from_currency_id, to_currency_id, rate, effective_date)
  - add_transaction(customer_id, rate_id, amount, converted_amount, transaction_date)
- Read/query functions:
  - get_customer(customer_id) -> Customer object or None
  - get_customer_by_email(email) -> Customer object or None
  - get_currency_id(currency_code) -> currency_id or None
  - get_exchange_rate(from_currency_id, to_currency_id) -> ExchangeRate object or None (returns latest by effective_date)
  - get_transactions(customer_id) -> list of ExchangeTransaction objects
- Notes: Exceptions (e.g. sqlite3.IntegrityError) are caught and printed; functions return None or empty lists as appropriate.

3) [Customer.py](</Users/wupei/Documents/GitHub/YoobeeMSE800.worktrees/week3-activity5-readme-docs/Week3/Activity 5/Customer.py>)
- Purpose: simple model class representing a customer entity.
- Class: Customer
  - __init__(customer_id, first_name, last_name, email, phone)
  - __str__(): human-readable representation used when printing a fetched customer.

4) [ExchangeRate.py](</Users/wupei/Documents/GitHub/YoobeeMSE800.worktrees/week3-activity5-readme-docs/Week3/Activity 5/ExchangeRate.py>)
- Purpose: model class that represents an exchange rate record and provides conversion logic.
- Class: ExchangeRate
  - __init__(rate_id, from_currency_id, to_currency_id, rate, effective_date)
  - calculate(amount): returns amount * rate rounded to 2 decimal places.

5) [ExchangeTransaction.py](</Users/wupei/Documents/GitHub/YoobeeMSE800.worktrees/week3-activity5-readme-docs/Week3/Activity 5/ExchangeTransaction.py>)
- Purpose: model class representing a stored exchange transaction.
- Class: ExchangeTransaction
  - __init__(transaction_id, customer_id, rate_id, amount, converted_amount, transaction_date)
  - __str__(): human-readable transaction summary used when printing transaction history.

6) [Activity 5.db](</Users/wupei/Documents/GitHub/YoobeeMSE800.worktrees/week3-activity5-readme-docs/Week3/Activity 5/Activity 5.db>)
- The SQLite database file created when the application runs (path used by database.py). It persists the tables and sample data.

7) [ER diagram.svg](</Users/wupei/Documents/GitHub/YoobeeMSE800.worktrees/week3-activity5-readme-docs/Week3/Activity 5/ER diagram.svg>)
- Visual entity-relationship diagram illustrating the four tables and their foreign-key relationships.


## How the pieces work together (example flow)

1. main.py calls database.create_* functions to ensure the schema exists and then add_sample_data().
2. A user signs up (user_signup) => main.py calls database.add_customer() to persist the customer and receives a customer_id.
3. When a user exchanges currency (user_exchange_currency), main.py uses database.get_currency_id() and database.get_exchange_rate() to fetch the correct rate, uses ExchangeRate.calculate() to compute converted amount, then calls database.add_transaction() to persist the exchange using the customer_id and rate_id.
4. Transaction history (user_exchaange_history) uses database.get_transactions() which returns ExchangeTransaction objects for display.


## Notes, assumptions and potential improvements

- Dates are stored as TEXT (ISO YYYY-MM-DD). For richer queries consider storing as ISO8601 timestamps and using SQL date functions.
- No separate `Currency` class file was implemented beyond the currency table; if UI or logic grows, adding a Currency model class would improve parity with other entities.
- Input validation and error handling are basic; production code should validate formats (emails, phone numbers) and use stronger error reporting.
- Concurrency and transaction handling are not implemented beyond simple commits; consider using transactions when performing multi-step updates.


If any additional details or a different README format (e.g., including UML or SQL DDL) are needed, say which format is preferred and updates will be made.
### 1. `customer`
* **Purpose**: Stores information about registered clients using the money exchange service.
* **Fields**:
  * `customer_id` (INTEGER, PK, AUTOINCREMENT): Unique identifier for each customer.
  * `first_name` (TEXT, NOT NULL): Customer's first name.
  * `last_name` (TEXT, NOT NULL): Customer's last name.
  * `email` (TEXT, NOT NULL, UNIQUE): Customer's contact email, used for ID lookup.
  * `phone` (TEXT, NOT NULL): Customer's contact phone number.
* **Justification**: Essential for business compliance, record keeping, and personalized transaction tracking. Identifying customers allows the business to associate exchange transactions with specific individuals.

### 2. `currency`
* **Purpose**: Stores master records of all supported currencies in the exchange system.
* **Fields**:
  * `currency_id` (INTEGER, PK, AUTOINCREMENT): Unique internal key for currency.
  * `currency_code` (TEXT, NOT NULL, UNIQUE): 3-letter ISO code (e.g., `USD`, `NZD`, `EUR`).
  * `currency_name` (TEXT, NOT NULL): Full descriptive name (e.g., `United States Dollar`).
  * `symbol` (TEXT, NOT NULL): Currency symbol (e.g., `$`, `€`).
* **Justification**: Separating currencies into a dedicated lookup table normalizes currency data across the database, preventing duplicated text strings (like repeated `"New Zealand Dollar"`) and enabling centralized management of supported currencies.

### 3. `exchange_rate`
* **Purpose**: Tracks conversion rates between base (`from_currency`) and target (`to_currency`) currencies along with effective dates.
* **Fields**:
  * `rate_id` (INTEGER, PK, AUTOINCREMENT): Unique identifier for each rate entry.
  * `from_currency_id` (INTEGER, FK -> `currency.currency_id`): Source currency.
  * `to_currency_id` (INTEGER, FK -> `currency.currency_id`): Destination currency.
  * `rate` (REAL, NOT NULL, CHECK > 0): Conversion multiplier rate.
  * `effective_date` (TEXT): Date/Timestamp when this rate applies.
* **Justification**: Exchange rates fluctuate constantly. Storing rates in a dedicated table allows historical tracking of exchange rates over time and supports multi-currency pairs without modifying transaction code.

### 4. `exchange_transaction`
* **Purpose**: Records individual currency exchange transactions conducted by customers.
* **Fields**:
  * `transaction_id` (INTEGER, PK, AUTOINCREMENT): Unique receipt/transaction ID.
  * `customer_id` (INTEGER, FK -> `customer.customer_id`): Customer who made the exchange.
  * `rate_id` (INTEGER, FK -> `exchange_rate.rate_id`): The exact exchange rate used.
  * `amount` (REAL, NOT NULL, CHECK > 0): Principal amount sold in source currency.
  * `converted_amount` (REAL, NOT NULL, CHECK > 0): Total received in target currency.
  * `transaction_date` (TEXT, NOT NULL): Date when the exchange occurred.
* **Justification**: Acts as the central transaction ledger linking customers to the exchange rates used. Linking directly to `rate_id` maintains an accurate audit trail of historical exchanges and calculation metrics.

---

## 🏗️ Project Architecture & OOP Integration

The application bridges SQLite database operations with Object-Oriented Python classes:

* **`Customer` Class**: Represents client objects and formats customer information (`__str__`).
* **`Currency` Class**: Encapsulates currency attributes and display formatting.
* **`ExchangeRate` Class**: Models conversion logic (`calculate()` method) between currency pairs.
* **`ExchangeTransaction` Class**: Enforces transaction history formatting and encapsulation.

---