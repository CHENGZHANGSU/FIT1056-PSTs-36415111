# main.py - The View Layer
from app.schedule import ScheduleManager


def front_desk_daily_roster(manager, day="all"):
    """Displays a pretty table of all lessons on a given day."""
    print(f"\n--- Daily Roster for {day} ---")
    # Notice: This code does not need to change. It doesn't care where the Course class lives.
    # It only talks to the manager.
    # TODO: Call a method on the manager to get the day's lessons and print them.
    for course in manager.get_course_list():
        course_exist = False
        print("\n##################################################################")
        print(f"Lessons {course.get_course_id()} {course.get_course_name()} for {course.get_course_instrument()}")
        for lesson in course.get_lessons():
            if (day != "all") and (lesson['day'].casefold() == day.casefold()):
                course_exist = True
                print(f"Lesson id {lesson['lesson_id']} on {day}, start at {lesson['start_time']} in {lesson['room']}")
            elif day == "all":
                course_exist = True
                print(f"Lesson id {lesson['lesson_id']} on {lesson['day']}, start at {lesson['start_time']} in {lesson['room']}")
        if not course_exist and day == "all":
            print(f"No lesson for {course.get_course_name()}\n")
        elif not course_exist:
            print(f"No lesson for {course.get_course_name()} on {day}\n")


def list_user_navigator(manager, order, type="s"):
    """Display students / teachers / attendance / courses information"""
    print("\n----- Accessing to the database -----")
    match type.lower() or type[0].lower():
        case "s":
            manager.list_students(order)
        case "t":
            manager.list_teachers(order)
        case "a":
            manager.list_attendance()
        case "c":
            front_desk_daily_roster(manager)
        case _:
            print("Invalid Syntax.\n")

def add_user_navigator(manager, type="s"):
    """Add a new user to the system"""
    print("\n----- Adding user to the database -----")
    match type.lower() or type[0].lower():
        case "s":
            name = input("Enter the student's name: ")
            course_id = int(input("Enter the course ID to enrol the student in: "))
            manager.front_desk_register(name, course_id)
        case "t":
            name = input("Enter the teacher's name: ")
            speciality = input("Enter the teacher's speciality: ")
            manager.add_teacher(name, speciality)
        case _:
            print("Invalid Syntax.\n")

def update_user_navigator(manager, type = "s"):
    """Update an existing user from the system"""
    print("\n----- Updating user to the database -----")
    simple_reminder = "#: If you don't want to update the respective categories or information, feel free to leave it blank and press 'enter.'\n"
    print(simple_reminder)
    user_id = int(input("Enter your user id: "))
    
    match type.lower() or type[0].lower():
        case "s":
            name = input("Enter your new name: ")
            course_id = input("Enter the course ID to enrol the student in (split with , for more than one): ")
            manager.update_user(type, user_id, name = name, course_id = course_id)
        case "t":
            name = input("Enter your new name: ")
            speciality = input("Enter your new speciality: ")
            manager.update_user(type, user_id, name = name, speciality = speciality)
        case _:
            print("Invalid Syntax.\n")

def remove_user_navigator(manager, type):
    """Remove an existing user from the system"""
    print("\n----- Removing user from the database -----")
    match type.lower() or type[0].lower():
        case "s":
            student_id = int(input("Enter the student id: "))
            manager.remove_user(student_id, "s")
        case "t":
            teacher_id = int(input("Enter the teacher id: "))
            manager.remove_user(teacher_id, "t")
        case _:
            print("Invalid Syntax.\n")

def _require_course_info(type = "add") -> tuple:
    """Helper function to collect course related information"""
    simple_reminder = "#: If you don't want to update the respective categories or information, feel free to leave it blank and press 'enter.'\n"
    match type:
        case "add":                
            print(simple_reminder)
            course_name = input("Enter the course name: ")
            instrument = input("Enter the name of the instrument: ")
            teacher_id = int(input("Enter the enrolled teacher id: "))
            return (course_name, instrument, teacher_id)
        case "update":
            course_id = int(input("Enter the course id need updates: "))
            course_name = input("Enter the new course name: ")
            instrument = input("Enter the name of the instrument: ")
            teacher_id = int(input("Enter the new enrolled teacher id: "))
            return (course_id, course_name, instrument, teacher_id)
        case _:
            print("Invalid Syntax in collecting course / lesson related information.\n")
            return ()

