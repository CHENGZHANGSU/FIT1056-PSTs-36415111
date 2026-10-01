# gui/student_pages.py
import pandas as pd
import streamlit as st
from Exceptions.UserNotFound import UserNotFound

def show_add_student_page(manager):
    # --- Add Section ---#
    st.subheader("Register New Student")
    with st.form("registration_form"):
        reg_name = st.text_input("New Student Name")
        reg_instrument = st.text_input("First Instrument")
        reg_course = st.selectbox("Select Course", [c.name for c in manager.courses])
        reg_course_id = 0
        for c in manager.courses:
            if c.name == reg_course:
                reg_course_id = c.id
        submitted = st.form_submit_button("Register Student")
        
        if submitted:
            # This call now works because we implemented the method in PST3.
            # TODO: Add a check for blank name/instrument.
            if reg_name and reg_instrument:
                new_student = manager.front_desk_register(reg_name, reg_course_id, reg_instrument)
                if new_student:
                    st.success(f"Successfully registered {reg_name}!")
                    st.balloons()
                    # You can use st.balloons() for extra flair.
                else:
                    st.error(f"Could not register student. A teacher for {reg_instrument} might not be available.")
            else:
                st.warning("Please enter both a name and an instrument.")

def show_find_student_page(manager):
    # --- Search Section ---#
    st.subheader("Find Student")
    with st.form("Student information"):
        reg_student_id = st.text_input(label = "Student ID", key = "Enter your student id: ", type = "search")
        submitted = st.form_submit_button("Find Student")

        if submitted:
            if reg_student_id:
                student = manager.find_user_by_id(int(reg_student_id), "s")
                if student:
                    frame = pd.DataFrame([student.__dict__])
                    user_table(manager, "u", frame)
                    st.success(f"Successfully find {student.name}!")
                else:
                    st.error(f"Could not find this student.")
            else:
                st.warning("Please enter your student id.")

def show_update_student_page(manager):
    # --- Update Section ---#
    st.subheader("Update Student")
    with st.form("Student Updated Information"):
        reg_student_id = st.text_input(label = "Student ID", key = "Enter your student id: ")
        reg_student_name = st.text_input(label = "Student Name", key = "Enter your student name")
        reg_student_course_ids = st.text_input(label = "Course ID(s)", key = "Enter the course ID to enrol the student in (split with , for more than one): ")
        reg_student_instruments = st.text_input(label = "Instrument(s)", key = "Enter the instrument you play (split with , when more than 1): ")
        info = []
        info.append(reg_student_id)
        info.append(reg_student_name)
        info.append(reg_student_course_ids)
        info.append(reg_student_instruments)
        submitted = st.form_submit_button("Update Student")

        if submitted:
            if len(info) == 4:
                try:
                    manager.update_user("s", int(reg_student_id), name = reg_student_name, course_id = reg_student_course_ids, instruments = reg_student_instruments)
                except UserNotFound as e:
                    st.error(str(e))
            else:
                st.warning("Please enter your information fully.")

def user_table(manager, type = "s", user = None):
    match type.casefold():
        case "s":
            frame = pd.DataFrame(manager.list_students("a"))
            frame.columns = ["Student ID", "Student Name", "Enrolled Course", "Enrolled Instrument"]
            st.dataframe(frame, use_container_width = True, hide_index = True)
        case "u":
            st.dataframe(user, use_container_width = True, hide_index = True)
        case _:
            print("nothing now")

def show_student_management_page(manager):
    """Renders all components for the student management page."""
    st.header("Students")
    user_table(manager)
