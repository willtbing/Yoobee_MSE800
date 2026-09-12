class UniversityConfig:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.universityname = ""
            cls.academicyear = 1900
            cls.semester = 2
        return cls._instance
u1 = UniversityConfig()
u2 = UniversityConfig()
u3 = UniversityConfig()
u1.universityname = "SouthEast University"
u2.academicyear = 1902
u2.semester = 4
print(u3.universityname)
print(u3.academicyear)
print(u3.semester)
