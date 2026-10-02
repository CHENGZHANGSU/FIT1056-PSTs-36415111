"""Streamlit entry point and top-level navigation for MSMS."""

import streamlit as st

from app.schedule import ScheduleManager
from gui.roster_pages import (
    check_in_page,
    create_course_page,
    create_lesson_page,
    enrollment_page,
    remove_lesson_page,
    roster_page,
    update_course_page,
    update_lesson_page,
)
from gui.student_pages import (
    add_student_page,
    find_student_page,
    list_students_page,
    print_student_card,
    remove_student_page,
    update_student_page,
)


def home_page() -> None:
    """Show a quick overview of the school's current records."""
    manager = st.session_state.manager

    st.title("Music School Management System")
    st.write(
        "Manage students, courses, lessons, and attendance from one place."
    )

    student_column, teacher_column, course_column = st.columns(3)
    student_column.metric("Students", len(manager.students))
    teacher_column.metric("Teachers", len(manager.teachers))
    course_column.metric("Courses", len(manager.courses))

    st.info("Choose a page from the navigation menu to get started.")
    st.caption("Stage 4: Streamlit user interface")


def payment_page() -> None:
    st.title("Payments")
    st.info("Payment management is planned for Stage 5.")


def launch() -> None:
    """Configure and run the multipage Streamlit application."""
    st.set_page_config(
        page_title="Music School Management System",
        page_icon="🎵",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "About": "MSMS Stage 4 — a Streamlit interface for music-school management."
        },
    )

    if "manager" not in st.session_state:
        st.session_state.manager = ScheduleManager()

    # Inject CSS to target the sidebar h1 title element
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] h1 {
            font-size: 20px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.title("Music School Management System")

    pages = {
        "Overview": [st.Page(home_page, title="Dashboard", icon=":material/dashboard:", default=True)],
        "Student Management": [
            st.Page(find_student_page, title="Find Student", icon="🔎"),
            st.Page(print_student_card, title="Print Student Card", icon="🖨️"),
            st.Page(add_student_page, title="Register Student", icon="📃"),
            st.Page(update_student_page, title="Update Student", icon="✏️"),
            st.Page(remove_student_page, title="Remove Student", icon="🗑️"),
            st.Page(list_students_page, title="Students", icon="📋"),
        ],
        "Course Management": [
            st.Page(roster_page, title="Daily Roster", icon="🗓️"),
            st.Page(check_in_page, title="Student Check-in", icon="🔥"),
            st.Page(enrollment_page, title="Student Enrollment", icon="👉"),
            st.Page(create_course_page, title="Create Course", icon="🆕"),
            st.Page(update_course_page, title="Update Course", icon="✨"),
            st.Page(remove_lesson_page, title="Remove Course", icon="🗑️"),
            st.Page(create_lesson_page, title="Create Lesson", icon="🆕"),
            st.Page(update_lesson_page, title="Update Lesson", icon="✨"),
        ],
        "Other": [
            st.Page(payment_page, title="Payments (coming soon)", icon="💳")
        ],
    }

    navigation = st.navigation(pages)
    navigation.run()
