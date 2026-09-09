"""
models.py
Object-oriented domain model for the Car Rental System.

Class hierarchy (per class diagram): User (abstract) <|-- Admin, User <|-- Customer;
Car; Booking.

Design patterns used:
  - Factory Method (UserFactory): centralizes creation of the correct User
    subclass (Admin vs Customer) so callers never branch on role themselves.
  - Observer (BookingObserver / Booking as subject): when a booking's status
    changes (approved/rejected), all registered observers are notified
    automatically. This also doubles as the assignment's "innovative
    feature": an automatic customer-notification system that can gain new
    notification channels (email, SMS, audit log, push...) without ever
    touching Booking's or Admin's code again.

Design note on User.login(): the class diagram shows login as a method on
User, but before authentication succeeds we don't yet know whether to build
an Admin or a Customer instance. So the practical entry point is the
classmethod User.authenticate(username, password), which looks up the row,
uses UserFactory to build the correct subclass, and verifies the password via
the protected _verify_password() helper.
"""

from __future__ import annotations

import hashlib
import os
import sqlite3
from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List, Optional

from db import get_connection

PBKDF2_ITERATIONS = 200_000
# Mileage (in miles) above which a car is considered "high mileage" and
# incurs an extra surcharge when booked. 50,000 miles reflects realistic
# wear-and-tear thresholds for rental fleet vehicles.
HIGH_MILEAGE_THRESHOLD = 50_000

# Flat surcharge (in dollars) added to a booking's total_fee for every
# complete 100 miles a car's mileage exceeds HIGH_MILEAGE_THRESHOLD.
HIGH_MILEAGE_SURCHARGE_PER_100_MI = 2.00


class AuthError(Exception):
    pass


class CarError(Exception):
    pass


class BookingError(Exception):
    pass


def _hash_password(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS).hex()


def _parse_date(s: str):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        raise BookingError(f"Invalid date '{s}', expected YYYY-MM-DD")


# --------------------------------------------------------------------------- User

class User(ABC):
    """Abstract base for Admin and Customer. Holds shared identity fields."""

    role: str = None  # set by subclasses ("admin" / "customer")

    def __init__(self, id: int, username: str, password_hash: str, salt: str, full_name: str):
        if type(self) is User:
            raise TypeError("User is abstract; instantiate Admin or Customer instead")
        self.id = id
        self.username = username
        self._password_hash = password_hash
        self._salt = salt
        self.full_name = full_name

    def _verify_password(self, password: str) -> bool:
        """Protected helper: recompute the hash and compare."""
        candidate = _hash_password(password, bytes.fromhex(self._salt))
        return candidate == self._password_hash

    @classmethod
    def register(cls, username: str, password: str, role: str, full_name: str = "") -> "User":
        """Create and persist a new Admin or Customer."""
        if role not in ("admin", "customer"):
            raise AuthError("role must be 'admin' or 'customer'")
        if not username or not password:
            raise AuthError("username and password are required")

        salt = os.urandom(16)
        password_hash = _hash_password(password, salt)

        with get_connection() as conn:
            try:
                cur = conn.execute(
                    """INSERT INTO users (username, password_hash, salt, role, full_name)
                       VALUES (?, ?, ?, ?, ?)""",
                    (username, password_hash, salt.hex(), role, full_name),
                )
                conn.commit()
            except Exception:
                raise AuthError(f"Username '{username}' is already taken")

        # --- Factory Method in action: caller doesn't branch on role itself ---
        return UserFactory.create_user(
            role, id=cur.lastrowid, username=username, password_hash=password_hash,
            salt=salt.hex(), full_name=full_name,
        )

    @classmethod
    def authenticate(cls, username: str, password: str) -> "User":
        """Look up the user, build the right subclass via UserFactory, and
        verify the password. This is the practical realization of login()."""
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if row is None:
            raise AuthError("Invalid username or password")

        # --- Factory Method in action again ---
        user = UserFactory.create_user(
            row["role"], id=row["id"], username=row["username"], password_hash=row["password_hash"],
            salt=row["salt"], full_name=row["full_name"],
        )

        if not user._verify_password(password):
            raise AuthError("Invalid username or password")

        return user

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"


