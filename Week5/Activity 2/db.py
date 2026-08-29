import sqlite3

DATABASE_NAME = "/Users/wupei/Documents/GitHub/YoobeeMSE800/Week5/Activity 2/College.db"

def create_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_lucturer_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lecturer(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            time TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)

def create_course_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS course(
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            lecturer_id INTEGER NOT NULL,
            course_name TEXT NOT NULL,
            time TEXT NOT NULL,
            room TEXT NOT NULL,
            student_num INTEGER NOT NULL UNIQUE,
            FOREIGN KEY (lecturer_id) REFERENCES Lucturer(id),
        )
    """)

def creat_student_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            time TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)
