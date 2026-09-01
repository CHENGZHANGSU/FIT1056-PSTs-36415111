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
        return super().get_id()

    def get_teacher_name(self) -> str:
        return super().get_name()

    def get_teacher_speciality(self) -> str:
        return self.speciality

    

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
    def get_course_id(self):
        return self.id

    def get_course_name(self):
        return self.name

    def get_course_instrument(self):
        return self.instrument

    def get_course_teacher_id(self):
        return self.teacher_id

    def get_enrolled_student_ids(self):
        return self.enrolled_student_ids

    def get_lessons(self):
        return self.lessons

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
