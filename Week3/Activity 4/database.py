import sqlite3

#create connection
def create_connection():
    conn = sqlite3.connect("/Users/wupei/Documents/GitHub/YoobeeMSE800/Week3/Activity 4/Activity.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

#create table
def create_table_Lecturer():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lecturer(
            Lecturer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            L_firstname TEXT NOT NULL,
            L_lastname TEXT NOT NULL,
            L_email TEXT UNIQUE,
            L_address TEXT
        )
    """)
    conn.commit()
    conn.close()

def create_table_Subject():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subject(
            Subject_code INTEGER PRIMARY KEY AUTOINCREMENT,
            Subject_unit INTEGER NOT NULL,
            Subject_desc TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def create_table_Lecture():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lecture(
           CC INTEGER PRIMARY KEY AUTOINCREMENT,
           Time TEXT NOT NULL,
           Date TEXT NOT NULL,
           Lecture_name TEXT NOT NULL,
           Lecturer_id INTEGER NOT NULL,
           Subject_code INTEGER NOT NULL,
           FOREIGN KEY (Lecturer_id) REFERENCES lecturer(Lecturer_id),
           FOREIGN KEY (Subject_code) REFERENCES subject(Subject_code)
        )
    """)
    conn.commit()
    conn.close()

def create_table_Student():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student(
           NID INTEGER PRIMARY KEY AUTOINCREMENT,
           F_name TEXT NOT NULL,
           L_name TEXT NOT NULL,
           B_date TEXT NOT NULL,
           Email TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()

def create_table_Enrollment():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enrollment(
           Enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
           Date_of_enrollment TEXT NOT NULL,
           CC INTEGER NOT NULL,
           student_id INTEGER NOT NULL,
           FOREIGN KEY (student_id) REFERENCES student(NID),
           FOREIGN KEY (CC) REFERENCES lecture(CC)
        )
    """)
    conn.commit()
    conn.close()

#add data

def add_Lecturer(L_firstname, L_lastname, L_email=None, L_address=None):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
                        INSERT INTO lecturer (L_firstname, L_lastname, L_email, L_address) 
                        VALUES (?, ?, ?, ?)
                        """, (L_firstname, L_lastname, L_email, L_address))
        conn.commit()
        print(" Lecturer added successfully.")
    except sqlite3.IntegrityError as e:
        print("Failed to add Lecturer:", e)
    conn.close()

def add_Subject(Subject_unit, Subject_desc):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
                        INSERT INTO subject (Subject_unit, Subject_desc) 
                        VALUES (?, ?)
                        """, (Subject_unit, Subject_desc))
        conn.commit()
        print(" Subject added successfully.")
    except sqlite3.IntegrityError as e:
        print("Failed to add Subject:", e)
    conn.close()

def add_Lecture(Time, Date, Lecture_name, Lecturer_id, Subject_code):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
                        INSERT INTO lecture (Time, Date, Lecture_name, Lecturer_id, Subject_code) 
                        VALUES (?, ?, ?, ?, ?)
                        """, (Time, Date, Lecture_name, Lecturer_id, Subject_code))
        conn.commit()
        print(" Lecture added successfully.")
    except sqlite3.IntegrityError as e:
        print("Failed to add Lecture:", e)
    conn.close()

def add_student(fname, lname, bdate, email=None):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
                        INSERT INTO student (F_name, L_name, B_date, Email) 
                        VALUES (?, ?, ?, ?)
                        """, (fname, lname, bdate, email))
        conn.commit()
        print(" Student added successfully.")
    except sqlite3.IntegrityError as e:
        print("Failed to add student:", e)
    conn.close()

def add_enrollment(date, CC, student_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
                        INSERT INTO enrollment (Date_of_enrollment, CC, student_id) 
                        VALUES (?, ?, ?)
                        """, (date, CC, student_id))
        conn.commit()
        print("Student " + str(student_id) + " enrolled in " + str(CC) + " successfully.")
    except sqlite3.IntegrityError:
        print(" Check the information to ensure that all data items are not empty.")
    conn.close()
