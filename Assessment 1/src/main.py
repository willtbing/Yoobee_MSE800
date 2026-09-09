"""
main.py
Command-line front end for the Car Rental System (OOP version, with
Factory Method + Observer design patterns wired in via models.py).

Run: python main.py
"""

from db import init_db
from models import (
    User, Admin, Customer, Car, Booking,
    EmailNotifier, AuditLogger,
    AuthError, CarError, BookingError,
)


def prompt(msg: str) -> str:
    return input(msg).strip()


def prompt_int(msg: str) -> int:
    while True:
        try:
            return int(prompt(msg))
        except ValueError:
            print("Please enter a whole number.")


def prompt_float(msg: str) -> float:
    while True:
        try:
            return float(prompt(msg))
        except ValueError:
            print("Please enter a number.")


# ---------------------------------------------------------------- auth flows

def do_register() -> None:
    print("\n-- Register --")
    username = prompt("Username: ")
    password = prompt("Password: ")
    full_name = prompt("Full name: ")
    role = prompt("Role (customer/admin): ").lower()
    try:
        user = User.register(username, password, role, full_name)
        print(f"Registered '{user.username}' as {user.role}. You can now log in.\n")
    except AuthError as e:
        print(f"Registration failed: {e}\n")


def do_login():
    print("\n-- Log in --")
    username = prompt("Username: ")
    password = prompt("Password: ")
    try:
        user = User.authenticate(username, password)
        print(f"Welcome, {user}.\n")
        return user
    except AuthError as e:
        print(f"Login failed: {e}\n")
        return None


# --------------------------------------------------------- customer actions

def customer_view_cars(customer: Customer) -> None:
    print("\n-- Available cars --")
    cars = customer.view_available_cars()
    if not cars:
        print("No cars available right now.")
    for c in cars:
        print(f"  {c}")
    print()


def customer_book_car(customer: Customer) -> None:
    customer_view_cars(customer)
    car_id = prompt_int("Car ID to book: ")
    start_date = prompt("Start date (YYYY-MM-DD): ")
    end_date = prompt("End date (YYYY-MM-DD): ")
    notes = prompt("Notes (optional): ")
    try:
        car = Car.get_by_id(car_id)
        booking = customer.book_car(car, start_date, end_date, notes)
        print(f"\nBooking created: {booking}")
        print(f"  Base fee:      ${booking.base_fee:.2f}")
        print(f"  Extra charges: ${booking.extra_charges:.2f}")
        print(f"  Total fee:     ${booking.total_fee:.2f}")
        print("  Status: pending admin approval\n")
    except (CarError, BookingError) as e:
        print(f"Could not create booking: {e}\n")


def customer_my_bookings(customer: Customer) -> None:
    print("\n-- My bookings --")
    bookings = customer.view_my_bookings()
    if not bookings:
        print("You have no bookings yet.")
    for b in bookings:
        print(f"  {b}")
    print()


def customer_menu(customer: Customer) -> None:
    while True:
        print("--- Customer menu ---")
        print("1) View available cars")
        print("2) Book a car")
        print("3) My bookings")
        print("4) Log out")
        choice = prompt("> ")
        if choice == "1":
            customer_view_cars(customer)
        elif choice == "2":
            customer_book_car(customer)
        elif choice == "3":
            customer_my_bookings(customer)
        elif choice == "4":
            return
        else:
            print("Invalid choice.\n")


# ------------------------------------------------------------ admin actions

def admin_add_car(admin: Admin) -> None:
    print("\n-- Add car --")
    make = prompt("Make: ")
    model = prompt("Model: ")
    year = prompt_int("Year: ")
    mileage = prompt_int("Mileage: ")
    daily_rate = prompt_float("Daily rate ($): ")
    min_days = prompt_int("Minimum rent days: ")
    max_days = prompt_int("Maximum rent days: ")
    try:
        car = admin.add_car(make, model, year, mileage, daily_rate, min_days, max_days)
        print(f"Added: {car}\n")
    except CarError as e:
        print(f"Could not add car: {e}\n")


def admin_update_car(admin: Admin) -> None:
    print("\n-- Update car --")
    for c in Car.list_all():
        print(f"  {c}")
    car_id = prompt_int("Car ID to update: ")
    field = prompt(
        "Field to update (make/model/year/mileage/available_now/"
        "min_rent_days/max_rent_days/daily_rate): "
    )
    value = prompt("New value: ")
    if field in ("year", "mileage", "min_rent_days", "max_rent_days"):
        value = int(value)
    elif field == "daily_rate":
        value = float(value)
    elif field == "available_now":
        value = value.lower() in ("1", "true", "yes", "y")
    try:
        car = admin.update_car(car_id, **{field: value})
        print(f"Updated: {car}\n")
    except CarError as e:
        print(f"Could not update car: {e}\n")


def admin_delete_car(admin: Admin) -> None:
    print("\n-- Delete car --")
    for c in Car.list_all():
        print(f"  {c}")
    car_id = prompt_int("Car ID to delete: ")
    try:
        admin.delete_car(car_id)
        print(f"Deleted car #{car_id}\n")
    except CarError as e:
        print(f"Could not delete car: {e}\n")


def admin_review_bookings(admin: Admin) -> None:
    print("\n-- Pending bookings --")
    pending = Booking.list_pending()
    if not pending:
        print("No pending bookings.\n")
        return
    for b in pending:
        print(f"  {b}")
    booking_id = prompt_int("Booking ID to decide (0 to cancel): ")
    if booking_id == 0:
        return
    decision = prompt("Approve or reject? (a/r): ").lower()
    try:
        booking = Booking.get_by_id(booking_id)
        if decision == "a":
            admin.approve_booking(booking)   # triggers Observer notifications
        else:
            admin.reject_booking(booking)    # triggers Observer notifications
        print(f"Booking #{booking.id} is now '{booking.status}'.\n")
    except BookingError as e:
        print(f"Could not update booking: {e}\n")


def admin_menu(admin: Admin) -> None:
    while True:
        print("--- Admin menu ---")
        print("1) View all cars")
        print("2) Add car")
        print("3) Update car")
        print("4) Delete car")
        print("5) Review pending bookings")
        print("6) Log out")
        choice = prompt("> ")
        if choice == "1":
            for c in Car.list_all():
                print(f"  {c}")
            print()
        elif choice == "2":
            admin_add_car(admin)
        elif choice == "3":
            admin_update_car(admin)
        elif choice == "4":
            admin_delete_car(admin)
        elif choice == "5":
            admin_review_bookings(admin)
        elif choice == "6":
            return
        else:
            print("Invalid choice.\n")


# ------------------------------------------------------------------- main

def main() -> None:
    init_db()

    # --- Observer pattern setup: every Booking created from now on will
    # automatically notify these observers whenever its status changes. ---
    Booking.register_default_observer(EmailNotifier())
    Booking.register_default_observer(AuditLogger())

    print("=== Car Rental System (OOP) ===\n")
    while True:
        print("1) Register")
        print("2) Log in")
        print("3) Exit")
        choice = prompt("> ")
        if choice == "1":
            do_register()
        elif choice == "2":
            user = do_login()
            if isinstance(user, Admin):
                admin_menu(user)
            elif isinstance(user, Customer):
                customer_menu(user)
        elif choice == "3":
            print("Goodbye.")
            return
        else:
            print("Invalid choice.\n")


if __name__ == "__main__":
    main()
