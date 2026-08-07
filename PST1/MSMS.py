# MSMS.py - The In-Memory Prototype
import pandas as pd

# --- Data Models ---
class Student:
    """A blueprint for student objects. Holds their info."""
    def __init__(self, student_id, name):
        self.id = student_id
        self.name = name
        # TODO: Initialize an empty list called 'enrolled_in' to store instrument names.
        self.enrolled_in = []

    def __str__(self) -> str:
        return f"{self.id}, {self.name}, {self.enrolled_in}"

    
class Teacher:
    """A blueprint for teacher objects."""
    def __init__(self, teacher_id, name, speciality):
        # TODO: Assign all three parameters (teacher_id, name, speciality)
        # to instance variables (e.g., self.id = teacher_id).
        self.id = teacher_id
        self.name = name
        self.speciality = speciality

    def __str__(self) -> str:
        return f"{self.id}, {self.name}, {self.speciality}"

# --- In-Memory Databases ---
# TODO: Create the global data stores.
student_db = []
teacher_db = []
next_student_id = 1
next_teacher_id = 1

# --- binary search through the list ---
def binary_search(lst, target):
    """Performs a binary search on a sorted list of students or teachers."""
    left, right = 0, len(lst) - 1
    while left <= right:
        mid = (left + right) // 2
        if lst[mid].id == target:
            return mid
        elif lst[mid].id < target:
            left = mid + 1
        else:
            right = mid - 1
    return None

# --- merge sort through the list ---
def merge(lst1, lst2):
    """
    Sub-function to sort two lists into one. 
    """
    new_lst = []

    i, j = 0, 0
    while i < len(lst1) and j < len(lst2):
        if lst1[i].id > lst2[j].id :                            # ascending order
            new_lst.append(lst2[j])
            j += 1
        else:
            new_lst.append(lst1[i])
            i += 1

    if i < len(lst1):                                           # any remaining elements in list1 or list2.
        new_lst += lst1[i:]
    elif j < len(lst2):
        new_lst += lst2[j:]

    return new_lst 

def merge_sort(lst):
    """
    Helper function to recursively separate list for further sorting.
    :complexity
        Best-case = Worst-case = O(nlogn)
        :n is the number of elements inside the list.
    """
    if len(lst) > 1:
        mid = len(lst) // 2

        # divide the list into left and right part
        lst1 = merge_sort(lst[mid:])
        lst2 = merge_sort(lst[:mid])

        return merge(lst1, lst2)
    elif len(lst) == 1:
        return lst
    else:
        print("There's nothing in the list. ")
        return lst

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
    if not teacher_db:
        print("No teachers in the system.")
        return
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
        return None
    # Otherwise, print the details for each student in the results list.
    else:
        print("\n--- Found Student List ---")
        for student in student_lst:
            print(f"  ID: {student.id}, Name: {student.name}, Enrolled in: {student.enrolled_in}")
        return student_lst

def find_teachers(term):
    """Finds teachers by name or speciality."""
    print(f"\n--- Finding Teachers matching '{term}' ---")
    # TODO: Implement this function similar to find_students, but check
    teacher_lst = []
    # for the term in BOTH the teacher's name AND their speciality.
    for teacher in teacher_db:
        if teacher.name.casefold() == term.casefold():          # for the term in teacher's name
            teacher_lst.append(teacher)
        elif teacher.speciality.casefold() == term.casefold():  # for the term in teacher's speciality
            teacher_lst.append(teacher)
    # After loop, no result found
    if not teacher_lst:
        print("No match found.")
    # Otherwise, print the details for each teacher from the result list
    else:
        print("\n--- Found Teacher List ---")
        for teacher in teacher_lst:
            print(f"  ID: {teacher.id}, Name: {teacher.name}, Speciality: {teacher.speciality}")
        return teacher_lst
        

# --- Front Desk Functions ---
def find_student_by_id(student_id):
    """A new helper to find one student by their exact ID."""
    # TODO: Loop through student_db. If a student's ID matches student_id, return the student object.
    for student in student_db:
        if student.id == student_id:
            return student
    # TODO: If the loop finishes without finding a match, return None.
    return None

def front_desk_register(name, instrument):
    """High-level function to register a new student and enrol them."""
    global next_student_id
    # TODO: Create a new Student object, add it to student_db, and increment the ID.
    new_student = Student(next_student_id, name)
    student_db.append(new_student)
    next_student_id += 1
    
    # TODO: Immediately call front_desk_enrol() using the new student's ID and the provided instrument.
    front_desk_enrol(new_student.id, instrument)
    print(f"Front Desk: Successfully registered '{name}' and enrolled them in '{instrument}'.")

def front_desk_enrol(student_id, instrument):
    """High-level function to enrol an existing student in a course."""
    # TODO: Use your new find_student_by_id() helper.
    student = find_student_by_id(student_id)
    # TODO: If the student is found, append the instrument to their 'enrolled_in' list.
    if student:
        student.enrolled_in.append(instrument)
        print(f"Front Desk: Enrolled student {student_id} in '{instrument}'.")
    else:
        # TODO: If the student is not found, print an error message like "Error: Student ID not found."
        print(f"Error: Student ID {student_id} not found.")