class Admin(User):
    role = "admin"

    def add_car(self, make: str, model: str, year: int, mileage: int, daily_rate: float,
                min_rent_days: int = 1, max_rent_days: int = 30) -> "Car":
        if min_rent_days < 1 or max_rent_days < min_rent_days:
            raise CarError("Invalid min/max rent day range")
        if daily_rate <= 0:
            raise CarError("daily_rate must be positive")

        with get_connection() as conn:
            cur = conn.execute(
                """INSERT INTO cars (make, model, year, mileage, available_now,
                                      min_rent_days, max_rent_days, daily_rate)
                   VALUES (?, ?, ?, ?, 1, ?, ?, ?)""",
                (make, model, year, mileage, min_rent_days, max_rent_days, daily_rate),
            )
            conn.commit()
        return Car.get_by_id(cur.lastrowid)

    def update_car(self, car_id: int, **fields) -> "Car":
        allowed = {"make", "model", "year", "mileage", "available_now",
                   "min_rent_days", "max_rent_days", "daily_rate"}
        updates = {k: v for k, v in fields.items() if k in allowed}
        if not updates:
            raise CarError("No valid fields to update")
        if "available_now" in updates:
            updates["available_now"] = int(bool(updates["available_now"]))

        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [car_id]

        with get_connection() as conn:
            cur = conn.execute(f"UPDATE cars SET {set_clause} WHERE id = ?", values)
            conn.commit()
            if cur.rowcount == 0:
                raise CarError(f"No car with id {car_id}")
        return Car.get_by_id(car_id)

    def delete_car(self, car_id: int) -> None:
        with get_connection() as conn:
            try:
                cur = conn.execute("DELETE FROM cars WHERE id = ?", (car_id,))
                conn.commit()
            except sqlite3.IntegrityError:
                # The car has one or more booking records referencing it (past
                # or present). Deleting it would corrupt those bookings'
                # car_id, so the database (correctly) refuses. Rather than
                # leaking a raw sqlite3 error to the CLI, surface a message
                # that tells the admin what actually happened and what to do
                # instead: mark the car unavailable rather than deleting it,
                # which preserves booking history for auditing.
                raise CarError(
                    f"Cannot delete car #{car_id}: it has existing booking "
                    "records. Mark it unavailable instead "
                    "(update_car(available_now=False)) to keep booking "
                    "history intact."
                )
            if cur.rowcount == 0:
                raise CarError(f"No car with id {car_id}")

    def approve_booking(self, booking: "Booking") -> None:
        booking._decide(approve=True)

    def reject_booking(self, booking: "Booking") -> None:
        booking._decide(approve=False)


class Customer(User):
    role = "customer"

    def view_available_cars(self) -> List["Car"]:
        return Car.list_all(only_available=True)

    def book_car(self, car: "Car", start_date: str, end_date: str, notes: str = "") -> "Booking":
        return Booking._create(customer=self, car=car, start_date=start_date,
                                end_date=end_date, notes=notes)

    def view_my_bookings(self) -> List["Booking"]:
        return Booking.list_by_user(self)


# --------------------------------------------------------- Factory Method pattern

class UserFactory:
    """Factory Method pattern: the single place in the codebase that knows
    how to turn a role string into the correct User subclass. Adding a new
    role in the future (e.g. 'fleet_manager') means changing ONE method here,
    not hunting down every `if role == ...` scattered across the codebase.
    """

    @staticmethod
    def create_user(role: str, **kwargs) -> "User":
        if role == "admin":
            return Admin(**kwargs)
        elif role == "customer":
            return Customer(**kwargs)
        raise AuthError(f"Unknown role: {role}")


# --------------------------------------------------------------------------- Car

