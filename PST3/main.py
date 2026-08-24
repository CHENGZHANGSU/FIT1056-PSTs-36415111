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
        print(f"Lessons {course['id']} {course['name']} for {course['instrument']}")
        for lesson in course['lessons']:
            if lesson['day'].casefold() == day.casefold():
                course_exist = True
                print(f"Lesson id {lesson['id']} on {day}, start at {lesson['start_time']} in {lesson['room']}")
        if not course_exist:
            print(f"No lesson for {course['name']} on {day}\n")



def switch_course(manager, student_id, from_course_id, to_course_id):
    # TODO: Implement the logic to switch a student by calling methods on the manager.
    print(f"\n--- Switch Course for {student_id} ---")
    # find the student first
    student = manager.find_student_by_id(student_id)
    if student == None or from_course_id not in student.get_enrolled_course_ids():
        print(f"Student {student_id} not found, please check and try again later.")
    else:
        from_course = manager.find_course_by_id(from_course_id)
        to_course = manager.find_course_by_id(to_course_id)
        if from_course == None:
            print(f"Original Course {from_course_id} not found, please check and try again later.")
        elif to_course == None:
            print(f"Targeted Course {to_course_id} not found, please check and try again later.")
        else:
            for i, course_id in enumerate(student.get_enrolled_course_ids()):
               if  int(course_id) == int(from_course_id):
                   student.get_enrolled_course_ids()[i] = int(to_course_id)
                   print(f"Course switch successfully from {from_course_id} to {to_course_id}.\n")
                   break

def main():
    """Main function to run the MSMS application."""
    manager = ScheduleManager() # Create ONE instance of the application brain.
    
    while True:
        print("\n===== MSMS v3 (Object-Oriented) =====")
        # TODO: Create a menu for the new PST3 functions.
        print("1. View Daily Roster")
        # Get user input and call the appropriate view function, passing 'manager' to it.
        choice = input("Enter choice: ")
        if choice == '1':
            day = input("Enter day (e.g., Monday): ")
            front_desk_daily_roster(manager, day)
        elif choice.lower() == 'q':
            break
        
if __name__ == "__main__":
    main()