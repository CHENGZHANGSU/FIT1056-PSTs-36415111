# gui/main_dashboard.py
import streamlit as st
import time

from app.schedule import ScheduleManager
from gui.student_pages import find_student_page, add_student_page, update_student_page, remove_student_page, list_students_page, print_student_card
from gui.roster_pages import create_course_page, roster_page, check_in_page, enrollment_page, create_lesson_page, update_course_page, update_lesson_page, remove_lesson_page

def payment_page():
    st.header("Payments")
    st.warning("This feature will be implemented in PST5.")

def launch():
    """Sets up the main Streamlit application window and navigation."""
    st.set_page_config(layout = "wide", page_title = "Music School Management System")

    # Instantiate the "brain" of our app ONCE and store it in the session state.
    # This is crucial so the manager object persists as we switch pages.
    if 'manager' not in st.session_state:
        st.session_state.manager = ScheduleManager()

    st.sidebar.title("MSMS Navigation")
    # Create a radio button menu in the sidebar for page navigation.
    # page = st.sidebar.radio("Go to", ["Student Management", "Daily Roster", "Payments (stub)"])

    # Use an if/elif block to call the correct function to render the selected page.
    # if page == "Student Management":
    time.sleep(0.5)
    pages = {
        "MSMS Navigation":[],
        "Student Management":[
            st.Page(find_student_page, title = "Find Student", icon="🔎"),
            st.Page(print_student_card, title = "Print Student Card", icon="🖨️"),
            st.Page(add_student_page, title = "Register New Student", icon="📃"),
            st.Page(update_student_page, title = "Update Existing Students", icon="✏️"),
            st.Page(remove_student_page, title = "Remove Existing Student", icon="🗑️"),
            st.Page(list_students_page, title = "List of Students", icon="📋")
        ],
        "Course Management":[
            st.Page(roster_page, title = "Daily Roster", icon="🗓️"),
            st.Page(check_in_page, title = "Check-In Student", icon="🔥"),
            st.Page(enrollment_page, title = "Student Enrollment", icon="👉"),
            st.Page(create_course_page, title = "Create New Course", icon="🆕"),
            st.Page(update_course_page, title = "Update Course", icon="✨"),
            st.Page(remove_lesson_page, title = "Remove Course", icon="🗑️"),
            st.Page(create_lesson_page, title = "Create New Lesson", icon="🆕"),
            st.Page(update_lesson_page, title = "Update Lesson", icon="✨")

        ],
        "Payments (stub)":[
            st.Page(payment_page, title = "Payments (stub)", icon="💳")
        ]
    }
    pg = st.navigation(pages)
    pg.run()
        # match student_management_page:
        #     case "Find a Student":
        #         time.sleep(0.5)
        #         show_find_student_page(st.session_state.manager)
        #         # show_student_management_page(st.session_state.manager)
        #     case "Register New Student":
        #         time.sleep(0.5)
        #         show_add_student_page(st.session_state.manager)
        #     case "Update Existing Students":
        #         time.sleep(0.5)
        #         show_update_student_page(st.session_state.manager)
        #     case "Remove Existing Student":
        #         time.sleep(0.5)
        #         show_remove_student_page(st.session_state.manager)
        #     case "List of Students":
        #         time.sleep(0.5)
        #         show_student_management_page(st.session_state.manager)
        #     case _:
        #         raise UnboundLocalError(f"Unknown elements found in {page} switching.\n")
    # elif page == "Daily Roster":
        # course_management_page = st.sidebar.radio("Daily Roster", ["Daily Roster", "Check-In Student", 
        #                                                     "Student Enrollment"])
        # match course_management_page:
        #     case "Daily Roster":
        #         time.sleep(0.5)
        #         show_roster_page(st.session_state.manager)
        #     case "Check-In Student":
        #         time.sleep(0.5)
        #         show_check_in_page(st.session_state.manager)
        #     case "Student Enrollment":
        #         show_enrollment_page(st.session_state.manager)
    # elif page == "Payments (stub)":

