import unittest
import pandas as pd
from pst2_main import *

# --- Unit Testing for Stage 2 ---
class TestStage2(unittest.TestCase):

    # def test_load_data(self):
    #     """
    #     Test the file initialization.
    #     """
    #     load_data(path = "PST2/test.json")
    #     save_data(path = "PST2/test.json")
    #     # load_data(path = "test.json")

    #     assert len(get_app_data()) == 5, "The file is generated unsuccessfully or with wrong length."

    # def test_student_register(self):
    #     """
    #     Test the student registration workflow.
    #     """
    #     load_data(path = "PST2/test.json")
    #     self.app_data = get_app_data()
    #     front_desk_register("Adam", "piano")                  # This command should run one time.
    #     save_data(path = "PST2/test.json")

    #     assert len(self.app_data['students']) == 1, "The student is registered unsuccessfully."
    #     assert self.app_data['students'][0]['id'] == 1, "Student id is registered unsuccessfully."
    #     assert self.app_data['students'][0]['name'] == "Adam", "Student name is registered unsuccessfully."
    #     assert self.app_data['students'][0]['enrolled_in'][0] == "piano", "Student enrollment is registered unsuccessfully."

    # def test_teacher_register(self):
    #     """
    #     Test the teacher registration workflow.
    #     """
    #     load_data(path = "PST2/test.json")
    #     self.app_data = get_app_data()
    #     add_teacher("Charlotte", "English")                      # This command should run one time.
    #     save_data(path = "PST2/test.json")

    #     assert len(self.app_data['teachers']) == 1, "The teacher is registered unsuccessfully."
    #     assert self.app_data['teachers'][0]['id'] == 1, "Teacher id is registered unsuccessfully."
    #     assert self.app_data['teachers'][0]['name'] == "Charlotte", "Teacher name is registered unsuccessfully."
    #     assert self.app_data['teachers'][0]['speciality'] == "English", "Teacher speciality is registered unsuccessfully."

    # def test_find(self):
    #     """
    #     Test the searching function for students and teachers.
    #     """
    #     load_data(path = "PST2/test.json")
    #     self.app_data = get_app_data()

    #     assert find_students("Adam") == True, "Student cannot be found successfully."
    #     assert find_teachers("Charlotte") == True, "Teacher cannot be found successfully."


    # def test_update(self):
    #     """
    #     Test the update of teacher and student information.
    #     """
    #     load_data(path = "PST2/test.json")
    #     update_student(1, name = "Leo", enrolled_in = ['violin'])    
    #     update_teacher(1, name = "Wendy", speciality = "Math")
    #     save_data(path = "PST2/test.json")

    #     self.app_data = get_app_data()

    #     assert self.app_data['students'][0]['name'] == "Leo", "Student name is updated unsuccessfully."
    #     assert self.app_data['students'][0]['enrolled_in'][0] == "violin", "Student enrollment is updated unsuccessfully."

    #     assert self.app_data['teachers'][0]['name'] == "Wendy", "Teacher name is updated unsuccessfully."
    #     assert self.app_data['teachers'][0]['speciality'] == "Math", "Teacher speciality is updated unsuccessfully."
        
    def test_remove(self):
        """
        Test the removal of teacher and student information.
        """
        load_data(path = "PST2/test.json")
        # remove_student(1)                                   # This command should only run once
        # remove_teacher(1)                                   # This command should only run once
        save_data(path = "PST2/test.json")

        self.app_data = get_app_data()

        self.assertEqual(len(self.app_data['students']), 0, "Student not removed successfully.")
        self.assertEqual(len(self.app_data['teachers']), 0, "Teacher not removed successfully.")


# --- Test Start ---
if __name__ == "__main__":
    unittest.main()