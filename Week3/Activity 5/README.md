---

## 🗄️ Database Tables & Justification

A total of **4 database tables** have been created in SQLite. Below is a detailed description and justification for each table:

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