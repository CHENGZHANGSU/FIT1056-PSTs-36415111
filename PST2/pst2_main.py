# pst2_main.py - The Persistent Application

import json
import datetime
import pandas as pd
from algorithm import *

DATA_FILE = "PST2/msms.json"
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
            "next_teacher_id": 1,
            "unused_id": {
                "ui_student": [],
                "ui_teacher": []
            }
        }

def save_data(path=DATA_FILE):
    """Saves all application data to a JSON file."""
    # TODO: Open the file at 'path' in write mode ('w').
    # Use json.dump() to write the global 'app_data' dictionary to the file.
    # Use the 'indent=4' argument in json.dump() to make the file readable.
    with open(path, 'w') as f:
        json.dump(app_data, f, indent=4)
    print("Data saved successfully.\n")

def list_students():
    """Prints all students in the database."""
    print("\n--- Student List ---")
    if not app_data['students']:
        print("No students in the system.")
        return
    # TODO: Loop through student_db. For each student, print their ID, name, and their enrolled_in list.
    for student in app_data['students']:
        print(f"  ID: {student['id']}, Name: {student['name']}, Enrolled in: {student['enrolled_in']}")

def list_teachers():
    """Prints all teachers in the database."""
    # TODO: Implement the logic to list all teachers, similar to list_students().
    print("\n--- Teacher List ---")
    if not app_data['teachers']:
        print("No teachers in the system.")
        return
    for teacher in app_data['teachers']:
        print(f"  ID: {teacher['id']}, Name: {teacher['name']}, Speciality: {teacher['speciality']}")

def list_navigator(choice : str):
    match (choice.lower()):
        case "s":
            list_students()
        case "t":
            list_teachers()
        case _:
            print("Unknown status")
            return None

def get_app_data():
    return app_data

def print_all():
    print(app_data)

def collect_unused_id(id: int, category: str):
    """
    Helper function to collect the removed id. 
    """
    match (category.casefold()):
        case "student":
            app_data['unused_id']['ui_student'].append(id)
        case "teacher":
            app_data['unused_id']['ui_teacher'].append(id)
        case _:
            print("Something wrong with id recycling.\n")

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
    if len(app_data['students']) == 0:
        print("Remove failed: There is nothing in student database.")
        return 
    # TODO: Find the student dictionary in app_data['students'] with the matching ID.
    for student in app_data['students']:
    # If found, use the .remove() method on the list to delete it.
        if student['id'] == student_id:
            collect_unused_id(student_id, "student")
            print(f"Student {student['name']} is removed. ")
            app_data['students'].remove(student)
            return
    print("Remove failed: Student not found.")
    # A list comprehension is a clean way to do this:
    # app_data['students'] = [s for s in app_data['students'] if s['id'] != student_id]
    
# TODO: Implement remove_teacher() and update_student() using the patterns above.
def remove_teacher(teacher_id : int):
    """
    Removes a student from the data store.
    """
    if len(app_data['teachers']) == 0:
        print("Remove failed: There is nothing in teacher database.")
        return 
    for teacher in app_data['teachers']:
        if teacher['id'] == teacher_id:
            collect_unused_id(teacher_id, "teacher")
            print(f"Teacher {teacher['name']} is removed. ")
            app_data['teachers'].remove(teacher)
            return
    print("Remove failed: Teacher not found")

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

def find_students(term):
    """Finds students by name."""
    print(f"\n--- Finding Students matching '{term}' ---")
    # TODO: Create an empty list to store results.
    student_lst = []
    # Loop through student_db. If the search 'term' (case-insensitive) is in the student's name,
    for student in app_data['students']:
        if student['name'].casefold() == term.casefold(): 
    # add them to your results list.
            student_lst.append(student)
    # After the loop, if the results list is empty, print "No match found."
    if not student_lst:
        print("No match found.")
        return False
    # Otherwise, print the details for each student in the results list.
    else:
        print("\n--- Found Student List ---")
        for student in student_lst:
            print(f"  ID: {student['id']}, Name: {student['name']}, Enrolled in: {student['enrolled_in']}")
        return True

def find_teachers(term):
    """Finds teachers by name or speciality."""
    print(f"\n--- Finding Teachers matching '{term}' ---")
    # TODO: Implement this function similar to find_students, but check
    teacher_lst = []
    # for the term in BOTH the teacher's name AND their speciality.
    for teacher in app_data['teachers']:
        if teacher['name'].casefold() == term.casefold():          # for the term in teacher's name
            teacher_lst.append(teacher)
        elif teacher['speciality'].casefold() == term.casefold():  # for the term in teacher's speciality
            teacher_lst.append(teacher)
    # After loop, no result found
    if not teacher_lst:
        print("No match found.")
        return False
    # Otherwise, print the details for each teacher from the result list
    else:
        print("\n--- Found Teacher List ---")
        for teacher in teacher_lst:
            print(f"  ID: {teacher['id']}, Name: {teacher['name']}, Speciality: {teacher['speciality']}")
        return True
    

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
        filename = f"PST2/{student_id}_card.txt"
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

