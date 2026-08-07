import unittest
from MSMS import *

# --- Unit Testing for Stage 1 ---
class TestAdd(unittest.TestCase):

    def test_add_teacher(self):
        """
        Testcase for teacher registration.
        """
        add_teacher("Dr.Keys", "Piano")
        add_teacher("Ms.Fret", "Guitar")
        assert len(teacher_db) == 2, "The size of the database did not change."
        assert str(teacher_db[0]) == "1, Dr.Keys, Piano", "The teacher element did not add correctly."
        assert str(teacher_db[1]) == "2, Ms.Fret, Guitar", "The teacher element did not add correctly."

    def test_add_student(self):
        """
        Testcase for front desk student registration and enrollment.
        """
        front_desk_register("Adam", "Piano")
        front_desk_register("Leo", "Violin")
        assert len(student_db) == 2, "The size of the database did not change."
        assert str(student_db[0]) == "1, Adam, ['Piano']", "The student element did not add correctly."
        assert str(student_db[1]) == "2, Leo, ['Violin']", "The student element did not add correctly."

    def test_remove_item(self):
        """
        Testcase for students and teachers removal.
        """
        assert len(teacher_db) == 2 and len(student_db) == 2, "Elements did not add correctly."

        # Simple removal
        remove_data("Dr.Keys")
        remove_data("Adam")
        assert len(teacher_db) == 1 and len(student_db) == 1, "Simple remove: Element did not remove correctly."

        # Repeat names removal
        front_desk_register("Adam", "Piano")
        front_desk_register("Adam", "Guitar")
        remove_data("Adam")                         # remove the Guitar one
        assert len(student_db) == 2, "Repeat remove: Element did not remove correctly."
        assert str(student_db[1]) == "3, Adam, ['Piano']", "Repeat remove: The student element did not remove correctly." 

 

# --- Test Start ---
if __name__ == "__main__":
    unittest.main()