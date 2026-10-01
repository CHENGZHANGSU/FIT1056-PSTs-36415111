# gui/main_dashboard.py
import streamlit as st
from app.schedule import ScheduleManager
from gui.student_pages import show_student_management_page, show_add_student_page, show_find_student_page, show_update_student_page
from gui.roster_pages import show_roster_page

def launch():
    """Sets up the main Streamlit application window and navigation."""
    st.set_page_config(layout = "wide", page_title = "Music School Management System")

    # Instantiate the "brain" of our app ONCE and store it in the session state.
    # This is crucial so the manager object persists as we switch pages.
    if 'manager' not in st.session_state:
        st.session_state.manager = ScheduleManager()

    st.sidebar.title("MSMS Navigation")
    # Create a radio button menu in the sidebar for page navigation.
    page = st.sidebar.radio("Go to", ["Student Management", "Daily Roster", "Payments (stub)"])

    # Use an if/elif block to call the correct function to render the selected page.
    if page == "Student Management":
        student_management_page = st.sidebar.radio("Student Management", ["Find a Student", "Register New Student", 
                                                             "Update Existing Students", "Remove Existing Student",
                                                             "View List of Students"])
        match student_management_page:
            case "Find a Student":
                show_find_student_page(st.session_state.manager)
                show_student_management_page(st.session_state.manager)
            case "Register New Student":
                show_add_student_page(st.session_state.manager)
            case "Update Existing Students":
                show_update_student_page(st.session_state.manager)
            case "Remove Existing Student":
                pass
            case "View List of Students":
                show_student_management_page(st.session_state.manager)
            case _:
                raise UnboundLocalError(f"Unknown elements found in {page} switching.\n")
    elif page == "Daily Roster":
        show_roster_page(st.session_state.manager)
    elif page == "Payments (stub)":
        st.header("Payments")
        st.warning("This feature will be implemented in PST5.")