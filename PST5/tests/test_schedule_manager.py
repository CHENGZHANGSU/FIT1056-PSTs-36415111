# tests/test_schedule_manager.py
import pytest
import os
from app.schedule import ScheduleManager
from app.student import StudentUser
from app.teacher import Course, TeacherUser
from Exceptions.NotFoundException import UserNotFound, CourseNotFound

# A pytest fixture creates a clean environment for each test function.
@pytest.fixture
def fresh_manager():
    """Creates a fresh ScheduleManager instance using a temporary test data file."""
    test_file = "tests/test_data.json"
    # ARRANGE: Ensure no old test file exists.
    if os.path.exists(test_file):
        os.remove(test_file)
    return ScheduleManager(data_path=test_file)

def test_add_teacher(fresh_manager):
    # ARRANGE: Add a teacher for the tests
    # ACT: Call the methods to add a new teacher
    fresh_manager.add_teacher("Justin", "Piano")

    # ASSERT: Check is the teacher is added as expected
    assert len(fresh_manager.teachers) == 1
    assert fresh_manager.teachers[0].name == "Justin"
    assert fresh_manager.teachers[0].speciality == "Piano"

def test_create_course(fresh_manager):
    # ARRANGE: We have a fresh manager from the fixture.
    # ACT: Call the method we want to test.
    with pytest.raises(UserNotFound):
        fresh_manager.add_course(course_name = "Beginner Piano", 
                                instrument = "Piano", 
                                teacher_id = 0)

    # ASSERT: Check if the outcome is what we expect.
    assert len(fresh_manager.courses) == 1
    assert fresh_manager.courses[0].name == "Beginner Piano"

def test_enroll_teacher_to_course(fresh_manager):
    # ARRANGE: add a dummy teacher and course
    fresh_manager.teachers.append(TeacherUser(1, "Winson", "Piano"))
    fresh_manager.add_course(course_name = "Beginner Piano", 
                            instrument = "Piano", 
                            teacher_id = 1)

    course = fresh_manager.courses[0]
    teacher_id = fresh_manager.teachers[0].id

    # ACT: Call the method for teacher-course enrollment
    fresh_manager.enroll_teacher_to_course(course, teacher_id, True)

    # ASSERT: Check the teacher is enrolled in the course
    # No data is deleted accidentally
    assert len(fresh_manager.courses) == 1
    assert len(fresh_manager.teachers) == 1
    assert fresh_manager.courses[0].teacher_id == 1

def test_add_student(fresh_manager):
    # ARRANGE: add a dummy course to the existing manager
    # with pytest.raises(UserNotFound):
    #     fresh_manager.add_course(course_name = "Beginner Piano", 
    #                             instrument = "Piano", 
    #                             teacher_id = 0)
    fresh_manager.courses.append(Course(101, "Beginner Piano", "Piano", 0))

    # ACT: call the method to add a student
    fresh_manager.front_desk_register("Adam", 101, "Piano")

    # ASSERT: Check the student enrolled successfully
    assert len(fresh_manager.students) == 1
    assert fresh_manager.students[0].name == "Adam"
    assert fresh_manager.students[0].enrolled_instruments[0] == "Piano"

def test_front_desk_enroll(fresh_manager):
    # ARRANGE: Add a dummy course and student to the existing manager
    fresh_manager.courses.append(Course(101, "Beginner Piano", "Piano", 0))
    fresh_manager.students.append(StudentUser(1, "Adam"))

    # ACT: Call the enrolling method
    student_id = fresh_manager.students[0].id
    course_id = fresh_manager.courses[0].id
    fresh_manager.front_desk_enrol(student_id, course_id, "s", "Piano")

    # ASSERT: Check the courses & instrument is enrolled
    assert fresh_manager.students[0].enrolled_course_ids[0] == 101
    assert fresh_manager.students[0].enrolled_instruments[0] == "Piano"

@pytest.mark.parametrize("type, user_id, expected_msg", [
    ("s", 1, "Adam"),
    ("t", 1, "Fekerri")
])
def test_find_user_success(fresh_manager, type, user_id, expected_msg):
    # ARRANGE: Add a dummy student and teacher
    fresh_manager.students.append(StudentUser(1, "Adam"))
    fresh_manager.teachers.append(TeacherUser(1, "Fekerri", "Piano"))

    # ACT: Call the method to find these users
    user = fresh_manager.find_user_by_id(user_id, type)

    # ASSERT: Check the student and teacher is found
    assert user.id == 1
    assert user.name == expected_msg
    assert user.id == 1
    assert user.name == expected_msg

def test_find_user_failed(fresh_manager):
    # ARRANGE: Start with empty manager
    # ACT: Call the method to find the not exist user
    with pytest.raises(UserNotFound) as e:
        fresh_manager.find_user_by_id(1, "s")

    with pytest.raises(UserNotFound) as z:
        fresh_manager.find_user_by_id(1, "t")

    # ASSERT: Check the error is raised
    assert "Student 1 not found." in str(e)
    assert "Teacher 1 not found." in str(z)
    

