from app.user import User

class StudentUser(User):
    """Represents a student, inheriting from the base User class."""
    def __init__(self, user_id, name):
        # TODO: Call the parent class's __init__ method using super().
        super().__init__(user_id, name)
        # TODO: Initialize an empty list called 'enrolled_course_ids' to store the IDs of courses.
        self.enrolled_course_ids = []

    """Accessor"""
    def get_enrolled_course_ids(self):
        return self.enrolled_course_ids

    """Mutator"""
    def enroll_course_ids(self, new_course_id: int):
        try:
            self.enrolled_course_ids.append(new_course_id)
        except:
            print("Error occur, please try again")

    def set_enrolled_course_ids(self, new_course_ids: list):
        self.enrolled_course_ids = new_course_ids