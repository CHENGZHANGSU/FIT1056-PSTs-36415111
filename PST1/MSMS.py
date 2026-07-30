# MSMS.py - The In-Memory Prototype

# --- Data Models ---
class Student:
    """A blueprint for student objects. Holds their info."""
    def __init__(self, student_id, name):
        self.id = student_id
        self.name = name
        # TODO: Initialize an empty list called 'enrolled_in' to store instrument names.
        self.enrolled_in = []

    
class Teacher:
    """A blueprint for teacher objects."""
    def __init__(self, teacher_id, name, speciality):
        # TODO: Assign all three parameters (teacher_id, name, speciality)
        # to instance variables (e.g., self.id = teacher_id).
        self.id = teacher_id
        self.name = name
        self.speciality = speciality


# --- In-Memory Databases ---
# TODO: Create the global data stores.
student_db = []
teacher_db = []
next_student_id = 1
next_teacher_id = 1

# --- Core Helper Functions ---
def add_teacher(name, speciality):
    """Creates a Teacher object and adds it to the database."""
    global next_teacher_id
    # TODO: Create a new Teacher object using the next available ID.
    new_teacher = Teacher(next_teacher_id, name, speciality)
    # TODO: Append the new_teacher to the teacher_db list.
    teacher_db.append(new_teacher)
    # TODO: Increment the next_teacher_id counter.
    next_teacher_id += 1
    print(f"Core: Teacher '{name}' added successfully.")

def list_students():
    """Prints all students in the database."""
    print("\n--- Student List ---")
    if not student_db:
        print("No students in the system.")
        return
    # TODO: Loop through student_db. For each student, print their ID, name, and their enrolled_in list.
    for student in student_db:
        print(f"  ID: {student.id}, Name: {student.name}, Enrolled in: {student.enrolled_in}")

def list_teachers():
    """Prints all teachers in the database."""
    # TODO: Implement the logic to list all teachers, similar to list_students().
    print("\n--- Teacher List ---")
    for teacher in teacher_db:
        print(f"  ID: {teacher.id}, Name: {teacher.name}, Speciality: {teacher.speciality}")

def find_students(term):
    """Finds students by name."""
    print(f"\n--- Finding Students matching '{term}' ---")
    # TODO: Create an empty list to store results.
    student_lst = []
    # Loop through student_db. If the search 'term' (case-insensitive) is in the student's name,
    for student in student_db:
        if student.name.casefold() == term.casefold(): 
    # add them to your results list.
            student_lst.append(student)
    # After the loop, if the results list is empty, print "No match found."
    if not student_lst:
        print("No match found.")
    # Otherwise, print the details for each student in the results list.
    else:
        for student in student_lst:
            print("\n--- Found Student List ---")
            print(f"  ID: {student.id}, Name: {student.name}, Enrolled in: {student.enrolled_in}")

def find_teachers(term):
    """Finds teachers by name or speciality."""
    print(f"\n--- Finding Teachers matching '{term}' ---")
    # TODO: Implement this function similar to find_students, but check
    teacher_lst = []
    # for the term in BOTH the teacher's name AND their speciality.
    for teacher in teacher_db:
        if teacher.name.casefold() == term.casefold():  # for the term in teacher's name
            teacher_lst.append(teacher)
        elif teacher.speciality.casefold() == term.casefold():  # for the term in teacher's speciality
            teacher_lst.append(teacher)
    # After loop, no result found
    if not teacher_lst:
        print("No match found.")
    # Otherwise, print the details for each teacher from the result list
    else:
        for teacher in teacher_lst:
            print("\n--- Found Teacher List ---")
            print(f"  ID: {teacher.id}, Name: {teacher.name}, Speciality: {teacher.speciality}")
        
    