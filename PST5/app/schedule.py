import json, datetime, re, os, logging, time
import streamlit as st
import pandas as pd

from app.student import StudentUser
from app.teacher import TeacherUser, Course
from algorithms.algorithm import merge_sort, binary_search

from Exceptions.NotFoundException import UserNotFound, CourseNotFound

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s %(levelname)s %(name)s %(message)s"
)
log = logging.getLogger("carelog    ")

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        # TODO: Initialize the new attendance_log attribute as an empty list.
        self.attendance_log = []
        self.finance_log = []
        # ... (next_id counters) ...
        self.id = {}
        self._load_data()
        self._to_object()

    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                # TODO: Load students, teachers, and courses as before.
                # ...
                self.students = data.get("students", [])
                self.teachers = data.get("teachers", [])
                self.courses = data.get("courses", [])
                # TODO: Correctly load the attendance log.
                # Use .get() with a default empty list to prevent errors if the key doesn't exist.
                self.attendance_log = data.get("attendance", [])
                self.finance_log = data.get("finance", [])
                self.id = data.get("id_counters", {})
                
        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")
    
    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        # TODO: Create a 'data_to_save' dictionary.
        data_to_save = {
            "students": [s.__dict__ for s in self.students],
            "teachers": [t.__dict__ for t in self.teachers],
            "courses": [c.__dict__ for c in self.courses],
            # TODO: Add the attendance_log to the dictionary to be saved.
            # Since it's already a list of dicts, no conversion is needed.
            "attendance": self.attendance_log,
            "finance": self.finance_log,
            # ... (next_id counters) ...
            "id_counters": self.id
        }
        # TODO: Write 'data_to_save' to the JSON file.
        with open(self.data_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def _course_ids(self) -> list[int]:
        """Helper function return list of course ids"""
        lst = []
        for course in self.courses:
            lst.append(course.get_course_id())
        return lst        

    def sync_courses_students(self):
        """
        Helper function synchronize enrolled students ids in course.
        The course student ids should obey students.
        """
        for course in self.courses:
            course_id = course.get_course_id()
            enrolled_student_ids = course.get_enrolled_student_ids()

            for student in self.students:
                student_id = student.get_id()
                enrolled_course_ids = student.get_enrolled_course_ids()

                if (course_id in enrolled_course_ids) & (student_id not in enrolled_student_ids):
                    course.enroll_student_in_course(student_id)       # enroll the missing student in to the course
                if (course_id not in enrolled_course_ids) & (student_id in enrolled_student_ids):
                    course.remove_enrolled_student_id(student_id)     # remove the student not enroll in the course

        remove_course_ids = []                                        # remove the enrolled course id in student, if the course is removed
        for student in self.students:
            student_id = student.get_id()
            enrolled_course_ids = student.get_enrolled_course_ids()

            course_exist = True
            for enrolled_course_id in enrolled_course_ids:
                if enrolled_course_id not in self._course_ids():      # check the existence of course id
                    course_exist = False
                    remove_course_ids.append(enrolled_course_id)

            if not course_exist:
                student.remove_enrolled_course_id(remove_course_ids)
                remove_course_ids.clear()

    def save_all(self):
        self.sync_courses_students()
        self._save_data()

    def _refresh(self):
        self._save_data()
        self._load_data()

    def _to_object(self):
        """Converts dictionaries back to their respective object types."""
        if len(self.students) != 0:
            for i in range(len(self.students)):
                student = self.students[i]
                new_student = StudentUser(student['id'], student['name'])
                if len(student['enrolled_course_ids']) != 0:
                    new_student.set_enrolled_course_ids(student['enrolled_course_ids'])
                if len(student['enrolled_instruments']) != 0:
                    new_student.set_enrolled_instruments(student['enrolled_instruments'])
                self.students[i] = new_student

        if len(self.teachers) != 0:
            for i in range(len(self.teachers)):
                teacher = self.teachers[i]
                new_teacher = TeacherUser(teacher['id'], teacher['name'], teacher['speciality'])
                self.teachers[i] = new_teacher

        if len(self.courses) != 0:
            for i in range(len(self.courses)):
                course = self.courses[i]
                new_course = Course(course['id'], course['name'], course['instrument'], course['teacher_id'])
                if len(course['lessons']) != 0:
                    new_course.set_list_lessons(course['lessons'])
                if len(course['enrolled_student_ids']) != 0:
                    new_course.set_enroll_student_lst(course['enrolled_student_ids'])
                self.courses[i] = new_course

    def _to_dict(self):
        self.students = [s.__dict__ for s in self.students]
        self.teachers = [t.__dict__ for t in self.teachers]
        self.courses = [c.__dict__ for c in self.courses]

    def check_in(self, student_id, course_id):
        """Records a student's attendance for a course after validation."""
        # This implementation remains the same, but it will now function correctly.
        student = self.find_user_by_id(student_id, "s")
        course = self.find_course_by_id(course_id)
        
        if not student or not course:
            print("Error: Check-in failed. Invalid Student or Course ID.")
            log.info("Student check-in failed | id=%s | course=%s", student_id, course_id)
            return False
            
        timestamp = datetime.datetime.now().isoformat()
        check_in_record = {"student_id": student_id, "course_id": course_id, "timestamp": timestamp}
        
        # This line will now work without causing an AttributeError.
        self.attendance_log.append(check_in_record)
        self._save_data() # This will now correctly save the attendance log.
        print(f"Success: Student {student.get_name()} checked into {course.get_course_name()}.")
        log.info("Student check-in successfully | id=%s | name=%s | course=%s", student_id, student.get_name(), course.get_course_name())
        return True
    

#--------------- Search Functions For Data Management ---------------#
    # TODO: Also implement find_student_by_id and find_course_by_id helper methods.
    # --- Front Desk Functions ---
    def find_user_by_id(self, user_id, type):
        """A new helper to find one student by their exact ID."""
        match type.lower() or type[0].lower():
            # Implement binary search to search for specific users.
            case "s":
                self._obey_order("s")
                index = binary_search(self.students, user_id)
                if index != None :
                    return self.students[index]
                raise UserNotFound(f"Student {user_id} not found.")
            case "t":
                self._obey_order("t")
                index = binary_search(self.teachers, user_id)
                if index != None:
                    return self.teachers[index]
                raise UserNotFound(f"Teacher {user_id} not found.")
            case _:
                raise UserNotFound("User not found.")
    
        
    def find_course_by_id(self, course_id, enrolled_id:list[int]=[0], type="None"):
        """
        A new helper to find courses by their exact ID.
        Implemented any course related actions. (Enroll students or teachers to a course)
        """
        # TODO: Loop through course lists. If a student's ID matches student_id, return the course object.
        for course in self.courses:
            if course.get_course_id() == int(course_id):
                if int(enrolled_id[0]) != 0:
                    match type[0].casefold():
                        case "s":                   # if a student enroll in this course 
                            course.enroll_student_in_course(enrolled_id[0])
                            return
                        case "t":                   # if a teacher enroll in this course
                            self.enroll_teacher_to_course(course, enrolled_id[0])
                        case "None":
                            pass
                        case _:
                            print("Invalid Syntax.\n")
                return course
        # TODO: If the loop finishes without finding a match, return None.
        raise CourseNotFound

    def front_desk_daily_roster(self, type:str, course_name = None, weekday = None):
        match type.casefold():
            case "c":   # find all the lessons of only given course name (course name provided)
                if course_name:
                    course = self._find_course_by_name(course_name)
                    if course:
                        return (course, course.get_lessons())
                    else:
                        raise CourseNotFound
            case "l":   # find the lessons on specific weekday given the course name (both)
                if course_name:
                    course = self._find_course_by_name(course_name)
                    if course:
                        return self._find_lesson(course, weekday)
                    else:
                        raise CourseNotFound
            case "a":   # find all the course and lessons of only given weekday (weekday provided)
                courses = []
                lessons = []
                lst_course = self.courses.copy()
                for course in lst_course:
                    found = False
                    approp_lessons = []
                    for lesson in course.get_lessons():
                        if lesson['day'] == str(weekday):
                            found = True
                            approp_lessons.append(lesson)
                    if found:
                        cur_course = Course(course.get_course_id(), course.get_course_name(), course.get_course_instrument(), course.get_course_teacher_id(),
                                        course.get_enrolled_student_ids(), course.get_lessons())
                        courses.append(cur_course)  # if the course contains the lessons with specified weekday
                        lessons.append(approp_lessons)  # the lessons of the current course with specified weekday
                if len(courses) >= 1:
                    return (courses, lessons)
                else:
                    raise CourseNotFound

    def _find_course_by_name(self, course_name:str):
        lst_course = self.courses.copy()
        for course in lst_course:
            if course.get_course_name() == str(course_name):
               return Course(course.get_course_id(), course.get_course_name(), course.get_course_instrument(), course.get_course_teacher_id(), 
                             course.get_enrolled_student_ids(), course.get_lessons())

    def _find_lesson(self, course:Course, day = None):
        lessons = []
        # if the specified weekday exist
        if day:
            for lesson in course.get_lessons():
                if lesson['day'] == str(day):
                    lessons.append(lesson)   
            return (course, lessons.copy())
        else:
            return(course, course.get_lessons())


    def get_course_list(self):
        return self.courses
    

#--------------- Quick View For Database Management ---------------#
    def list_students(self, order):
        """Prints all students in the database."""
        res_lst = []
        match order[0].lower() or order.lower():
            case "a":
                res_lst = self._obey_order("s")
                self.students = res_lst
                res = [s.__dict__ for s in res_lst]
                return res
            case "d":
                res_lst = self._obey_order("s", "descending")
                self.students = res_lst
                res = [s.__dict__ for s in res_lst]
                return res
            case _:
                print("Invalid Syntax.\n")

        print("\n--- Student List ---")
        if not self.students:
            print("No students in the system.")
            return
        # TODO: Loop through student_db. For each student, print their ID, name, and their enrolled_in list.
        for student in self.students:
            print(f"  ID: {student.get_id()}, Name: {student.get_name()}, Enrolled in: {student.get_enrolled_course_ids()}")

    def list_teachers(self, order):
        """Prints all teachers in the database."""
        match order[0].lower():
            case "a":
                self._obey_order("s") 
            case "d":
                self._obey_order("s", "descending")
            case _:
                print("Invalid Syntax.\n")

        # TODO: Implement the logic to list all teachers, similar to list_students().
        print("\n--- Teacher List ---")
        if not self.teachers:
            print("No teachers in the system.")
            return None
        for teacher in self.teachers:
            print(f"  ID: {teacher.get_teacher_id()}, Name: {teacher.get_teacher_name()}, Speciality: {teacher.get_teacher_speciality()}")

    def list_attendance(self):    
        """Prints all attendance records in the database"""
        print("\n--- Attendance Records ---")
        if not self.attendance_log:
            print("No attendance records in the system.")
            return None
        for record in self.attendance_log:
            print(f"  Student ID: {record['student_id']}, Course ID: {record['course_id']}, Timestamp: {record['timestamp']}")

    def list_course_lessons(self, course=None):
        """Print all lessons with the corresponding course"""
        if course:
            print(f"\n--- Lessons in course {course.get_course_id()}---")
            for lesson in course.get_lessons():
                print(f"  Lesson id: {lesson['lesson_id']} on {lesson['day']}, start at {lesson['start_time']} in {lesson['room']}")
        else:
            print("No course or lesson found in the system.")
            return None


    def print_student_card(self, student_id):
        """Creates a text file badge for a student."""
        # TODO: Find the student dictionary in app_data['students'].
        student_to_print = None
        for student in self.students:
            if student.get_id() == student_id:
                student_to_print = student
                break
        
        if student_to_print:
            # TODO: Create a filename, e.g., f"{student_id}_card.txt".
            filename = f"data/{student_id}_card.txt"
            enrolled_courses = student_to_print.get_enrolled_course_ids()
            enrolled_courses_str = ', '.join(str(course_id) for course_id in enrolled_courses)
            # TODO: Open the file in write mode ('w').
            with open(filename, 'w') as f:
                # Write the student's details to the file in a nice format.
                f.write("========================\n")
                f.write(f"  MUSIC SCHOOL ID BADGE\n")
                f.write("========================\n")
                f.write(f"ID: {student_to_print.get_id()}\n")
                f.write(f"Name: {student_to_print.get_name()}\n")
                f.write(f"Enrolled In: {enrolled_courses_str}\n")
            print(f"Printed student card to {filename}.")
            return filename
        else:
            print(f"Error: Could not print card, student {student_id} not found.")

#--------------- Front Desk Functions For Database Management ---------------#
    def front_desk_register(self, name, course_id, instruments:str) -> StudentUser:
        """High-level function to register a new student and enrol them."""
        student_id = self.id['next_student_id']
        # TODO: Create a new Student object, add it to student_db, and increment the ID.
        new_student = StudentUser(student_id, name)
        self.students.append(new_student)
        self.id['next_student_id'] += 1
        
        # TODO: Immediately call front_desk_enrol() using the new student's ID and the provided instrument.
        self.front_desk_enrol(new_student.get_id(), course_id, "s", instruments)
        print(f"Front Desk: Successfully registered '{name}' and enrolled in '{course_id}'.")
        log.info("Student added | id=%s | name=%s | instruments=%s", student_id, name, instruments)
        return new_student

    def front_desk_enrol(self, user_id, course_id, type:str, instruments:str):
        """High-level function to enrol an existing user in a course."""
        user = StudentUser|TeacherUser
        match type:
            case "s":
                user = self.find_user_by_id(user_id, type)
            case "t":
                user = self.find_user_by_id(user_id, type)
            case _:
                print("Invalid type of finding a user.\n")
                user = None

        # TODO: If the user is found, append the course to their 'enrolled_in' list.
        if user:
            course = self.find_course_by_id(course_id)
            # If course is valid
            if course:
                match user:
                    case StudentUser():
                        self.find_course_by_id(course_id, [user_id], "s")       # Enroll student id into course object
                        user.enroll_course_ids(course_id)                       # Enroll course id into student object
                        user.set_enrolled_instrument(instruments)               # Set the enrolled instrument for the student
                        print(f"Front Desk: Enrolled student {user_id} in '{course_id}'.")
                        log.info("Student enrolled successfully | id=%s | course=%s", user_id, course_id)
                    case TeacherUser():
                        self.find_course_by_id(course_id, [user_id], "t")
                    case _:
                        print("Invalid type of finding a user.\n")
                        return None
            else:
                print(f"Front Desk: Course id {course_id} not found.")
                log.info("Failed to find Course | user_id=%s | course_id=%s", user_id, course_id)
        else:
            # TODO: If the user is not found, print an error message like "Error: Student ID not found."
            print(f"Error: User ID {user_id} not found.")
            log.info("Failed to find user | user_id=%s", user_id)

    def add_teacher(self, name, speciality):
        """Adds a teacher dictionary to the data storage."""
        # TODO: Get the next teacher ID from app_data['next_teacher_id'].
        teacher_id = self.id['next_teacher_id']
        # TODO: Create a new teacher dictionary with 'id', 'name', and 'speciality' keys.
        new_teacher = TeacherUser(teacher_id, name, speciality)
        # TODO: Append the new dictionary to the app_data['teachers'] list.
        self.teachers.append(new_teacher)
        # TODO: Increment the 'next_teacher_id' in app_data.
        self.id['next_teacher_id'] += 1
        print(f"Core: Teacher '{name}' added.")

    def enroll_teacher_to_course(self, course:Course, enrolled_id:int):
        """Helper function used to enroll/re-enroll a new teacher in a course"""
        if course.get_course_teacher_id() != 0:                 # if there exist an enrolled teacher
            print(f"Teacher {course.get_course_teacher_id()} already enroll in this course.")
            user_input = input("Do you want to replace? (y/n): ")
            match user_input[0].lower():
                case "y":
                    course.set_teacher_id(enrolled_id)
                    teacher = self.find_user_by_id(enrolled_id, "t")
                    if teacher != None:
                        course.set_instrument(teacher.get_teacher_speciality())
                case "n":
                    print("\n")
                case _:
                    print("Invalid Syntax occur.\n")
        elif course.get_course_teacher_id() == 0:               # if no enrolled teacher found
            course.set_teacher_id(enrolled_id)
            print(f"Teacher {enrolled_id} has enrolled in course {course.get_course_id()}.\n")

    def remove_user(self, user_id, type):
        """Removes a user from the system"""
        user = StudentUser|TeacherUser
        match type:
            case "s":
                user = self.find_user_by_id(user_id, type)
                if not user:
                    raise UserNotFound
            case "t":
                user = self.find_user_by_id(user_id, type)
                if not user:
                    raise UserNotFound
            case _:
                print("Invalid type of finding a user.\n")
                raise UserNotFound

        # Remove the user and the responding courses they enrolled or taught
        match user:
            case StudentUser():
                try:
                    self._remove_user_in_course(user)
                    self.students.remove(user)
                    print(f"Student {user.get_name()} has been removed.\n")
                    log.info("Remove a student | id=%s | name=%s", user_id, user.get_name())
                    self.sync_courses_students()  # Synchronize the enrolled students in courses after updating
                    st.success(f"Remove the student {user.get_name()} successfully.")
                except Exception as e:
                    raise e

            case TeacherUser():
                self._remove_user_in_course(user)
                self.teachers.remove(user)
                print(f"Teacher {user.get_name()} has been removed.\n")
                self.sync_courses_students()  # Synchronize the enrolled students in courses after updating 
            case _:
                print("Invalid type of recognizing a user.\n")

    def _remove_user_in_course(self, user:StudentUser|TeacherUser):
        """Removes a user from all courses they are enrolled in or teaching."""
        match user:
            case StudentUser():
                for course in self.courses:
                    if user.get_id() in course.get_enrolled_student_ids():
                        course.remove_enrolled_student_id(user.get_id())
                        print(f"{user.get_name()} has been removed from course {course.get_course_id()}.")
            case TeacherUser():
                for course in self.courses:
                    if user.get_id() == course.get_course_teacher_id():
                        course.set_teacher_id(-1)   # means no teacher currently taking this course
                        print(f"{user.get_name()} has been removed from course {course.get_course_id()}.")
            case _:
                print("Invalid type of user, failed to match in any courses.\n")

    def update_user(self, type, user_id, **field):
        """Updates a user's information in the system."""
        match type:
            case "s":
                print("\n----- Updating a student user -----")
                student = None
                try:
                    student = self.find_user_by_id(user_id, "s")
                except UserNotFound as e:
                    raise e
                choice = "u"
                
                # Transform list of string to integer
                courses = field["course_id"].replace(" ", "").split(",")
                course_list = [int(x) for x in courses if x.isdigit()]

                # instruments = field["instrument"].replace(" ", "").split(",")
                # instrument_list = [x for x in instruments if x != ""]

                # Remove enrollment or update multiple enrollments
                if student:
                    match choice[0].lower():
                        case "r":
                            student.remove_enrolled_course_id(field['course_id'])
                            student.update(name = field['name'], course_id = [], instruments = [])
                            st.success(f"Successfully update {field['name']}!")
                            print(f"Student {field['name']} update successfully.\n")
                            log.info("Student Updated | new_id=%s | new_name=%s | new_courses=%s | new_instruments=%s",
                                     user_id, field['name'], field['course_id'], field['instrument'])
                            return
                        case "u":
                            student.update(name = field['name'], course_id = course_list, instrument = field['instrument'])
                            st.success(f"Student {field['name']} update successfully!")
                            print(f"Student {field['name']} update successfully.\n")
                            log.info("Student Updated | new_id=%s | new_name=%s | new_courses=%s | new_instruments=%s",
                                     user_id, field['name'], field['course_id'], field['instrument'])
                            self.sync_courses_students()  # Synchronize the enrolled students in courses after updating
                            return
                        case _:
                            print("Invalid Syntax.\n")
                            return None
                else:
                    print(f"Student {user_id} not found.\n")
                    return None
            case "t":
                print("\n----- Updating a teacher user -----")
                teacher = self.find_user_by_id(user_id, "t")
                if teacher:
                    teacher.update(name = field['name'], speciality = field['speciality'])
                    print(f"Teacher {field['name']} update successfully.\n")
                else:
                    print(f"Teacher {user_id} not found.\n")
                    return None
            case _:
                print("Invalid user detected.\n")
                return None

    def _course_title(self, course_id):
        # arg = f"Enter the course id need to {action}: "
        # user_input = int(input(arg))
        course = self.find_course_by_id(int(course_id))
        if course:
            return course
        else:
            print(f"Course id {course_id} not found, fail to update.\n")
            return None

    def add_course(self, **field):
        """Add a specific course to the system"""
        new_course_id = self.id['next_course_id']
        enrolled_teacher_id = field['teacher_id']

        if self.find_user_by_id(enrolled_teacher_id, "t"):
            new_course = Course(new_course_id, field['course_name'], field['instrument'], field['teacher_id'])

            # self.add_lessons(new_course)                                   # Add lessons into the course through users
            self.courses.append(new_course)
            self.id['next_course_id'] += 1
            sep_string = f"with {new_course.get_course_instrument()} added successfully.\n"
            print(f"Course {new_course.get_course_id()} {new_course.get_course_name()} by teacher {new_course.get_course_teacher_id()}", sep_string)
            log.info("Course Added | new_id=%s | new_name=%s | new_instrument=%s | new_teacher_id=%s",
                    new_course.get_course_id(), new_course.get_course_name(), new_course.get_course_instrument(), 
                    new_course.get_course_teacher_id())
        else:
            print(f"Teacher {enrolled_teacher_id} not found. Please enroll a valid teacher.\n")
            log.warning("Course Creation Failed | teacher_id=%s", enrolled_teacher_id)
            raise UserNotFound

    def _str_to_bool(self, user_input:str) -> bool:
        """Helper method to convert user input to boolean."""
        match user_input:
            case "y":
                return True
            case "n":
                return False
            case _:
                print("Invalid Syntax.\n")
                return False

    def _required_lesson_info(self) -> tuple:
        """Helper method used to collect the lesson related information"""
        pattern = r"d{2}:d{2}"
        lesson_id = self.id['next_lesson_id']
        day = input("Which day the lesson will be (e.g. Monday): ")
        start_time = input("Enter the lesson time (e.g. 14:30): ")

        if not re.match(pattern, start_time) and start_time.replace(" ", "") != "":               # Check the format of datetime 
            start_time = f"{start_time[0:2]}:{start_time[3:]}"

        room = input("Enter the room of the lesson (e.g. Room A): ")
        return (lesson_id, day, start_time, room)

    def _lesson_title(self, arg:str) -> bool:
        """Helper function to consist with OCP principle"""
        arg = f"\nDo you want to {arg} a lesson? (y/n) "
        user_input = input(arg)[0]
        choice = self._str_to_bool(user_input)
        return choice

    def add_lessons(self, course, info):
        print("\n----- Adding lessons to the course -----")
        # choice = self._lesson_title("add")
        if course == None:
            course_id = int(input("Enter the course id need to add lessons: "))
            course = self.find_course_by_id(course_id)

        if course:
            # while choice:
            # info = self._required_lesson_info()
            new_lesson = {'lesson_id': info[0], 'day': info[1], 'start_time': info[2], 'room': info[3]}
            self.id['next_lesson_id'] += 1
            # choice = self._lesson_title("add")

            # Check whether the lesson(s) added correctly.
            course.add_lesson_to_course(new_lesson)
            for lesson in course.get_lessons():
                print(f"Lesson {lesson['lesson_id']} in course {course.get_course_id()} added successfully.")
        else:
            return

    def update_course(self, **field):
        """Updates a course's information in the system."""
        print("\n----- Updating a course from the system -----")
        course = self._course_title(field["course_id"])
        if course:
            if self.find_user_by_id(field['teacher_id'], "t"):
                course.update(course_name = field["course_name"], instrument = field['instrument'], teacher_id = field["teacher_id"])
            else:
                course.update(course_name = field["course_name"], instrument = field['instrument'], teacher_id = 0)
                print(f"Teacher {field['teacher_id']} not found, fail to update teacher id. \n")
            print(f"Course {field['course_name']} updated successfully.\n")

            # choice = self._str_to_bool(input("Do you want to update lessons in this course? (y/n): "))
            # if choice:
            #     self.update_lesson(course)
        else:   
            return None

    def update_lesson(self, course, info):
        """Update lessons with the corresponding course"""
        # if not course:
        #     course = self._course_title("update")

        if course:
            # choice = self._lesson_title("update")
            # while choice:
            self.list_course_lessons(course)
            print(f"\n----- Adding lessons from the course {course.get_course_id()} -----")
            # lesson_id = int(input("Enter the lesson id need updates: "))
            # info = self._required_lesson_info()
            field = {'lesson_id': info[0], 'day': info[1], 'start_time': info[2], 'room': info[3]}
                                    
            for lesson in course.get_lessons():                     # Update the corresponding lesson dictionary
                if int(info[0]) == lesson['lesson_id']:
                    updates = field.copy()
                    for key, value in field.items():                # If user type nothing or same as origin, no need any updates
                        if (value == lesson[key]) or (value.replace(" ", "") == ""):
                            updates.pop(key, None)
                    if len(updates) != 0:
                        lesson.update(updates)
                        print(f"Lesson {info[0]} updates successfully.")
                    else:
                        print(f"Lesson {info[0]} remains the same.")
                    break

                # choice = self._lesson_title("update")
        else:
            return None

    def remove_course(self, course):
        print("\n----- Removing a course from the system -----")
        # course = self._course_title("remove")

        if course:
            print(course)
            # choice = self._str_to_bool(input("Do you want to remove this course? (y/n): "))
            # if choice:
            self.courses.remove(course)
            for student in self.students:
                if course.get_course_id() in student.get_enrolled_course_ids():
                    student.get_enrolled_course_ids().remove(course.get_course_id())
        else:
            return None

    def remove_lessons(self):
        """Update lessons with the corresponding course"""
        course = self._course_title("remove")
        choice = self._lesson_title("remove")

        if course:
            print(f"\n----- Removing lessons from the course {course.get_course_id()} -----")
            while choice:
                self.list_course_lessons(course)
                lesson_id = int(input("\nEnter the lesson id need removes: "))
                                        
                for lesson in course.get_lessons():         # Update the corresponding lesson dictionary
                    if lesson_id == lesson['lesson_id']:
                        course.get_lessons().remove(lesson)
                        print(f"Lesson {lesson_id} removes successfully.")
                        break

                if len(course.get_lessons()) == 0:          # if no lesson left, terminate the loop
                    print(f"No lesson in course {course.get_course_id()}.\n")
                    return None
                choice = self._lesson_title("remove")
        else:
            return None

#--------------- Front desk methods for student payment ---------------#
    def record_payment(self, student_id:int, amount, method) -> bool:
        """
        Record the new payment from student as dictionary.
        """
        new_payment = {"student_id": student_id, "amount": amount, "payment method": method, "timestamp": datetime.datetime.now().isoformat()}
        try:
            self.finance_log.append(new_payment)
            log.info("Payment success | student_id=%s | amount=%s | payment method=%s | t", student_id, amount, method)
            return True
        except Exception as e:
            log.warning("Payment failed | student_id=%s | reason=%s", student_id, e)
            return False

    def get_payment_history(self, student_id:int) -> list[dict]:
        """
        Retrieve all the payment records for a student via id.
        """
        records = []
        student = self.find_user_by_id(int(student_id), "s")

        if not student:
            log.warning("Student not found | student_id=%s", student_id)
            return records

        for finance in self.finance_log:
            if int(finance['student_id']) == int(student_id):
                records.append(finance)

        if records:
            log.info("Records found | student_id=%s", student_id)
        else:
            log.info("Records not found | student_id=%s", student_id)
        return records

    def export_report(self, kind, out_path):
        """Exports a log to a CSV file."""
        print(f"Exporting {kind} report to {out_path}...")
        # TODO: Use an if/elif block to select the correct data list based on 'kind'.
        if kind == "finance":
            self.database_to_csv("finance", "ascending", out_path)
        elif kind == "attendance":
            self.database_to_csv("attendance", "ascending", out_path)
        else:
            print("Error: Unknown report type.")
            return
         

#--------------- Algorithms For Database Management ---------------#
    def _obey_order(self, type = "s", order = "ascending") -> list:
        """
        Sort the database of each list in dict according to user need. 
        """
        match type:
            case "s":
                return self._sort_data(order, self.students)
            case "t":
                return self._sort_data(order, self.teachers)
            case "c":
                return self._sort_data(order, self.courses)
            case "a":
                return self.attendance_log
            case "f":
                return self.finance_log
            case _:
                print("Invalid Syntax in order.\n")
                return []

    def _sort_data(self, order, lst) -> list:
        """Sort the system data into different orders"""
        match order[0].lower():
            case "a":
                return merge_sort(lst, "ascending")
            case "d":
                return merge_sort(lst, "descending")
            case _:
                print("Invalid Syntax.\n")
                return []
    
#--------------- Print as .csv file for Database Management ---------------#
    def _return_data(self, type="s") -> list:
        match type:
            case "s":
                return self.students
            case "t":
                return self.teachers
            case "a":
                return self.attendance_log
            case "f":
                return self.finance_log
            case _:
                return []

    # @st.cache_data
    def _print_to_csv(self, lst:list, order:str, type:str, folder_path=None):
        if not folder_path:
            folder_path = "output_csv"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        if order.replace(" ", "") != "":
            self._obey_order(f"{type[0].lower()}", order.casefold())
        self._to_dict()
        lst = self._return_data(f"{type[0].lower()}")
        df = pd.DataFrame(data = lst)
        try:
            if len(lst) == 0:
                print(f"There is nothing inside {type.casefold()} database")
            print("File generated.\n")
            self._to_object()
            # return df.to_csv().encode('utf-8')
            return df.to_csv(f"{folder_path}/{type.capitalize()}.csv", index = True, encoding = 'utf-8')
        except:
            self._to_object()
            print("Error, please check the database and try again.\n")
            return None  

    def database_to_csv(self, choice, order='ascending', folder_path=None):
        """
        High-level function to transform the database into csv file.
        """
        # choice = input("Which data should be transformed into .csv file? (s/t/a/whole): ")
        # order = ""
        # if choice[0].lower() != "a":
        #     order = input("Which order should the data presented? (ascending / descending): ")

        match (choice[0].lower()):                                         # match various options
            case "s":
                return self._print_to_csv(self.students, order, "student", folder_path)
            case "t":
                return self._print_to_csv(self.teachers, order, "teacher", folder_path)
            case "a":
                return self._print_to_csv(self.attendance_log, "", "attendance", folder_path)
            case "f":
                return self._print_to_csv(self.finance_log, order, "finance", folder_path)
            # case "w":
            #     success = False
            #     lst = {"student": self.students, "teacher": self.teachers, "attendance": self.attendance_log}
            #     for key, value in lst.items():
            #         if key == "attendance":
            #             order = ""
            #         if self._print_to_csv(value, order, key, folder_path):
            #             success = True
            #         else:
            #             continue
            #     return success
            case _:
                print("Unknown data")
                return False
