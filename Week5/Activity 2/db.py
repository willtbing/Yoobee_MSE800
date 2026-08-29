import os
import sqlite3

# Portable path: put the db file next to this script instead of a hardcoded
# absolute path (the original had a machine-specific /Users/... path).
DATABASE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "college.db")


def create_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create every table used by the app. Safe to call multiple times."""
    conn = create_connection()
    cursor = conn.cursor()

    # One table for Person + its subclasses (Student/Lecturer/Admin), with a
    # 'role' discriminator column -- this matches the single Person
    # superclass in the class diagram instead of three separate,
    # partially-duplicated tables.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS person (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL CHECK(role IN ('admin', 'lecturer', 'student')),
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS course (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            lecturer_id INTEGER NOT NULL,
            course_name TEXT NOT NULL,
            time TEXT NOT NULL,
            room TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            FOREIGN KEY (lecturer_id) REFERENCES person(id)
        )
    """)

    # The 'enrolls in' / 'approves enrollment for' association from the
    # class diagram: a Student requests a Course, an Admin approves it.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enrollment (
            enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected')),
            FOREIGN KEY (student_id) REFERENCES person(id),
            FOREIGN KEY (course_id) REFERENCES course(course_id)
        )
    """)

    conn.commit()
    conn.close()


# ------------------------------------------------------------------
# Person (shared by Student / Lecturer / Admin)
# ------------------------------------------------------------------
def insert_person(role, name, email, phone, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO person (role, name, email, phone, password) VALUES (?, ?, ?, ?, ?)",
        (role, name, email, phone, password),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_person_by_email(email, role=None):
    conn = create_connection()
    cursor = conn.cursor()
    if role:
        cursor.execute("SELECT * FROM person WHERE email = ? AND role = ?", (email, role))
    else:
        cursor.execute("SELECT * FROM person WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    return row


def get_person_by_id(person_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM person WHERE id = ?", (person_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def update_person_password(person_id, new_password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE person SET password = ? WHERE id = ?", (new_password, person_id))
    conn.commit()
    conn.close()


def list_people(role):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM person WHERE role = ?", (role,))
    rows = cursor.fetchall()
    conn.close()
    return rows


# ------------------------------------------------------------------
# Course
# ------------------------------------------------------------------
def insert_course(lecturer_id, course_name, time, room, capacity):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO course (lecturer_id, course_name, time, room, capacity) VALUES (?, ?, ?, ?, ?)",
        (lecturer_id, course_name, time, room, capacity),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def update_course(course_id, **fields):
    if not fields:
        return
    conn = create_connection()
    cursor = conn.cursor()
    assignments = ", ".join(f"{key} = ?" for key in fields)
    values = list(fields.values()) + [course_id]
    cursor.execute(f"UPDATE course SET {assignments} WHERE course_id = ?", values)
    conn.commit()
    conn.close()


def delete_course(course_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM enrollment WHERE course_id = ?", (course_id,))
    cursor.execute("DELETE FROM course WHERE course_id = ?", (course_id,))
    conn.commit()
    conn.close()


def get_course_by_id(course_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM course WHERE course_id = ?", (course_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def get_all_courses():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM course")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_courses_by_lecturer(lecturer_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM course WHERE lecturer_id = ?", (lecturer_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


# ------------------------------------------------------------------
# Enrollment
# ------------------------------------------------------------------
def insert_enrollment(student_id, course_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO enrollment (student_id, course_id, status) VALUES (?, ?, 'pending')",
        (student_id, course_id),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_enrollment_by_id(enrollment_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM enrollment WHERE enrollment_id = ?", (enrollment_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def set_enrollment_status(enrollment_id, status):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE enrollment SET status = ? WHERE enrollment_id = ?", (status, enrollment_id))
    updated = cursor.rowcount  # 0 means the id didn't exist -- caller must check this
    conn.commit()
    conn.close()
    return updated


def get_approved_students_by_course(course_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT person.id, person.name, person.email
        FROM enrollment
        JOIN person ON person.id = enrollment.student_id
        WHERE enrollment.course_id = ? AND enrollment.status = 'approved'
    """, (course_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_pending_enrollments():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT enrollment.enrollment_id, person.name, course.course_name, enrollment.status
        FROM enrollment
        JOIN person ON person.id = enrollment.student_id
        JOIN course ON course.course_id = enrollment.course_id
        WHERE enrollment.status = 'pending'
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_enrollments_by_student(student_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM enrollment WHERE student_id = ?", (student_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows
