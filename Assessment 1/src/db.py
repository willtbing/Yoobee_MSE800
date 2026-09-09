"""
db.py
Database connection helper and schema initialization for the Car Rental System.
"""

import sqlite3
import sys
from pathlib import Path

# DB_PATH must point next to the running program, not next to this source
# file. Under normal `python main.py` execution these are the same thing,
# but a PyInstaller --onefile executable unpacks db.py into a temporary
# folder that is deleted when the program exits — if DB_PATH used
# __file__ directly in that case, the database would be silently recreated
# empty on every launch. sys.frozen is set by PyInstaller at runtime to
# signal this situation; sys.executable then points at the actual
# executable file the user launched, which is what we want the database to
# sit next to instead.
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

DB_PATH = BASE_DIR / "car_rental.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    username        TEXT NOT NULL UNIQUE,
    password_hash   TEXT NOT NULL,
    salt            TEXT NOT NULL,
    role            TEXT NOT NULL CHECK (role IN ('admin', 'customer')),
    full_name       TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS cars (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    make                TEXT NOT NULL,
    model               TEXT NOT NULL,
    year                INTEGER NOT NULL,
    mileage             INTEGER NOT NULL DEFAULT 0,
    available_now       INTEGER NOT NULL DEFAULT 1,
    min_rent_days       INTEGER NOT NULL DEFAULT 1,
    max_rent_days       INTEGER NOT NULL DEFAULT 30,
    daily_rate          REAL NOT NULL,
    created_at          TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS bookings (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL REFERENCES users(id),
    car_id          INTEGER NOT NULL REFERENCES cars(id),
    start_date      TEXT NOT NULL,
    end_date        TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'pending'
                        CHECK (status IN ('pending', 'approved', 'rejected', 'cancelled', 'completed')),
    base_fee        REAL NOT NULL,
    extra_charges   REAL NOT NULL DEFAULT 0,
    total_fee       REAL NOT NULL,
    notes           TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    decided_at      TEXT
);
"""


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(SCHEMA)
        conn.commit()


if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