def find_id(name: str):
    """
    Helper function to find id via name.
    :complexity
        Best-case = Worst-case = O(n),
        :n is the number of students or teachers.
    """
    choice = input("student or teacher? (s/t): ")
    choice = choice[0].lower()
    match choice:
        case "s":
            return [find_students(name), "s"]
        case "t":
            return [find_teachers(name), "t"]
    return [None, None]

def repeat_element():
    """
    Helper function used to deal with when teachers or students share same name. 
    """
    res = input("Choose your id (q for not found): ")
    return res

def remove_data(term):
    """
    High-level function to remove a student or teacher from the database
    :complexity
        Best-case = Worst-case = O(nlogn),
        :n is the length of the database or list.
    Merge sort will have average complexity O(nlogn), while binary search with best case O(1),
    and worst case O(logn), and final list remove function is O(n).
    """
    result = find_id(term)                                      # find the id from name
    if result[0] == None:                                       # if no match found
        print("No match found.") 
        return False
    try:
        id = int(repeat_element())                              # dealing with repeat names
    except ValueError:                                          # if id not found
        print("No match found.")
        return False
    choice = result[1]
    tempo_lst = []
    match choice:
        case "s":
            tempo_lst = merge_sort(student_db)                  # sort the database through id 
        case "t":
            tempo_lst = merge_sort(teacher_db)                  
    index = binary_search(tempo_lst, id)                        # find the targeted index
    if index != None:
        match choice:                                           # remove element according to database
            case "s":
                student_db.remove(student_db[index])    
                print(f"Student '{term}' has been removed successfully.")
            case "t":
                teacher_db.remove(teacher_db[index])
                print(f"Teacher '{term}' has been removed successfully.")
    else:
        print("No match found.") 
        return False

        
def front_desk_lookup(term):
    """High-level function to search everything."""
    print(f"\n--- Performing lookup for '{term}' ---")
    find_students(term)
    find_teachers(term)

# --- Transform database into csv file ---
def database_to_csv(term: str) -> bool:
    """
    High-level function to transform the database into csv file.
    """
    match term:
        case "s":                                               # choose as student 
            data = [vars(student) for student in student_db]
            if data:
                df = pd.DataFrame(data=data)
                df.to_csv("Student List.csv", index = True, encoding = "utf-8")
                print("Student List has already generated successfully.")
                return True
            else:
                print("There's currently nothing in the student database.")
                return False
        case "t":                                               # choose as teacher
            data = [vars(teacher) for teacher in teacher_db]
            if data:
                df = pd.DataFrame(data=data)
                df.to_csv("Teacher List.csv", index = True, encoding = "utf-8")
                print("Teacher List has already generated successfully.")
                return True
            else:
                print("There's currently nothing in the teacher database.")
                return False
    return False

def database_csv_navigator(term: str):
    """
    Helper function of input validation before enter list to .csv transformation 
    """
    user_input = term
    while True:
        if user_input.lower() == "s" or user_input.lower() == "t":
            if not database_to_csv(user_input.lower()):
                print("There is some hidden issue, please check the database and try again.")
            break
        elif user_input.lower() == "q":
            print("Exiting CSV generation.")
            break
        else:
            user_input = input("Please enter (s/t) for student or teacher (q for quit): ")
    


# --- Main Application ---
def main():
    """Runs the main interactive menu for the receptionist."""
    # Pre-populate some data for easy testing
    add_teacher("Dr.Keys", "Piano")
    add_teacher("Ms.Fret", "Guitar")

    while True:
        print("\n===== Music School Front Desk =====")
        print("1. Register New Student")
        print("2. Enrol Existing Student")
        print("3. Lookup Student or Teacher")
        print("4. (Admin) List all Students")
        print("5. (Admin) List all Teachers")
        print("6. (Admin) Remove staff / student")
        print("p. (Admin) Print database to .csv")
        print("q. Quit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            # TODO: Prompt for student name and instrument, then call front_desk_register.
            name = input("Enter student name: ")
            instrument = input("Enter instrument to enrol in: ")
            front_desk_register(name, instrument)
        elif choice == '2':
            # TODO: Prompt for student ID (as an int) and instrument, then call front_desk_enrol.
            try:
                student_id = int(input("Enter student ID: "))
                instrument = input("Enter instrument to enrol in: ")
                front_desk_enrol(student_id, instrument)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == '3':
            # TODO: Prompt for a search term, then call front_desk_lookup.
            term = input("Enter search term: ")
            front_desk_lookup(term)
        elif choice == '4':
            list_students()
        elif choice == '5':
            list_teachers()
        elif choice == '6':
            remove_data(input("Enter the name: "))
        elif choice == 'p':
            database_csv_navigator(input("Please enter (s/t) for student or teacher (q for quit): "))
        elif choice.lower() == 'q':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# --- Program Start ---
if __name__ == "__main__":
    main()

    
