def calculate_bill(price, quantity, tax):
    subtotal = price * quantity
    tax_amount = subtotal * tax
    total = subtotal + tax_amount
    return total

price = 50
quantity = 3
tax = 0.15

breakpoint()

bill = calculate_bill(price, quantity, tax)
print("Final bill:", bill)