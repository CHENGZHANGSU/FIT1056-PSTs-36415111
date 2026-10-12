class UserNotFound(Exception):
    def __str__(self) -> str:
        return "User Not Found."

class CourseNotFound(Exception):
    def __str__(self) -> str:
        return "Course Not Found."

