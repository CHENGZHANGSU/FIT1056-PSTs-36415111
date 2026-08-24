import json
import datetime
from app.student import StudentUser
from app.teacher import TeacherUser, Course

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="PST3/data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        # TODO: Initialize the new attendance_log attribute as an empty list.
        self.attendance_log = []
        # ... (next_id counters) ...
        self._load_data()
        # ID controller
        self.id = {}

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

    def _refresh(self):
        self._save_data()
        self._load_data()


    def check_in(self, student_id, course_id):
        """Records a student's attendance for a course after validation."""
        # This implementation remains the same, but it will now function correctly.
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)
        
        if not student or not course:
            print("Error: Check-in failed. Invalid Student or Course ID.")
            return False
            
        timestamp = datetime.datetime.now().isoformat()
        check_in_record = {"student_id": student_id, "course_id": course_id, "timestamp": timestamp}
        
        # This line will now work without causing an AttributeError.
        self.attendance_log.append(check_in_record)
        self._save_data() # This will now correctly save the attendance log.
        print(f"Success: Student {student.name} checked into {course.name}.")
        return True

    # TODO: Also implement find_student_by_id and find_course_by_id helper methods.
    # --- Front Desk Functions ---
    def find_student_by_id(self, student_id):
        """A new helper to find one student by their exact ID."""
        # TODO: Loop through student list. If a student's ID matches student_id, return the student object.
        for student in self.students:
            if student['id'] == student_id:
                return student
        # TODO: If the loop finishes without finding a match, return None.
        return None
    
        
    def find_course_by_id(self, course_id):
        """A new helper to find courses by their exact ID."""
        # TODO: Loop through course lists. If a student's ID matches student_id, return the course object.
        for course in self.courses:
            if course['id'] == course_id:
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
            print(f"  ID: {student.get_student_id()}, Name: {student.get_student_name()}, Enrolled in: {student.get_enrolled_course_ids()}")

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

