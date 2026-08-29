import db
from Admin import Admin
from Lecturer import Lecturer
from Student import Student
from Couse import Course

ROLE_CLASSES = {"1": Admin, "2": Lecturer, "3": Student}


def sign_up_flow(person_cls):
    print(f"\n-- {person_cls.__name__} sign up --")
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    phone = input("Phone: ").strip()
    password = input("Password: ").strip()
    try:
        return person_cls.sign_up(name, email, phone, password)
    except ValueError as exc:
        print(exc)
        return None


def login_flow(person_cls):
    print(f"\n-- {person_cls.__name__} login --")
    email = input("Email: ").strip()

    remembers = input("Do you remember your password? (y/n): ").strip().lower()
    if remembers == "n":
        new_password = input("Enter a new password: ").strip()
        row = db.get_person_by_email(email, role=person_cls.role)
        if row is None:
            print("No account with that email.")
            return None
        person = person_cls(row[0], row[2], row[3], row[4])
        person.forget_password(new_password)

    password = input("Password: ").strip()
    return person_cls.login(email, password)


def admin_menu(admin):
    while True:
        print(f"\n-- Admin menu ({admin.name}) --")
        print("1) Add a course")
        print("2) Update a course")
        print("3) Delete a course")
        print("4) Approve an enrollment")
        print("5) Logout")
        print("6) View a course's enrolled students")
        choice = input("Choose an action: ").strip()

        if choice == "1":
            admin.list_lecturers()
            lecturer_id = input("Lecturer id to assign: ").strip()
            course_name = input("Course name: ").strip()
            time = input("Time (e.g. Mon 10:00-12:00): ").strip()
            room = input("Room: ").strip()
            capacity = int(input("Capacity: ").strip())
            try:
                Course.add_course(int(lecturer_id), course_name, time, room, capacity)
            except ValueError as exc:
                print(exc)

        elif choice == "2":
            course_id = int(input("Course id to update: ").strip())
            course = Course.get_by_id(course_id)
            if not course:
                print("No such course.")
                continue
            room = input(f"New room (blank to keep '{course.room}'): ").strip()
            if room:
                course.update_course(room=room)

        elif choice == "3":
            course_id = int(input("Course id to delete: ").strip())
            course = Course.get_by_id(course_id)
            if course:
                course.delete_course()
            else:
                print("No such course.")

        elif choice == "4":
            admin.list_pending_enrollments()
            enrollment_id = input("Enrollment id to approve (blank to cancel): ").strip()
            if enrollment_id:
                admin.approve_enrollment(int(enrollment_id), approve=True)

        elif choice == "5":
            break

        elif choice == "6":
            course_id = input("Course id: ").strip()
            course = Course.get_by_id(int(course_id)) if course_id else None
            if not course:
                print("No such course.")
                continue
            students = course.approved_students()
            if not students:
                print("No approved students yet.")
            for student_id, name, email in students:
                print(f"  {name} ({email})")

        else:
            print("Invalid choice.")


def lecturer_menu(lecturer):
    while True:
        print(f"\n-- Lecturer menu ({lecturer.name}) --")
        print("1) View assigned courses")
        print("2) Logout")
        choice = input("Choose an action: ").strip()

        if choice == "1":
            lecturer.view_assigned_courses()
        elif choice == "2":
            break
        else:
            print("Invalid choice.")


def student_menu(student):
    while True:
        print(f"\n-- Student menu ({student.name}) --")
        print("1) Enroll into a course")
        print("2) Logout")
        choice = input("Choose an action: ").strip()

        if choice == "1":
            for course in Course.get_all():
                print(f"  {course}")
            course_id = input("Course id to enroll in: ").strip()
            if course_id:
                student.enroll_course(int(course_id))
        elif choice == "2":
            break
        else:
            print("Invalid choice.")


MENUS = {Admin: admin_menu, Lecturer: lecturer_menu, Student: student_menu}


def main():
    db.init_db()

    while True:
        print("\n=== College Management System ===")
        print("1) Admin")
        print("2) Lecturer")
        print("3) Student")
        print("4) Exit")
        role_choice = input("Choose a role: ").strip()

        if role_choice == "4":
            print("Goodbye.")
            break
        if role_choice not in ROLE_CLASSES:
            print("Invalid choice.")
            continue

        person_cls = ROLE_CLASSES[role_choice]
        print("1) Sign up  2) Login")
        action = input("Choose an action: ").strip()

        person = sign_up_flow(person_cls) if action == "1" else login_flow(person_cls)
        if person is None:
            continue

        MENUS[person_cls](person)


if __name__ == "__main__":
    main()
