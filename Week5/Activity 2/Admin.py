import db
from Person import Person


class Admin(Person):
    role = "admin"

    def approve_enrollment(self, enrollment_id, approve=True):
        if db.get_enrollment_by_id(enrollment_id) is None:
            print(f"No enrollment with id {enrollment_id} -- nothing was changed.")
            return False
        status = "approved" if approve else "rejected"
        db.set_enrollment_status(enrollment_id, status)
        print(f"Admin {self.name} {status} enrollment #{enrollment_id}.")
        return True

    def list_lecturers(self):
        rows = db.list_people("lecturer")
        if not rows:
            print("No lecturers registered yet.")
        for person_id, role, name, email, phone, _password in rows:
            print(f"  id {person_id}: {name} ({email})")
        return rows

    def list_pending_enrollments(self):
        rows = db.get_pending_enrollments()
        if not rows:
            print("No pending enrollments.")
        for enrollment_id, student_name, course_name, status in rows:
            print(f"  #{enrollment_id} {student_name} -> {course_name} [{status}]")
        return rows

    # Course CRUD lives on Course itself (see Couse.py) since that's how the
    # class diagram drew addCourse()/updateCourse()/deleteCourse() -- Admin
    # is simply the role expected to call them, e.g.:
    #   Course.add_course(lecturer_id=..., ...)
