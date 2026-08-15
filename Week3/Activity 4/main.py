'''
Develop a database project based on the ER diagram created in W3-A3. Review and update the ER diagram if necessary before implementing the database and you can use the sample code in your Blackboard.
Populate the database with the following sample data:
3 courses
2 lecturers
5 students
Appropriate enrolment records for the students
Any additional records required for the other entities/tables in your ER diagram
Once the database has been developed and populated, use SQL queries to answer the following questions:
How many students are registered in each course?
List the names and student IDs of students who have enrolled in more than one course.
'''

import sqlite3
from database import (create_connection, create_table_Enrollment, create_table_Lecture, 
                      create_table_Lecturer, create_table_Student, 
                      create_table_Subject, add_enrollment, add_Lecture, 
                      add_Lecturer, add_student, add_Subject)

def main():
    #create table
    create_table_Lecturer()
    create_table_Subject()
    create_table_Lecture()
    create_table_Student()
    create_table_Enrollment()
    #Insert data
    add_Subject(24, "Professional Software Engineering")
    add_Subject(16, "Research Methods")
    add_Subject(16, "Quantum Computing")
    add_Lecturer("Mohammad", "Norouzifard", "Mohammad.Norouzifard@yoobeecolleges.com")
    add_Lecturer("Reem", "Abbas", "Reem.Abbas@yoobeecolleges.com")
    add_student("Pei", "Wu", "1981-12-23", "270931971@yoobeestudent.ac.nz")
    add_student("Passang", "Lhamo", "1996-11-11", "270931974@yoobeestudent.ac.nz")
    add_student("Shuohui", "Liu", "1985-4-1", "270921971@yoobeestudent.ac.nz")
    add_student("Vishal", "Rana", "2002-7-12", "270331971@yoobeestudent.ac.nz")
    add_student("Immanuel", "Santhosh", "1995-5-2", "270931471@yoobeestudent.ac.nz")
    add_Lecture("09:00", "2026-08-20", "Professional Software Engineering", 1, 1)
    add_Lecture("13:00", "2026-08-21", "Research Methods", 2, 2)
    add_Lecture("10:00", "2026-08-22", "Quantum Computing", 1, 3)
    add_enrollment("2026-08-18", 1, 1)
    add_enrollment("2026-08-18", 2, 1)
    add_enrollment("2026-08-18", 3, 1)
    add_enrollment("2026-08-18", 1, 2)
    add_enrollment("2026-08-18", 2, 3)
    add_enrollment("2026-08-18", 2, 4)
    add_enrollment("2026-08-18", 1, 5)
    add_enrollment("2026-08-18", 3, 5)
    #How many students are registered in each course?
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT
                        subject.Subject_code,
                        subject.Subject_desc,
                        COUNT(DISTINCT enrollment.student_id) AS student_count
                    FROM subject
                    LEFT JOIN lecture
                        ON subject.Subject_code = lecture.Subject_code
                    LEFT JOIN enrollment
                        ON lecture.CC = enrollment.CC
                    GROUP BY
                        subject.Subject_code,
                        subject.Subject_desc;
                    """)
    results = cursor.fetchall()
    print("Number of students registered in each course:")
    for row in results:
        print(f"Subject Code: {row[0]}, Subject Description: {row[1]}, Student Count: {row[2]}")
    #List the names and student IDs of students who have enrolled in more than one course.
    cursor.execute("""
                    SELECT
                        student.NID,
                        student.F_name,
                        student.L_name,
                        COUNT(DISTINCT enrollment.CC) AS course_count
                    FROM student
                    LEFT JOIN enrollment ON student.NID = enrollment.student_id
                    GROUP BY
                        student.NID,
                        student.F_name,
                        student.L_name
                    HAVING COUNT(DISTINCT enrollment.CC) > 1;
                    """)
    results = cursor.fetchall()
    print("Students enrolled in more than one course:")
    for row in results:
        print(f"Student ID: {row[0]}, First Name: {row[1]}, Last Name: {row[2]}, Course Count: {row[3]}") 

if __name__ == "__main__":
    main()