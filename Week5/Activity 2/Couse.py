import db


class Course:
    def __init__(self, course_id, lecturer_id, course_name, time, room, capacity):
        self.course_id = course_id
        self.lecturer_id = lecturer_id
        self.course_name = course_name
        self.time = time
        self.room = room
        self.capacity = capacity

    # ---------------- "use cases" from the diagrams ----------------
    @classmethod
    def add_course(cls, lecturer_id, course_name, time, room, capacity):
        """Admin creates a course and assigns the teaching lecturer here --
        this is the only place a Lecturer gets attached to a Course."""
        lecturer_row = db.get_person_by_id(lecturer_id)
        if lecturer_row is None or lecturer_row[1] != "lecturer":
            raise ValueError(f"No lecturer with id {lecturer_id}. Use 'list lecturers' to see valid ids.")
        course_id = db.insert_course(lecturer_id, course_name, time, room, capacity)
        print(f"Course '{course_name}' added (lecturer: {lecturer_row[2]}, id {lecturer_id}).")
        return cls(course_id, lecturer_id, course_name, time, room, capacity)

    def update_course(self, **changes):
        db.update_course(self.course_id, **changes)
        for key, value in changes.items():
            setattr(self, key, value)
        print(f"Course '{self.course_name}' updated: {changes}")

    def delete_course(self):
        db.delete_course(self.course_id)
        print(f"Course '{self.course_name}' deleted.")

    # ---------------- lookups ----------------
    @classmethod
    def get_by_id(cls, course_id):
        row = db.get_course_by_id(course_id)
        return cls(*row) if row else None

    @classmethod
    def get_all(cls):
        return [cls(*row) for row in db.get_all_courses()]

    def approved_students(self):
        """Students actually enrolled (approved) in this course."""
        return db.get_approved_students_by_course(self.course_id)

    def __repr__(self):
        return f"Course(#{self.course_id}, {self.course_name!r}, lecturer_id={self.lecturer_id})"
