# main.py - The View Layer
from app.schedule import ScheduleManager

def front_desk_daily_roster(manager, day):
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
            if lesson['day'].casefold() == day.casefold():
                course_exist = True
                print(f"Lesson id {lesson['lesson_id']} on {day}, start at {lesson['start_time']} in {lesson['room']}")
        if not course_exist:
            print(f"No lesson for {course.get_course_name()} on {day}\n")


def list_user_navigator(manager, type="s"):
    print("\n----- Accessing to the database -----")
    match type.lower() or type[0].lower():
        case "s":
            manager.list_students()
        case "t":
            manager.list_teachers()
        case "a":
            password = int(input("Enter the password to view attendance: "))
            if password == password:
                manager.list_attendance()
        case _:
            print("Invalid Syntax.\n")

def add_user_navigator(manager, type="s"):
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

def remove_user_navigator(manager, type):
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

def main():
    """Main function to run the MSMS application."""
    manager = ScheduleManager() # Create ONE instance of the application brain.
    
    while True:
        print("\n===== MSMS v3 (Object-Oriented) =====")
        # TODO: Create a menu for the new PST3 functions.
        print("1. View Daily Roster")
        print("2. List User")
        print("3. Add User")
        print("4. Enrollment")
        print("5. Update User")
        print("6. Remove User")
        print("7. Print student-card")
        print("p. Print to .csv")
        print("q. Save and Quit")
        # Get user input and call the appropriate view function, passing 'manager' to it.
        choice = input("Enter choice: ")
        if choice == '1':
            day = input("Enter day (e.g., Monday): ")
            front_desk_daily_roster(manager, day)

        elif choice == '2':
            res = input("Access student, teacher or attendance? (s/t/a): ")
            list_user_navigator(manager, res)

        elif choice == '3':
            res = input("Add student or teacher? (s/t): ")
            add_user_navigator(manager, res)

        elif choice == '4':
            enrollment_navigator(manager)

        elif choice == '5':
            pass

        elif choice == '6':
            type = input("Remove a student or teacher (s/t): ")
            remove_user_navigator(manager, type)

        elif choice == '7':
            pass

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