def obey_order(order = "ascending"):
    """
    Sort the database of each list in dict according to user need. 
    """
    key = ['students', 'teachers', 'attendance']
    for k in key:
        if len(app_data[k]) != 0:
            if order.casefold() in "ascending":
                app_data[k] = merge_sort(app_data[k])
                print(f"{k.capitalize()} database is sorted in ascending order.\n")
            else:
                app_data[k] = merge_sort(app_data[k], "descending")
                print(f"{k.capitalize()} database is sorted in descending order.\n")

# --- Transform database into csv file ---
def database_to_csv() -> bool:
    """
    High-level function to transform the database into csv file.
    """
    obey_order(input("Which order the data should be arranged? (asc/des): "))
    choice = input("Which data should be transformed into .csv file? (s/t/a/all): ")

    target_key = ['students', 'teachers', 'attendance']
    match (choice.lower()):                                         # match various options
        case "s":
            df = pd.DataFrame(data = app_data['students'])
            try:
                if len(app_data['students']) != 0:
                    print("There is nothing inside student database")
                df.to_csv("PST2/Students.csv", index = True, encoding = 'utf-8')
                print("File generated.\n")
                return True
            except:
                print("Error, please check the database and try again.\n")
                return False  
        case "t":
                df = pd.DataFrame(data = app_data['teachers'])
                try:
                    if len(app_data['teachers']) != 0:
                        print("There is nothing inside teacher database")
                    df.to_csv("PST2/Teachers.csv", index = True, encoding = 'utf-8')
                    print("File generated.\n")
                    return True
                except:
                    print("Error, please check the database and try again.\n")
                    return False
        case "a":
                df = pd.DataFrame(data = app_data['attendance'])
                try:
                    if len(app_data['attendance']) != 0:
                        print("There is nothing inside attendance database")
                    df.to_csv("PST2/Attendance.csv", index = True, encoding = 'utf-8')
                    print("File generated.\n")
                    return True
                except:
                    print("Error, please check the database and try again.\n")
                    return False
        case "all":
                data = []
                for key in target_key:
                    for value in app_data[key]:
                        data.append(value)

                df = pd.DataFrame(data = data)
                try:
                    df.to_csv("PST2/Database Overview.csv", index = True, encoding = 'utf-8')
                    print("File generated.\n")
                    return True
                except:
                    print("Error, please check the database and try again.\n")
                    return False
        case _:
            print("Unknown status")
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
        print("2. Add Teacher")
        print("3. Check-in Student")
        print("4. Print Student Card")
        print("5. Update Teacher Info")
        print("6. Update Student Info")
        print("7. Remove Student")
        print("8. Remove Teacher")
        print("9. List Students/Teachers")
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
            # TODO: Prompt for student name and instrument, then call front_desk_register.
            name = input("Enter teacher name: ")
            speciality = input("Enter your speciality: ")
            add_teacher(name, speciality)
            made_change = True

        elif choice == '3':
            # TODO: Get student_id and course_id from user, then call check_in().
            student_id = int(input("Please enter your student id: "))
            course_id = input("Please enter your course_id: ")
            check_in(student_id, course_id)
            made_change = True

        elif choice == '4':
            # TODO: Get student_id, then call print_student_card().
            student_id = int(input("Please enter your student id: "))
            print_student_card(student_id)
            pass # No change made, so no save needed

        elif choice == '5':
            # TODO: Get teacher_id and new details, then call update_teacher().
            teacher_id = int(input("Please enter your teacher id: "))
            name = input("Please enter your name: ")
            speciality = input("Please enter your speciality: ")
            # Example: update_teacher(1, speciality="Advanced Piano")
            update_teacher(teacher_id, name = name, speciality = speciality)
            made_change = True

        elif choice == '6':
            # TODO: Get teacher_id and new details, then call update_teacher().
            student_id = int(input("Please enter your student id: "))
            name = input("Please enter your name: ")
            enrollment = input("Please enter your new enrollment: ")
            update_student(student_id, name = name, enrolled_in = [f"{enrollment}"])
            made_change = True

        elif choice == '7':
            # TODO: Get student_id, then call remove_student().
            student_id = int(input("Please enter your student id: "))
            remove_student(student_id)
            made_change = True

        elif choice == '8':
            # TODO: Get teacher_id, then call remove_teacher().
            teacher_id = int(input("Please enter your teacher id: "))
            remove_teacher(teacher_id)
            made_change = True

        elif choice == '9':
            list_navigator(input("List for students or teachers (s/t): "))

        elif choice == 'p':
            database_csv_navigator()

        elif choice.lower() == 'q':
            print("\nSaving final changes and exiting.")
            break

        else:
            print("Invalid choice.")
            
        if made_change:
            save_data() # Save the data immediately after any change.

    save_data() # One final save on exit.

# --- Program Start ---
if __name__ == "__main__":
    main()
