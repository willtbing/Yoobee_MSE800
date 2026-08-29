import db
from Person import Person


class Student(Person):
    role = "student"

    def enroll_course(self, course_id):
        """Request to join a course. Stays PENDING until an Admin approves it
        (Admin.approve_enrollment)."""
        enrollment_id = db.insert_enrollment(self.id, course_id)
        course = db.get_course_by_id(course_id)
        course_name = course[2] if course else "unknown course"
        print(f"{self.name} requested to enroll in '{course_name}' (pending approval).")
        return enrollment_id

    def my_enrollments(self):
        return db.get_enrollments_by_student(self.id)
