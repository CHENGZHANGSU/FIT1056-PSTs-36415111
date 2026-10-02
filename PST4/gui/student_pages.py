# gui/student_pages.py
import pandas as pd
import streamlit as st
import time, bcrypt

from Exceptions.NotFoundException import UserNotFound
from Security.Verification import Verification

def find_student_page():
    time.sleep(0.5)
    show_find_student_page(st.session_state.manager)

def add_student_page():
    time.sleep(0.5)
    show_add_student_page(st.session_state.manager)

def update_student_page():
    time.sleep(0.5)
    show_update_student_page(st.session_state.manager)

def remove_student_page():
    time.sleep(0.5)
    show_remove_student_page(st.session_state.manager)

def list_students_page():
    time.sleep(0.5)
    show_student_management_page(st.session_state.manager)

def print_student_card():
    time.sleep(0.5)
    show_print_student_card_page(st.session_state.manager)


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
            with st.spinner(f"Registering for {reg_name}..."):
                time.sleep(2)
                if reg_name and reg_instrument:
                    new_student = manager.front_desk_register(reg_name, reg_course_id, reg_instrument)
                    if new_student:
                        st.success(f"Successfully registered {reg_name}!")
                        st.balloons()
                        manager.save_all()
                        # You can use st.balloons() for extra flair.
                    else:
                        st.error(f"Could not register student. A teacher for {reg_instrument} might not be available.")
                else:
                    st.warning("Please enter both a name and an instrument.")

def show_find_student_page(manager):
    # --- Search Section ---#
    st.subheader("Find Student")
    with st.form("Student information"):
        reg_student_id = st.text_input(label = "Student ID", placeholder = "Enter your student id: ", type = "search")
        submitted = st.form_submit_button("Find Student")

        if submitted:
            with st.spinner(f"Looking for student{reg_student_id}..."):
                time.sleep(2)
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
        reg_student_id = st.text_input(label = "Student ID", placeholder = "Enter your student id: ")
        reg_student_name = st.text_input(label = "Student Name", placeholder = "Enter your student name")
        reg_student_course_ids = st.text_input(label = "Course ID(s)", placeholder = "Enter the course ID to enrol the student in (split with , for more than one): ")
        reg_student_instruments = st.text_input(label = "Instrument(s)", placeholder = "Enter the instrument you play (split with , when more than 1): ")
        info = []
        info.append(reg_student_id)
        info.append(reg_student_name)
        info.append(reg_student_course_ids)
        info.append(reg_student_instruments)
        submitted = st.form_submit_button("Update Student")

        if submitted:
            if len(info) == 4:
                with st.spinner(f"Updating for Student {reg_student_name}..."):
                    time.sleep(2)
                    try:
                        manager.update_user("s", int(reg_student_id), name = reg_student_name, course_id = reg_student_course_ids, instrument = reg_student_instruments)
                        manager.save_all()
                    except UserNotFound as e:
                        st.error(str(e))
            else:
                st.warning("Please enter your information fully.")

def show_remove_student_page(manager):
    st.subheader("Remove Student")
    if manager.students:
        select = st.selectbox("Select Student ID", [s.get_id() for s in manager.students], index = None, placeholder = "Select or Enter the Student ID")
        student = None
        if select:
            student = manager.find_user_by_id(int(select), "s")
        if student:
            user_table(manager, "u", [student.__dict__])
        # else:
        #     st.error(f"Could not find this student.") 
        confirm = st.checkbox("Confirm Remove")
        delete = st.button("Remove")

        if delete:
            if confirm:
                if select:
                        with st.spinner("Removing Student..."):
                            time.sleep(2)
                            try:
                                manager.remove_user(int(select), "s")
                                manager.save_all()
                            except Exception as e:
                                st.error(str(e))
                else:
                    st.error(UserNotFound)
            else:
                st.info("Please Confirm")

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
    with st.spinner("Retrieving the Student Database"):
        user_table(manager)
        time.sleep(2)
        order = st.selectbox("Order", ["ascending", "descending"], index = None, placeholder = "Please choose the order to download")
        if order:
            account = st.text_input("Account", placeholder = "Please enter your account to download the student database")
            password = st.text_input("Password", placeholder = "Please enter your password to download the student database", type = "password")
            if account and password:
                verifier = Verification(account, password)
                if verifier.verify():
                    csv = manager.database_to_csv("s", order)
                    download_button = st.download_button(label = "Download Student CSV", data = csv, file_name="Students.csv", mime="text/csv", icon=":material/download:")
                    if download_button:
                        st.success("Download successful!")
                else:
                    st.error("Incorrect account or password")

def show_print_student_card_page(manager):
    st.subheader("Student Card")
    with st.form("Print Card"):
        reg_student_id = st.text_input(label = "Student ID", placeholder = "Enter your student id: ", type = "search")
        submitted = st.form_submit_button("Print Student Card")

        if submitted:
            with st.spinner("Retrieving the Student information"):
                time.sleep(2)

    if reg_student_id:
            student = manager.find_user_by_id(int(reg_student_id), "s")
            if student:
                filename = manager.print_student_card(int(reg_student_id))
                with open(f"{filename}", "r") as f:
                    text = f.read()
                download_button = st.download_button(label = "Download Student Card", data = text, file_name=f"Student{reg_student_id} card.txt", 
                                                        mime="text/plain", icon=":material/download:")
                if download_button:
                    st.success("Download successful!")
            else:
                st.error(f"Could not find this student.")
    else:
        st.warning("Please enter your student id.")