def add_course_lessons_navigator(manager, type = "c"):
    """Add a new course or lesson to the system"""
    match type[0].lower():
        case "c":
            print("\n----- Adding a new course to the database -----")
            info = _require_course_info()
            manager.add_course(course_name = info[0], instrument = info[1], teacher_id = info[2])
        case "l":
            manager.add_lessons()
        case _:
            print("Invalid Syntax in add courses and lessons.\n")
            return None

def update_course_lessons_navigator(manager, type="c"):
    """Update an existing course or lesson from the system"""
    front_desk_daily_roster(manager)
    print("\n")
    match type[0].lower():
        case "c":
            info = _require_course_info("update")
            manager.update_course(info[0], course_name = info[1], instrument = info[2], teacher_id = info[3])
        case "l":
            manager.update_lesson()
        case _:
            print("Invalid Syntax in update courses and lessons.\n")
            return None
        
def remove_course_lessons_navigator(manager, type="c"):
    """Remove an existing course or lesson from the system"""
    front_desk_daily_roster(manager)
    print("\n")
    match type[0].lower():
        case "c":
            manager.remove_course()
        case "l":
            manager.remove_lessons()
        case _:
            print("Invalid Syntax in remove courses and lessons.\n")
            return None
    
def enrollment_navigator(manager):
    print("\n----- Enrolling events to users -----")
    print("1. Enroll new course as a student")
    print("2. Enroll new teacher in the course")
    choice = int(input("Please enter your choice: "))
    match choice:
        case 1:
            manager.front_desk_enrol(int(input("Please enter your student id: ")), int(input("Please enter the course id: ")), "s")
        case 2:
            manager.front_desk_enrol(int(input("Please enter your teacher id: ")), int(input("Please enter the course id: ")), "t")
            pass
        case _:
            print("Invalid Syntax.")
            return 

def print_student_card_navigator(manager):
    print("\n----- Printing student card -----")
    student_id = int(input("Enter the student id: "))
    manager.print_student_card(student_id)

def _type_title(action:str, p1:str, p2:str, abbrev:str) -> str:
    arg = f"{action} a {p1} or a {p2}? ({abbrev}): "
    type = input(arg)
    return type

def main():
    """Main function to run the MSMS application."""
    manager = ScheduleManager() # Create ONE instance of the application brain.
    
    while True:
        manager.sync_courses_students()     # Synchronize courses and students consistently.
        print("\n===== MSMS v3 (Object-Oriented) =====")
        # TODO: Create a menu for the new PST3 functions.
        print("1. View Daily Roster")
        print("2. List User / Attendance / Course")
        print("3. Add User")
        print("4. Enrollment")
        print("5. Update User")
        print("6. Remove User")
        print("7. Add Course")
        print("8. Update Courses & Lessons")
        print("9. Remove Courses & Lessons")
        print("10. Print student-card")
        print("p. Print to .csv")
        print("q. Save and Quit")
        # Get user input and call the appropriate view function, passing 'manager' to it.
        choice = input("Enter choice: ")
        if choice == '1':
            day = input("Enter day (e.g., Monday): ")
            front_desk_daily_roster(manager, day)

        elif choice == '2':
            type = input("List students, teachers, courses or attendance? (s/t/c/a): ")
            order = ""
            if type[0].lower() == "c" or type[0].lower() == "a":
                order = "a"
            else:
                order = input("View in ascending or descending method? (a/d): ")
            list_user_navigator(manager, order, type)

        elif choice == '3':
            type = _type_title("Add", "student", "teacher", "s/t")
            add_user_navigator(manager, type)

        elif choice == '4':
            enrollment_navigator(manager)

        elif choice == '5':
            type = _type_title("Update", "student", "teacher", "s/t")
            update_user_navigator(manager, type)

        elif choice == '6':
            type = _type_title("Remove", "student", "teacher", "s/t")
            remove_user_navigator(manager, type)

        elif choice == '7':
            type = _type_title("Add", "course", "lesson", "c/l")
            add_course_lessons_navigator(manager, type)

        elif choice == '8':
            type = _type_title("Update", "course", "lesson", "c/l")
            update_course_lessons_navigator(manager, type)

        elif choice == '9':
            type = _type_title("Remove", "course", "lesson", "c/l")
            remove_course_lessons_navigator(manager, type)

        elif choice == '10':
            print_student_card_navigator(manager)

        elif choice.lower() == 'p':
            pass

        elif choice.lower() == 'q':
            manager.save_all()
            print("\nSaving final changes and exiting.")
            break
        
        else:
            print("Invalid choice.")
        
if __name__ == "__main__":
    main()