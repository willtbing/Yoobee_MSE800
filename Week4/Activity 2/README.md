## Activity Diagram – Currency Exchange System

This diagram represents the **main workflow of a currency exchange system**. It uses two swimlanes to show the responsibilities of the **Customer** and **Admin**.

### 1. Customer Process

The customer workflow is:

1. **Check whether the customer already has an account**

   * **No** → The customer can **Sign up**.
   * **Yes** → Check whether the customer remembers their customer ID.
2. If the customer does not remember the ID, they can **Check Customer ID**.
3. The system checks whether the customer ID exists.
4. If the ID is valid, the customer can **Log in**.
5. After logging in, the customer can:

   * **Check currency rate**
   * **Exchange currency**
   * **Check exchange history**

### 2. Admin Process

The Admin is responsible for managing the system data:

* **Add customer** – create a new customer account.
* **Add currency** – add a supported currency.
* **Add currency rate** – add or update exchange-rate information.
* **Add currency exchange record** – record a currency exchange transaction.

### 3. Overall Functionality

The diagram represents the complete workflow of the currency exchange application:

```text
Customer
   ↓
Check Account
   ↓
Sign Up / Check Customer ID
   ↓
Login
   ↓
┌─────────────────────────┐
│ Check Currency Rate     │
│ Exchange Currency       │
│ Check Exchange History  │
└─────────────────────────┘

Admin
   ↓
┌─────────────────────────┐
│ Add Customer            │
│ Add Currency            │
│ Add Currency Rate       │
│ Add Exchange Record     │
└─────────────────────────┘
```

Overall, the activity diagram shows how **customers access and use the currency exchange services**, while **administrators maintain customers, currencies, exchange rates, and transaction records**.
