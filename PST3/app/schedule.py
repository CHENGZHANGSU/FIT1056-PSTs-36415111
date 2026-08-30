import json
import datetime
from app.student import StudentUser
from app.teacher import TeacherUser, Course

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        # TODO: Initialize the new attendance_log attribute as an empty list.
        self.attendance_log = []
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
            # ... (next_id counters) ...
            "id_counters": self.id
        }
        # TODO: Write 'data_to_save' to the JSON file.
        with open(self.data_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def save_all(self):
        self._save_data()

    def _to_object(self):
        """Converts dictionaries back to their respective object types."""
        for i in range(len(self.students)):
            student = self.students[i]
            new_student = StudentUser(student['id'], student['name'])
            if len(student['enrolled_course_ids']) != 0:
                new_student.set_enrolled_course_ids(student['enrolled_course_ids'])
            self.students[i] = new_student

        for i in range(len(self.teachers)):
            teacher = self.teachers[i]
            new_teacher = TeacherUser(teacher['user_id'], teacher['name'], teacher['speciality'])
            self.teachers[i] = new_teacher

        for i in range(len(self.courses)):
            course = self.courses[i]
            new_course = Course(course['id'], course['name'], course['instrument'], course['teacher_id'])
            if len(course['lessons']) != 0:
                new_course.set_list_lessons(course['lessons'])
            if len(course['enrolled_student_ids']) != 0:
                new_course.set_enroll_student_lst(course['enrolled_student_ids'])
            self.courses[i] = new_course

    def check_in(self, student_id, course_id):
        """Records a student's attendance for a course after validation."""
        # This implementation remains the same, but it will now function correctly.
        student = self.find_user_by_id(student_id, "s")
        course = self.find_course_by_id(course_id)
        
        if not student or not course:
            print("Error: Check-in failed. Invalid Student or Course ID.")
            return False
            
        timestamp = datetime.datetime.now().isoformat()
        check_in_record = {"student_id": student_id, "course_id": course_id, "timestamp": timestamp}
        
        # This line will now work without causing an AttributeError.
        self.attendance_log.append(check_in_record)
        self._save_data() # This will now correctly save the attendance log.
        print(f"Success: Student {student.get_name()} checked into {course.get_course_name()}.")
        return True

    # TODO: Also implement find_student_by_id and find_course_by_id helper methods.
    # --- Front Desk Functions ---
    def find_user_by_id(self, user_id, type):
        """A new helper to find one student by their exact ID."""
        match type.lower() or type[0].lower():
            case "s":
                # TODO: Loop through student list. If a student's ID matches student_id, return the student object.
                for student in self.students:
                    if student.get_id() == user_id:
                        return student
            case "t":
                for teacher in self.teachers:
                    if teacher.get_id() == user_id:
                        return teacher
            case _:
                print("User not found.\n")
        # TODO: If the loop finishes without finding a match, return None.
        return None
    
        
    def find_course_by_id(self, course_id, enrolled_student_id:int=0):
        """A new helper to find courses by their exact ID."""
        # TODO: Loop through course lists. If a student's ID matches student_id, return the course object.
        for course in self.courses:
            if course.get_course_id() == course_id:
                if enrolled_student_id != 0:    # if a student enroll in this course
                    course.enroll_student_in_course(enrolled_student_id)
                return course
        # TODO: If the loop finishes without finding a match, return None.
        return None

    def get_course_list(self):
        return self.courses

    def list_students(self):
        """Prints all students in the database."""
        print("\n--- Student List ---")
        if not self.students:
            print("No students in the system.")
            return
        # TODO: Loop through student_db. For each student, print their ID, name, and their enrolled_in list.
        for student in self.students:
            print(f"  ID: {student.get_id()}, Name: {student.get_name()}, Enrolled in: {student.get_enrolled_course_ids()}")

    def list_teachers(self):
        """Prints all teachers in the database."""
        # TODO: Implement the logic to list all teachers, similar to list_students().
        print("\n--- Teacher List ---")
        if not self.teachers:
            print("No teachers in the system.")
            return
        for teacher in self.teachers:
            print(f"  ID: {teacher.get_teacher_id()}, Name: {teacher.get_teacher_name()}, Speciality: {teacher.get_teacher_speciality()}")

    def list_attendance(self):
        """Prints all attendance records in the database"""
        pass

    def front_desk_register(self, name, course_id):
        """High-level function to register a new student and enrol them."""
        student_id = self.id['next_student_id']
        # TODO: Create a new Student object, add it to student_db, and increment the ID.
        new_student = StudentUser(student_id, name)
        self.students.append(new_student)
        self.id['next_student_id'] += 1
        
        # TODO: Immediately call front_desk_enrol() using the new student's ID and the provided instrument.
        self.front_desk_enrol(new_student.get_id(), course_id)
        print(f"Front Desk: Successfully registered '{name}' and enrolled in '{course_id}'.")

    def front_desk_enrol(self, student_id, course_id):
        """High-level function to enrol an existing student in a course."""
        # TODO: Use your new find_student_by_id() helper.
        student = self.find_user_by_id(student_id, "s")
        # TODO: If the student is found, append the course to their 'enrolled_in' list.
        if student:
            course = self.find_course_by_id(course_id)
            # If course is valid
            if course:
                self.find_course_by_id(course_id, student_id)   # Enroll student id into course object
                student.enroll_course_ids(course_id)            # Enroll course id into student object
                print(f"Front Desk: Enrolled student {student_id} in '{course_id}'.")
            else:
                print(f"Front Desk: Course id {course_id} not found.")
        else:
            # TODO: If the student is not found, print an error message like "Error: Student ID not found."
            print(f"Error: Student ID {student_id} not found.")

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

    def remove_user(self, user_id, type):
        user = StudentUser|TeacherUser
        match type:
            case "s":
                user = self.find_user_by_id(user_id, type)
            case "t":
                user = self.find_user_by_id(user_id, type)
            case _:
                print("Invalid type of finding a user.\n")
                return None
                
        match user:
            case StudentUser():
                self._remove_user_in_course(user)
                self.students.remove(user)
                print(f"Student {user.get_name()} has been removed.\n")

            case TeacherUser():
                self._remove_user_in_course(user)
                self.teachers.remove(user)
                print(f"Teacher {user.get_name()} has been removed.\n")
            case _:
                print("Invalid type of recognizing a user.\n")

    def _remove_user_in_course(self, user:StudentUser|TeacherUser):
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
    

