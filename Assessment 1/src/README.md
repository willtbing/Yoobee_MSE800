# Car Rental System

A command-line Car Rental System built for MSE800 Professional Software Engineering
(Assignment 1 — Object-Oriented Programming Assignment), implemented in Python with
SQLite as the persistence layer.

It supports two roles — **Customer** and **Admin** — and covers user registration/login,
car fleet management, rental booking with automatic fee calculation, and an
admin approval workflow with automatic (Observer-pattern-based) notifications.

For the full design rationale, UML diagrams, design patterns, and software evolution
plan, see the accompanying `Car_Rental_System_Report.pdf`.

---

## 1. Requirements

- **Python 3.10 or later** (uses modern type-hint syntax such as `tuple[float, float, float]`
  and `from __future__ import annotations`)
- No third-party packages required — the system only uses Python's standard library
  (`sqlite3`, `hashlib`, `abc`, `datetime`, `os`)

Check your Python version:

```bash
python3 --version
```

## 2. Installation

*(This section applies if you are running from source — Option A in Section 3.
If you have the pre-built executable, skip straight to Option B and no
installation is needed.)*

1. Download or clone the project, which is organised into two folders:
   - `src/` — the source code (`db.py`, `models.py`, `main.py`)
   - `doc/` — the design report (`Car_Rental_System_Report.pdf`) and all UML diagrams
2. No `pip install` step is required — there are no external dependencies.
3. (Optional) If you want to start from a clean database, make sure no `car_rental.db`
   file already exists inside `src/` — one will be created there automatically the
   first time you run the program (see Section 3).

## 3. Running the System

There are two ways to run this system, depending on which files you have.

### Option A — Running from source (requires Python 3.10+)

From a terminal, `cd` into the `src/` folder and run:

```bash
cd src
python3 main.py
```

On first run, this automatically creates `src/car_rental.db` with the required
tables (`users`, `cars`, `bookings`). On subsequent runs, the existing database
file is reused, so your data persists between sessions.

### Option B — Running the pre-built executable (no Python required)

If you received the `CarRentalSystem` release build instead of (or in addition
to) the source code, no installation is required at all:

1. Unzip the release build.
2. Double-click `CarRentalSystem` (or run `./CarRentalSystem` from a terminal
   inside that folder).
3. **On macOS**, the first time you run it you will likely see a warning that
   the app "cannot be opened because the developer cannot be verified" — this
   is expected for an unsigned build produced with PyInstaller, not a sign of
   a corrupted file. To proceed: right-click (or Control-click) the
   `CarRentalSystem` file, choose **Open**, then confirm **Open** again in the
   dialog that appears. You only need to do this once.
4. A `car_rental.db` file will be created in the same folder as the
   executable the first time you run it, and reused on every run after that.

Both options run the exact same program and produce the same menu and
behaviour described below — the only difference is whether Python is
installed on your machine or not.

You will see a menu:

```
=== Car Rental System (OOP) ===

1) Register
2) Log in
3) Exit
```

### 3.1 First-time setup — create an Admin account

The database starts empty, so the very first thing you should do is register an
Admin account so you can add cars to the fleet:

1. Choose `1) Register`.
2. Enter a username and password of your choice.
3. Enter a full name (optional — press Enter to leave blank).
4. When asked for a role, type `admin`.
5. Choose `2) Log in` and sign in with the account you just created.
6. From the Admin menu, choose `2) Add car` and fill in the car's details
   (make, model, year, mileage, daily rate, minimum/maximum rental days).

### 3.2 Everyday use — as a Customer

1. Register again with role `customer` (a separate account from the Admin one —
   the system does not let you register the same username twice).
2. Log in and use the Customer menu to browse available cars, book a car for a
   date range, and view the status of your bookings.

### 3.3 Approving or rejecting a booking

Log back in as the Admin account, choose `5) Review pending bookings`, select a
booking ID, and choose to approve or reject it. You will see simulated
email/audit-log notifications printed to the console at this point — these
represent the notification system described in the report's Innovative Solution
section (Section 5).

### 3.4 Exiting

Choose `3) Exit` from the main menu, or press `Ctrl+C` at any time.

## 4. Project Files

| File | Purpose |
|---|---|
| `src/main.py` | The command-line interface (presentation layer). Prints menus, reads user input, and calls methods on the domain objects in `models.py`. Contains no business logic of its own. |
| `src/models.py` | The domain layer. Defines the `User` (abstract) / `Admin` / `Customer` class hierarchy, `Car`, `Booking`, the `UserFactory` (Factory Method pattern), and `BookingObserver` / `EmailNotifier` / `SMSNotifier` / `AuditLogger` (Observer pattern). All validation, fee calculation, and business rules live here. |
| `src/db.py` | The persistence layer. Defines the SQLite schema (`users`, `cars`, `bookings` tables) and a single `get_connection()` helper that every domain class uses to talk to the database. |
| `src/car_rental.db` | The SQLite database file. Created automatically on first run; not included in the source distribution (each installation generates its own). Delete this file to reset the system to a blank state. |
| `doc/Car_Rental_System_Report.pdf` / `.docx` | Design and Architecture / Innovative Solution / Software Evolution report (UML diagrams, design pattern rationale, maintenance and versioning plan). Not required to run the program — supporting documentation only. |
| `doc/*.png` | The individual UML diagrams (ER, Use Case, Class, Sequence, Activity, and the high-level Architectural Diagram) embedded in the report, provided separately for convenience. |
| `README.md` | This file. |

## 5. License

This project is released under the **MIT License**.

```
MIT License

Copyright (c) 2026 Pei Wu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 6. Known Bugs and Limitations

- **No database migrations.** The schema is created with
  `CREATE TABLE IF NOT EXISTS`, which only applies to a brand-new database file.
  If you pull a newer version of this project with schema changes but already
  have an existing `src/car_rental.db`, the old file will silently keep the old
  schema. **Workaround:** delete `src/car_rental.db` and restart the program to
  regenerate it from the current schema.
- **Deleting a car with existing bookings is blocked, by design.** SQLite's
  foreign-key constraint prevents deleting a car that any booking (past or
  present) references, to protect booking history from being corrupted. Use
  `Update car` to set `available_now` to `False` instead of deleting a car
  that has ever been booked.
- **Notifications are simulated, not real.** `EmailNotifier` and `SMSNotifier`
  print to the console rather than sending an actual email or SMS. Wiring
  these up to a real provider (e.g. an SMTP server or Twilio) is discussed as
  a short-term item in the report's Future Roadmap (Section 6.4).
- **Timestamps use the database process's local time zone**
  (`datetime('now', 'localtime')`). If the machine's system clock/timezone is
  misconfigured, stored timestamps will be off accordingly.
- **The pre-built executable is unsigned.** It is not signed with an Apple
  Developer certificate (or a Windows code-signing certificate), so the
  operating system will show an "unidentified developer" warning on first
  launch. This is expected — see Option B in Section 3 for how to proceed.
- **Single-user, single-process design.** The system does not handle
  concurrent writes from multiple processes; it is intended to be run as a
  single interactive CLI session at a time.
- **No password recovery.** If a user forgets their password, there is
  currently no "reset password" flow — a new account would need to be
  registered.

If you find an issue not listed here, please note it for the project's issue
tracker (see the report's Maintenance Strategy, Section 6.1).

## 7. Credits

**Developer:** Pei Wu (Student ID: 270931971)
**Course:** MSE800 Professional Software Engineering — Master of Software Engineering, Yoobee College of Creative Innovation
**Assignment:** Assignment 1 — Object-Oriented Programming Assignment
