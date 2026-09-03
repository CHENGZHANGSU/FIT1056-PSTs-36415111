from app.user import User

class TeacherUser(User):
    """Represents a teacher."""
    # TODO: Implement the TeacherUser class, inheriting from User.
    # It should have an additional 'speciality' attribute in its __init__.
    def __init__(self, user_id, name, speciality):
        super().__init__(user_id, name)
        self.speciality = speciality

    """Accessor"""
    def get_teacher_id(self) -> int:
        id = super().get_id()
        return id

    def get_teacher_name(self) -> str:
        name = super().get_name()
        return name

    def get_teacher_speciality(self) -> str:
        speciality = self.speciality 
        return speciality

    """Additional Helper Method"""
    def update(self, **field):
        if field['name'].replace(" ", "") != "":
            super().set_name(field['name'])
        if field['speciality'].replace(" ", "") != "":
            self.speciality = field['speciality'] 

    

class Course:
    """Represents a single course offered by the school, linked to a teacher."""
    def __init__(self, course_id, name, instrument, teacher_id):
        self.id = course_id
        self.name = name
        self.instrument = instrument
        self.teacher_id = teacher_id
        # TODO: Initialize two empty lists: 'enrolled_student_ids' and 'lessons'.
        self.enrolled_student_ids = []
        self.lessons = [] # This will hold lesson dictionaries

    """Accessor"""
    def get_id(self):
        id = self.id
        return id

    def get_course_id(self):
        id = self.id
        return id

    def get_course_name(self):
        name = self.name
        return name

    def get_course_instrument(self):
        instrument = self.instrument
        return instrument

    def get_course_teacher_id(self):
        course_teacher_id = self.teacher_id
        return course_teacher_id

    def get_enrolled_student_ids(self):
        enrolled_student_ids = self.enrolled_student_ids
        return enrolled_student_ids

    def get_lessons(self):
        lessons = self.lessons
        return lessons

    """Mutator"""
    def set_list_lessons(self, lst_lesson:list):
        self.lessons = lst_lesson

    def set_teacher_id(self, new_teacher_id:int):
        self.teacher_id = new_teacher_id

    def set_enroll_student_lst(self, enrolled_lst_student:list):
        self.enrolled_student_ids = enrolled_lst_student

    def set_instrument(self, new_instrument:str):
        self.instrument = new_instrument

    def enroll_student_in_course(self, student_id:int):
        self.enrolled_student_ids.append(student_id)

    def remove_enrolled_student_id(self, student_id:int):
        self.enrolled_student_ids.remove(student_id)

    """Additional Helper Method"""
    def update(self, **field):
        pass
