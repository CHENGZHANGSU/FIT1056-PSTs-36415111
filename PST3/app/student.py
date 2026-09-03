from app.user import User

class StudentUser(User):
    """Represents a student, inheriting from the base User class."""
    def __init__(self, user_id, name):
        # TODO: Call the parent class's __init__ method using super().
        super().__init__(user_id, name)
        # TODO: Initialize an empty list called 'enrolled_course_ids' to store the IDs of courses.
        self.enrolled_course_ids = []

    """Accessor"""
    def get_id(self) -> int:
        id = super().get_id()
        return id

    def get_enrolled_course_ids(self):
        return self.enrolled_course_ids

    """Mutator"""
    def enroll_course_ids(self, new_course_id: int):
        try:
            self.enrolled_course_ids.append(new_course_id)
        except:
            print("Error occur, please try again.\n")

    def set_enrolled_course_ids(self, new_course_ids: list):
        self.enrolled_course_ids = new_course_ids

    def help_remove_course_id(self, removed_id: int):
        try:
            self.enrolled_course_ids.remove(id)
        except:
            print(f"Course {id} is not in your current studying units.\n")

    def remove_enrolled_course_id(self, remove_id: int|list[int]):
        if type(remove_id) == int:
            self.help_remove_course_id(remove_id)
        elif type(remove_id) == list[int]:
            for id in remove_id:
                self.help_remove_course_id(id)
        else:
            print("Invalid data type.\n")


    """Additional Helper method"""
    def update(self, **field):
        if field['name'].replace(" ", "") != "":
            super().set_name(field['name'])
        if type(field['course_id']) == list:
            if len(field['course_id']) != 0:
                self.enrolled_course_ids = field['course_id']
        else:
            print(f"{type(field['course_id'])}. ")
            print("Invalid data type.\n")

        