# pst2_main.py - The Persistent Application

import json
import datetime
import pandas as pd

DATA_FILE = "msms.json"
app_data = {} # This global dictionary will hold ALL our data.

# --- Core Persistence Engine ---
def load_data(path=DATA_FILE):
    """Loads all application data from a JSON file."""
    global app_data
    try:
        with open(path, 'r') as f:
            # TODO: Use json.load(f) to load the file's content into the global 'app_data' variable.
            app_data = json.load(f)
            print("Data loaded successfully.")
    except FileNotFoundError:
        print("Data file not found. Initializing with default structure.")
        # TODO: If the file doesn't exist, initialize 'app_data' with a default dictionary.
        # It should have keys like: "students", "teachers", "attendance", "next_student_id", "next_teacher_id".
        # The lists should be empty and the IDs should start at 1.
        app_data = {
            "students": [],
            "teachers": [],
            "attendance": [],
            "next_student_id": 1,
            "next_teacher_id": 1
        }

def save_data(path=DATA_FILE):
    """Saves all application data to a JSON file."""
    # TODO: Open the file at 'path' in write mode ('w').
    # Use json.dump() to write the global 'app_data' dictionary to the file.
    # Use the 'indent=4' argument in json.dump() to make the file readable.
    with open(path, 'w') as f:
        json.dump(app_data, f, indent=4)
    print("Data saved successfully.")

def print_all():
    print(app_data)


# --- Full CRUD for Core Data ---
# Note: We are now working with lists of dictionaries, not lists of objects.

# --- Front Desk Functions ---
def find_student_by_id(student_id):
    """A new helper to find one student by their exact ID."""
    # TODO: Loop through student_db. If a student's ID matches student_id, return the student object.
    for student in app_data['students']:
        if student['id'] == student_id:
            return student
    # TODO: If the loop finishes without finding a match, return None.
    return None

def front_desk_register(name, instrument):
    """High-level function to register a new student and enrol them."""
    student_id = app_data['next_student_id']
    # TODO: Create a new Student object, add it to student_db, and increment the ID.
    new_student = {'id': student_id, 'name': name, 'enrolled_in' : []}
    app_data['students'].append(new_student)
    app_data['next_student_id'] += 1
    
    # TODO: Immediately call front_desk_enrol() using the new student's ID and the provided instrument.
    front_desk_enrol(new_student['id'], instrument)
    print(f"Front Desk: Successfully registered '{name}' and enrolled them in '{instrument}'.")

def front_desk_enrol(student_id, instrument):
    """High-level function to enrol an existing student in a course."""
    # TODO: Use your new find_student_by_id() helper.
    student = find_student_by_id(student_id)
    # TODO: If the student is found, append the instrument to their 'enrolled_in' list.
    if student:
        student['enrolled_in'].append(instrument)
        print(f"Front Desk: Enrolled student {student_id} in '{instrument}'.")
    else:
        # TODO: If the student is not found, print an error message like "Error: Student ID not found."
        print(f"Error: Student ID {student_id} not found.")

def add_teacher(name, speciality):
    """Adds a teacher dictionary to the data store."""
    # TODO: Get the next teacher ID from app_data['next_teacher_id'].
    teacher_id = app_data['next_teacher_id']
    # TODO: Create a new teacher dictionary with 'id', 'name', and 'speciality' keys.
    new_teacher = {"id": teacher_id, "name": name, "speciality": speciality}
    # TODO: Append the new dictionary to the app_data['teachers'] list.
    app_data['teachers'].append(new_teacher)
    # TODO: Increment the 'next_teacher_id' in app_data.
    app_data['next_teacher_id'] += 1
    print(f"Core: Teacher '{name}' added.")

def update_teacher(teacher_id, **fields):
    """Finds a teacher by ID and updates their data with provided fields."""
    # TODO: Loop through the app_data['teachers'] list.
    for teacher in app_data['teachers']:
        # TODO: If a teacher's 'id' matches teacher_id:
        if teacher['id'] == teacher_id:
            # Use the .update() method on the teacher dictionary to apply the 'fields'.
            teacher.update(fields)
            print(f"Teacher {teacher_id} updated.")
            return
    print(f"Error: Teacher with ID {teacher_id} not found.")

def remove_student(student_id : int):
    """
    Removes a student from the data store.
    """
    # TODO: Find the student dictionary in app_data['students'] with the matching ID.
    for student in app_data['students']:
    # If found, use the .remove() method on the list to delete it.
        if student['id'] == student_id:
            print(f"Student {student['name']} is removed. ")
            app_data['students'].remove(student)
            return
    print("Remove failed.")
    # A list comprehension is a clean way to do this:
    # app_data['students'] = [s for s in app_data['students'] if s['id'] != student_id]
    
# TODO: Implement remove_teacher() and update_student() using the patterns above.
def remove_teacher(teacher_id : int):
    """
    Removes a student from the data store.
    """
    for teacher in app_data['teachers']:
        if teacher['id'] == teacher_id:
            print(f"Teacher {teacher['name']} is removed. ")
            app_data['teachers'].remove(teacher)
            return
    print("Remove failed. ")

