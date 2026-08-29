import db
from Person import Person


class Lecturer(Person):
    role = "lecturer"

    def view_assigned_courses(self):
        """Lecturer only VIEWS the courses an Admin has assigned to them
        (the 'teaches' association) -- they can never assign themselves."""
        rows = db.get_courses_by_lecturer(self.id)
        if not rows:
            print(f"{self.name} has no assigned courses yet.")
        for course_id, lecturer_id, course_name, time, room, capacity in rows:
            print(f"  #{course_id} {course_name} | {time} | room {room} | capacity {capacity}")
        return rows
