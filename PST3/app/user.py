class User:
    """A base class for all users in the system."""
    def __init__(self, user_id, name):
        self.id = user_id
        self.name = name

    """Accessor"""
    def get_id(self) -> int:
        return self.id

    def get_name(self) -> str:
        return self.name

    """Mutator"""
    def set_id(self, new_id: int):
        self.id = new_id

    def set_name(self, new_name: str):
        self.name = new_name
