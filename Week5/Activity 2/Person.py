from abc import ABC

import db


class Person(ABC):
    """Abstract superclass. role must be set by every subclass
    ('admin' / 'lecturer' / 'student') so it lines up with the
    'role' column in the person table."""

    role = None  # overridden by Student / Lecturer / Admin

    def __init__(self, person_id, name, email, phone):
        self.id = person_id
        self.name = name
        self.email = email
        self.phone = phone

    # ---------------- class-level "use cases" ----------------
    @classmethod
    def sign_up(cls, name, email, phone, password):
        """Create a new account for this role and return the new instance."""
        if db.get_person_by_email(email) is not None:
            raise ValueError(f"An account with email '{email}' already exists.")
        new_id = db.insert_person(cls.role, name, email, phone, password)
        print(f"[{cls.__name__}] {name} signed up successfully.")
        return cls(new_id, name, email, phone)

    @classmethod
    def login(cls, email, password):
        """Look up the account by email + password and return an instance,
        or None if the credentials don't match."""
        row = db.get_person_by_email(email, role=cls.role)
        if row is None:
            print(f"[{cls.__name__}] No account found for {email}.")
            return None
        person_id, role, name, db_email, phone, db_password = row
        if db_password != password:
            print(f"[{cls.__name__}] {name} login failed (wrong password).")
            return None
        print(f"[{cls.__name__}] {name} login succeeded.")
        return cls(person_id, name, db_email, phone)

    def forget_password(self, new_password):
        """'Remember password? N' branch in the activity diagram."""
        db.update_person_password(self.id, new_password)
        print(f"[{self.__class__.__name__}] {self.name} reset their password.")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"
