class UserNotFound(Exception):
    def __str__(self) -> str:
        return "User Not Found."