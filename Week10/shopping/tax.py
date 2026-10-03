from shop import calculate_price


def get_tax_rate():
    """Pretend to call an external tax service. Mocked in tests."""
    raise RuntimeError("tax service is not available")


def total_with_tax(price, quantity):
    subtotal = calculate_price(price, quantity)
    rate = get_tax_rate()
    return round(subtotal * (1 + rate), 2)
