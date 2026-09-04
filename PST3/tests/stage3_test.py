import unittest
import json

import sys
sys.path.append('./')

from app.schedule import ScheduleManager
from app.student import StudentUser
from app.teacher import Course, TeacherUser


class TestStage3(unittest.TestCase):
    """Tests for the Stage 3 object-oriented schedule manager."""

    def setUp(self):
        filename = "tests/test_copy.json"
        data = {}
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        with open("tests/test.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4) 

        self.data_path = "tests/test.json"
        self.manager = ScheduleManager(str(self.data_path))
        print(self.manager.attendance_log)

    def test_loads_json_into_model_objects(self):
        self.assertEqual(len(self.manager.students), 2)
        self.assertEqual(len(self.manager.teachers), 2)
        self.assertEqual(len(self.manager.courses), 3)
        self.assertEqual(len(self.manager.attendance_log), 2)
        self.assertIsInstance(self.manager.students[0], StudentUser)
        self.assertIsInstance(self.manager.teachers[0], TeacherUser)
        self.assertIsInstance(self.manager.courses[0], Course)

    def test_finds_users_and_courses_by_id(self):
        student = self.manager.find_user_by_id(1, "s")
        teacher = self.manager.find_user_by_id(2, "t")
        course = self.manager.find_course_by_id(102)

        self.assertIsNotNone(student)
        self.assertIsNotNone(teacher)
        self.assertIsNotNone(course)

        assert student is not None
        assert teacher is not None
        assert course is not None

        self.assertEqual(student.get_name(), "Alice Johnson")
        self.assertEqual(teacher.get_name(), "Mr. David Fret")
        self.assertEqual(course.get_course_name(), "Acoustic Guitar Fundamentals")
        self.assertIsNone(self.manager.find_user_by_id(999, "s"))
        self.assertIsNone(self.manager.find_course_by_id(999))

    def test_sorting_users_in_both_directions(self):
        ascending = self.manager._obey_order("s", "ascending")
        descending = self.manager._obey_order("s", "descending")

        self.assertEqual([student.get_id() for student in ascending], [1, 2])
        self.assertEqual([student.get_id() for student in descending], [2, 1])

    def test_enrolment_and_synchronization(self):
        student = self.manager.find_user_by_id(2, "s")
        course = self.manager.find_course_by_id(103)
        
        assert student is not None
        assert course is not None

        self.manager.front_desk_enrol(student.get_id(), course.get_course_id(), "s")
        self.assertIn(103, student.get_enrolled_course_ids())
        self.assertIn(2, course.get_enrolled_student_ids())

        student.enrolled_course_ids.append(999)
        self.manager.sync_courses_students()
        self.assertNotIn(999, student.get_enrolled_course_ids())

    def test_check_in_records_valid_attendance(self):
        original_count = len(self.manager.attendance_log)
        self.assertTrue(self.manager.check_in(1, 101))
        self.assertEqual(len(self.manager.attendance_log), original_count + 1)

        record = self.manager.attendance_log[-1]
        self.assertEqual(record["student_id"], 1)
        self.assertEqual(record["course_id"], 101)
        self.assertIn("timestamp", record)

        self.assertFalse(self.manager.check_in(999, 101))
        self.assertEqual(len(self.manager.attendance_log), original_count + 1)

    def test_adds_and_removes_users_with_course_updates(self):
        self.manager.id["next_teacher_id"] = 3
        self.manager.add_teacher("New Teacher", "Violin")

        new_teacher = self.manager.find_user_by_id(3, "t")
        course = self.manager.find_course_by_id(101)
        guitar_course = self.manager.find_course_by_id(102)

        assert new_teacher is not None
        assert course is not None
        assert guitar_course is not None
        self.assertEqual(new_teacher.get_teacher_speciality(), "Violin")

        self.manager.remove_user(1, "t")
        self.assertIsNone(self.manager.find_user_by_id(1, "t"))
        self.assertEqual(course.get_course_teacher_id(), -1)

        self.manager.remove_user(2, "s")
        self.assertIsNone(self.manager.find_user_by_id(2, "s"))
        self.assertNotIn(2, guitar_course.get_enrolled_student_ids())

    def test_updates_teacher_information(self):
        self.manager.update_user("t", 1, name="Updated Teacher", speciality="Cello")
        teacher = self.manager.find_user_by_id(1, "t")

        assert teacher is not None
        self.assertEqual(teacher.get_name(), "Updated Teacher")
        self.assertEqual(teacher.get_teacher_speciality(), "Cello")


if __name__ == "__main__":
    unittest.main()