class Car:
    def __init__(self, id: int, make: str, model: str, year: int, mileage: int,
                 available_now: bool, min_rent_days: int, max_rent_days: int, daily_rate: float):
        self.id = id
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.available_now = available_now
        self.min_rent_days = min_rent_days
        self.max_rent_days = max_rent_days
        self.daily_rate = daily_rate

    @staticmethod
    def _from_row(row) -> "Car":
        return Car(id=row["id"], make=row["make"], model=row["model"], year=row["year"],
                    mileage=row["mileage"], available_now=bool(row["available_now"]),
                    min_rent_days=row["min_rent_days"], max_rent_days=row["max_rent_days"],
                    daily_rate=row["daily_rate"])

    @classmethod
    def get_by_id(cls, car_id: int) -> "Car":
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM cars WHERE id = ?", (car_id,)).fetchone()
        if row is None:
            raise CarError(f"No car with id {car_id}")
        return cls._from_row(row)

    @classmethod
    def list_all(cls, only_available: bool = False) -> List["Car"]:
        query = "SELECT * FROM cars"
        if only_available:
            query += " WHERE available_now = 1"
        query += " ORDER BY id"
        with get_connection() as conn:
            rows = conn.execute(query).fetchall()
        return [cls._from_row(r) for r in rows]

    def is_available_for(self, start_date: str, end_date: str) -> bool:
        if not self.available_now:
            return False
        with get_connection() as conn:
            row = conn.execute(
                """SELECT 1 FROM bookings
                   WHERE car_id = ? AND status IN ('pending', 'approved')
                     AND start_date < ? AND end_date > ?
                   LIMIT 1""",
                (self.id, end_date, start_date),
            ).fetchone()
        return row is None

    def calculate_fee(self, start_date: str, end_date: str) -> tuple[float, float, float]:
        start = _parse_date(start_date)
        end = _parse_date(end_date)
        if start < date.today():
            raise BookingError("start_date cannot be in the past")
        days = (end - start).days
        if days <= 0:
            raise BookingError("end_date must be after start_date")
        if days < self.min_rent_days:
            raise BookingError(f"Rental period too short: minimum is {self.min_rent_days} day(s)")
        if days > self.max_rent_days:
            raise BookingError(f"Rental period too long: maximum is {self.max_rent_days} day(s)")

        base_fee = self.daily_rate * days
        extra_charges = 0.0
        if self.mileage > HIGH_MILEAGE_THRESHOLD:
            over = self.mileage - HIGH_MILEAGE_THRESHOLD
            extra_charges = (over // 100) * HIGH_MILEAGE_SURCHARGE_PER_100_MI

        return base_fee, extra_charges, base_fee + extra_charges

    def __str__(self) -> str:
        avail = "available" if self.available_now else "unavailable"
        return (f"#{self.id} {self.year} {self.make} {self.model} | {self.mileage} mi | "
                f"${self.daily_rate:.2f}/day | rent {self.min_rent_days}-{self.max_rent_days} days | {avail}")


# --------------------------------------------------------------- Observer pattern

class BookingObserver(ABC):
    """Observer interface. Any class that wants to react to a booking's
    status changing (e.g. send an email, send an SMS, write an audit log)
    implements update()."""

    @abstractmethod
    def update(self, booking: "Booking") -> None:
        ...


class EmailNotifier(BookingObserver):
    """Concrete observer: simulates emailing the customer when their
    booking is approved or rejected."""

    def update(self, booking: "Booking") -> None:
        print(f"[Email] Booking #{booking.id}: status changed to '{booking.status}'. "
              f"Notifying customer (user_id={booking.user_id}).")


class SMSNotifier(BookingObserver):
    """Concrete observer: simulates an SMS notification."""

    def update(self, booking: "Booking") -> None:
        print(f"[SMS] Your booking #{booking.id} is now '{booking.status}'.")


class AuditLogger(BookingObserver):
    """Concrete observer: writes a timestamped audit trail entry."""

    def update(self, booking: "Booking") -> None:
        print(f"[Audit] {datetime.now().isoformat(timespec='seconds')} "
              f"- booking #{booking.id} -> {booking.status}")


# --------------------------------------------------------------------------- Booking

class Booking:
    """Subject in the Observer pattern: notifies all registered observers
    whenever its status changes via approve()/reject()."""

    # Observers registered here apply to every Booking instance by default
    # (e.g. wired up once at application startup in main.py).
    _default_observers: List[BookingObserver] = []

    def __init__(self, id: int, user_id: int, car_id: int, start_date: str, end_date: str,
                 status: str, base_fee: float, extra_charges: float, total_fee: float,
                 notes: Optional[str], decided_at: Optional[str] = None):
        self.id = id
        self.user_id = user_id
        self.car_id = car_id
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.base_fee = base_fee
        self.extra_charges = extra_charges
        self.total_fee = total_fee
        self.notes = notes
        self.decided_at = decided_at
        self._observers: List[BookingObserver] = list(Booking._default_observers)

    @classmethod
    def register_default_observer(cls, observer: BookingObserver) -> None:
        """Wire up an observer that will be attached to every future Booking
        instance (call once at application startup)."""
        cls._default_observers.append(observer)

    def add_observer(self, observer: BookingObserver) -> None:
        """Attach an observer to this specific booking only."""
        self._observers.append(observer)

    def _notify_observers(self) -> None:
        for observer in self._observers:
            observer.update(self)

    @staticmethod
    def _from_row(row) -> "Booking":
        return Booking(id=row["id"], user_id=row["user_id"], car_id=row["car_id"],
                        start_date=row["start_date"], end_date=row["end_date"], status=row["status"],
                        base_fee=row["base_fee"], extra_charges=row["extra_charges"],
                        total_fee=row["total_fee"], notes=row["notes"], decided_at=row["decided_at"])

    @classmethod
    def _create(cls, customer: Customer, car: Car, start_date: str, end_date: str,
                notes: str = "") -> "Booking":
        if not car.is_available_for(start_date, end_date):
            raise BookingError(f"Car #{car.id} is not available for that date range")

        base_fee, extra_charges, total_fee = car.calculate_fee(start_date, end_date)

        with get_connection() as conn:
            cur = conn.execute(
                """INSERT INTO bookings (user_id, car_id, start_date, end_date, status,
                                          base_fee, extra_charges, total_fee, notes)
                   VALUES (?, ?, ?, ?, 'pending', ?, ?, ?, ?)""",
                (customer.id, car.id, start_date, end_date, base_fee, extra_charges, total_fee, notes),
            )
            conn.commit()
        return cls.get_by_id(cur.lastrowid)

    @classmethod
    def get_by_id(cls, booking_id: int) -> "Booking":
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,)).fetchone()
        if row is None:
            raise BookingError(f"No booking with id {booking_id}")
        return cls._from_row(row)

    @classmethod
    def list_by_user(cls, user: User) -> List["Booking"]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM bookings WHERE user_id = ? ORDER BY id", (user.id,)
            ).fetchall()
        return [cls._from_row(r) for r in rows]

    @classmethod
    def list_pending(cls) -> List["Booking"]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM bookings WHERE status = 'pending' ORDER BY id"
            ).fetchall()
        return [cls._from_row(r) for r in rows]

    @classmethod
    def list_all(cls) -> List["Booking"]:
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM bookings ORDER BY id").fetchall()
        return [cls._from_row(r) for r in rows]

    def is_pending(self) -> bool:
        return self.status == "pending"

    def approve(self) -> None:
        """Public per the class diagram; prefer calling Admin.approve_booking(booking)."""
        self._decide(approve=True)

    def reject(self) -> None:
        """Public per the class diagram; prefer calling Admin.reject_booking(booking)."""
        self._decide(approve=False)

    def _decide(self, approve: bool) -> None:
        if not self.is_pending():
            raise BookingError(f"Booking #{self.id} is already '{self.status}'")
        new_status = "approved" if approve else "rejected"
        with get_connection() as conn:
            conn.execute(
                "UPDATE bookings SET status = ?, decided_at = datetime('now') WHERE id = ?",
                (new_status, self.id),
            )
            conn.commit()
        self.status = new_status
        self._notify_observers()  # --- Observer pattern in action ---

    def __str__(self) -> str:
        return (f"Booking #{self.id} | car #{self.car_id} | {self.start_date} -> {self.end_date} "
                f"| status={self.status} | total=${self.total_fee:.2f}")