def update_student(student_id, **fields):
    """
    Finds a student by ID and updates their data with provided fields.
    """
    for student in app_data['students']:
        if student['id'] == student_id:
            student.update(fields)
            print(f"Student {student_id} updated.")
            return
    print(f"Error: Teacher with ID {student_id} not found.")
    

# --- New Receptionist Features ---
def check_in(student_id, course_id, timestamp=None):
    """Records a student's attendance for a course."""
    if timestamp is None:
        # TODO: Get the current time as a string using datetime.datetime.now().isoformat()
        timestamp = datetime.datetime.now().isoformat()
    
    # TODO: Create a check-in record dictionary.
    # It should contain 'student_id', 'course_id', and 'timestamp'.
    check_in_record = {
        "student_id": student_id,
        "course_id": course_id,
        "timestamp": timestamp
    }
    # TODO: Append this new record to the app_data['attendance'] list.
    app_data['attendance'].append(check_in_record)
    print(f"Receptionist: Student {student_id} checked into {course_id}.")

def print_student_card(student_id):
    """Creates a text file badge for a student."""
    # TODO: Find the student dictionary in app_data['students'].
    student_to_print = None
    for s in app_data['students']:
        if s['id'] == student_id:
            student_to_print = s
            break
    
    if student_to_print:
        # TODO: Create a filename, e.g., f"{student_id}_card.txt".
        filename = f"{student_id}_card.txt"
        # TODO: Open the file in write mode ('w').
        with open(filename, 'w') as f:
            # Write the student's details to the file in a nice format.
            f.write("========================\n")
            f.write(f"  MUSIC SCHOOL ID BADGE\n")
            f.write("========================\n")
            f.write(f"ID: {student_to_print['id']}\n")
            f.write(f"Name: {student_to_print['name']}\n")
            f.write(f"Enrolled In: {', '.join(student_to_print.get('enrolled_in', []))}\n")
        print(f"Printed student card to {filename}.")
    else:
        print(f"Error: Could not print card, student {student_id} not found.")

# --- Transform database into csv file ---
def database_to_csv() -> bool:
    """
    High-level function to transform the database into csv file.
    """
    target_key = ['students', 'teachers', 'attendance']
    output = {}
    for key in target_key:
        output += app_data[key]

    df = pd.DataFrame(data=output)
    try:
        df.to_csv("Database Overview.csv", index = True, encoding = 'utf-8')
        return True
    except:
        return False

def database_csv_navigator():
    """
    Helper function of input validation before enter list to .csv transformation 
    """
    # Determine whether the .csv file is generated successfully. 
    if database_to_csv():
        print("Database is successfully transformed into .csv file. ")
    else:
        print("Errors generated, please review the format of the database and try again. ")

# --- Main Application Loop ---
def main():
    """Main function to run the MSMS application."""
    load_data() # Load all data from file at startup.

    while True:
        print("\n===== MSMS v2 (Persistent) =====")
        print("0. Check")
        print("1. Add Student")
        print("2. Check-in Student")
        print("3. Print Student Card")
        print("4. Update Teacher Info")
        print("5. Remove Student")
        print("6. Remove Teacher")
        print("p. Print database to .csv")
        print("q. Quit and Save")
        
        choice = input("Enter your choice: ")
        
        made_change = False # A flag to track if we need to save
        if choice == '0':
            print_all()
        elif choice == '1':
            # TODO: Prompt for student name and instrument, then call front_desk_register.
            name = input("Enter student name: ")
            instrument = input("Enter instrument to enrol in: ")
            front_desk_register(name, instrument)
            made_change = True
        elif choice == '2':
            # TODO: Get student_id and course_id from user, then call check_in().
            student_id = int(input("Please enter your student id: "))
            course_id = input("Please enter your course_id: ")
            check_in(student_id, course_id)
        elif choice == '3':
            # TODO: Get student_id, then call print_student_card().
            student_id = int(input("Please enter your student id: "))
            print_student_card(student_id)
            pass # No change made, so no save needed
        elif choice == '4':
            # TODO: Get teacher_id and new details, then call update_teacher().
            teacher_id = int(input("Please enter your teacher id: "))
            speciality = input("Please enter your speciality")
            # Example: update_teacher(1, speciality="Advanced Piano")
            update_student(teacher_id, speciality = speciality)
            made_change = True
        elif choice == '5':
            # TODO: Get student_id, then call remove_student().
            student_id = int(input("Please enter your student id: "))
            remove_student(student_id)
            made_change = True
        elif choice == '6':
            # TODO: Get teacher_id, then call remove_teacher().
            teacher_id = int(input("Please enter your teacher id: "))
            remove_teacher(teacher_id)
            made_change = True
        elif choice == 'p':
            database_csv_navigator()
        elif choice.lower() == 'q':
            print("Saving final changes and exiting.")
            break
        else:
            print("Invalid choice.")
            
        if made_change:
            save_data() # Save the data immediately after any change.

    save_data() # One final save on exit.

# --- Program Start ---
if __name__ == "__main__":
    main()
