# Car Rental System — Release Build

A command-line Car Rental System, built for MSE800 Professional Software
Engineering (Assignment 1). This is the **pre-built executable** — no Python
installation or setup is required to run it.

For the full design rationale, UML diagrams, and source code, see the
separately submitted Source Code Folder and `Car_Rental_System_Report.pdf`.

---

## 1. Running the Program

1. Unzip this release build if you haven't already.
2. Double-click `CarRentalSystem` (or open a terminal in this folder and run
   `./CarRentalSystem`).
3. **On macOS**, the first time you run it you will likely see a warning that
   the app "cannot be opened because the developer cannot be verified" — this
   is expected for an unsigned build and does not mean the file is corrupted.
   To proceed: right-click (or Control-click) `CarRentalSystem`, choose
   **Open**, then confirm **Open** again in the dialog that appears. You only
   need to do this once — after that it will launch normally.
4. A `car_rental.db` file will be created automatically in the same folder as
   the executable the first time you run it, and will be reused (so your data
   persists) on every run after that.

You will see a menu:

```
=== Car Rental System (OOP) ===

1) Register
2) Log in
3) Exit
```

## 2. First-time Setup — Create an Admin Account

The database starts empty, so the first thing to do is register an Admin
account so you can add cars to the fleet:

1. Choose `1) Register`, pick a username/password, and enter `admin` as the role.
2. Choose `2) Log in` with that account.
3. From the Admin menu, choose `2) Add car` and fill in the car's details.

Register again with role `customer` (a separate account) to browse cars,
book one, and track your bookings from the Customer menu. Log back in as the
Admin account and choose `5) Review pending bookings` to approve or reject
customer bookings.

## 3. Known Limitations

- **Unsigned build.** Not signed with an Apple Developer certificate, hence
  the Gatekeeper warning described above — this is expected, not a bug.
- **Notifications are simulated.** Booking approval/rejection notifications
  print to the console rather than sending a real email or SMS.
- **No password recovery.** If you forget a password, register a new account.
- **Single-user, single-process.** Not designed for concurrent access from
  multiple instances running at once.
- **Timestamps use this computer's local time zone.**

## 4. License

Released under the MIT License. See the Source Code Folder submission for
the full license text.

## 5. Credits

**Developer:** Pei Wu (Student ID: 270931971)
**Course:** MSE800 Professional Software Engineering — Master of Software Engineering, Yoobee College of Creative Innovation
**Assignment:** Assignment 1 — Object-Oriented Programming Assignment