def test_find_course_by_id(fresh_manager):
    # ARRANGE: Add a dummy course into the existing manager
    fresh_manager.courses.append(Course(101, "Beginner Piano", "Piano", 0))

    # ACT: Call the method to find the course
    course_id = fresh_manager.courses[0].id
    course = fresh_manager.find_course_by_id(course_id)

    # ASSERT: Check the course is found correctly
    assert course.id == 101
    assert course.name == "Beginner Piano"
    assert course.instrument == "Piano"

def test_remove_user(fresh_manager):
    # ARRANGE: Add a dummy student and teacher user
    fresh_manager.students.append(StudentUser(1, "Adam"))
    fresh_manager.teachers.append(TeacherUser(1, "Fekerri", "Piano"))

    # ACT: Call the remove user method
    student_id = fresh_manager.students[0].id
    teacher_id = fresh_manager.teachers[0].id
    fresh_manager.remove_user(student_id, "s")
    fresh_manager.remove_user(teacher_id, "t")

    # ASSERT: Check the users are remove correctly
    assert len(fresh_manager.students) == 0
    assert len(fresh_manager.teachers) == 0

def test_update_user(fresh_manager):
    # ARRANGE: Add a dummy student and teacher user with course
    fresh_manager.courses.append(Course(101, "Beginner Piano", "Piano", 0))
    fresh_manager.courses.append(Course(102, "Beginner Violin", "Violin", 0))

    fresh_manager.students.append(StudentUser(1, "Adam"))
    student_id = fresh_manager.students[0].id
    fresh_manager.front_desk_enrol(student_id, 101, "s", "Piano")

    fresh_manager.teachers.append(TeacherUser(1, "Fekerri", "Piano"))
    teacher_id = fresh_manager.teachers[0].id

    # ACT: Call the method to update the user.

    fresh_manager.update_user("s", student_id, 
                              name = "Leo", course_id = "102", instrument = "Violin")
    fresh_manager.update_user("t", teacher_id,
                              name = "Winson", speciality = "Violin")
    updated_student = fresh_manager.students[0]
    updated_teacher = fresh_manager.teachers[0]
    
    # ASSERT: Check the users are updated successfully
    assert len(fresh_manager.students) == 1 and len(fresh_manager.teachers) == 1
    assert updated_student.name == "Leo"
    assert updated_student.enrolled_course_ids == [102]
    assert updated_student.enrolled_instruments == ["Piano", "Violin"]
    assert updated_teacher.name == "Winson"
    assert updated_teacher.speciality == "Violin"
    

def test_record_payment_and_history(fresh_manager):
    # ARRANGE: Add a dummy student to the manager for the test.
    # with pytest.raises(CourseNotFound):
    #     fresh_manager.front_desk_register("Adam", 101, "Piano")
    # This test verifies the core financial logic you added in Fragment 5.1.
    # fresh_manager.students.append(...)
    fresh_manager.students.append(StudentUser(1, "Adam"))
    student_id_to_test = 1

    # ACT: Record a payment for that student.
    fresh_manager.record_payment(student_id_to_test, 100.00, "Credit Card")
    
    # ACT 2: Get the payment history.
    history = fresh_manager.get_payment_history(student_id_to_test)

    # ASSERT: Check the results.
    assert len(history) == 1
    assert history[0]['amount'] == 100.00
    assert history[0]['method'] == "Credit Card"
    
def test_get_payment_history_no_results(fresh_manager):
    # TODO: Implement a test that checks if get_payment_history
    # returns an empty list for a student with no payments.
    # ACT 1: initialize a student without any records
    with pytest.raises(CourseNotFound):
        fresh_manager.front_desk_register("Adam", 101, "Piano")
    student_id_to_test = 1

    # ACT 2: obtain the record for this student without records
    history = fresh_manager.get_payment_history(student_id_to_test)

    # ASSERT: Check the result in empty.
    assert len(history) == 0
    assert history == []

def test_course_student_synchronization(fresh_manager):
    # ARRANGE: add two dummy students and one dummy course
    with pytest.raises(UserNotFound):
        fresh_manager.add_course(course_name = "Beginner Piano", 
                                instrument = "Piano", 
                                teacher_id = 1)
    fresh_manager.front_desk_register("Adam", 101, "Piano")
    fresh_manager.front_desk_register("Winson", 101, "Piano")

    # ACT: call the method to synchronize the student and course id
    fresh_manager.sync_courses_students()

    # ASSERT: Check student ids in course object
    assert len(fresh_manager.courses[0].enrolled_student_ids) == 2
    assert fresh_manager.courses[0].enrolled_student_ids == [1,2]

    # ASSERT: Check course id in 
    assert fresh_manager.students[0].enrolled_course_ids == [101]
    assert fresh_manager.students[1].enrolled_course_ids == [101]

    # Save the succeed enrolled state
    # fresh_manager.save_all()

# tests/test_schedule_manager.py
# ... (fixture setup) ...
