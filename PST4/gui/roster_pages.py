# gui/roster_pages.py
import streamlit as st
import pandas as pd
import time

from app.schedule import Course
from Exceptions.NotFoundException import UserNotFound, CourseNotFound
from gui.student_pages import user_table

def roster_page():
    time.sleep(0.5)
    show_roster_page(st.session_state.manager)

def check_in_page():
    time.sleep(0.5)
    show_check_in_page(st.session_state.manager)

def enrollment_page():
    time.sleep(0.5)
    show_enrollment_page(st.session_state.manager)

def create_course_page():
    time.sleep(0.5)
    show_create_course_page(st.session_state.manager)

def update_course_page():
    time.sleep(0.5)
    show_update_course_page(st.session_state.manager)

def create_lesson_page():
    time.sleep(0.5)
    show_create_lesson_page(st.session_state.manager)

def update_lesson_page():
    time.sleep(0.5)
    show_update_lesson_page(st.session_state.manager)

def remove_lesson_page():
    time.sleep(0.5)
    show_remove_course_page(st.session_state.manager)

def _all_lesson_with_course(manager, course_name):
    res = manager.front_desk_daily_roster("c", course_name)
    course = res[0].__dict__
    course.pop('lessons', None)
    course_frame = pd.DataFrame([course])
    st.subheader(f"Course {course['id']}: {course['name']}")
    st.dataframe(course_frame, use_container_width = True, hide_index = True)
    lesson_frame = pd.DataFrame(res[1])
    st.subheader(f"Lessons of Course {course['id']} {course['name']}")
    st.dataframe(lesson_frame, use_container_width = True, hide_index = True)
    st.success(f"Find the lesson of {course_name} successfully.")

def show_roster_page(manager):
    """Renders the daily roster and check-in functionality."""
    st.header("Daily Roster")
    # --- View Roster Section (remains the same) ---
    day = st.selectbox("Select a day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], index = None, 
                       placeholder = "Choose a weekday (or leave it blank)")
    course_name = st.selectbox("Select a course", [c.name for c in manager.courses], index = None, 
                                   placeholder = "Choose a course (or leave it blank)")

    # ... (code to display the dataframe) ...
    with st.form("roster_form"):
        submitted = st.form_submit_button("Search")
        if submitted:
            with st.spinner("Sending your request..."):
                time.sleep(2)
                if day and course_name:
                    try:
                        res = manager.front_desk_daily_roster("l", course_name, day)
                        course = res[0].__dict__
                        course.pop('lessons', None)
                        course_frame = pd.DataFrame([course])
                        st.subheader(f"Course {course['id']}: {course['name']}")
                        st.dataframe(course_frame, use_container_width = True, hide_index = True)
                        lesson_frame = pd.DataFrame(res[1])
                        st.subheader(f"Lessons of Course {course['id']} {course['name']}")
                        st.dataframe(lesson_frame, use_container_width = True, hide_index = True)
                        st.success(f"Find the lesson of {course_name} on {day} successfully.")
                    except CourseNotFound:
                        st.error(str(CourseNotFound))
                elif course_name:
                    try:
                        _all_lesson_with_course(manager, course_name)
                    except CourseNotFound:
                        st.error(str(CourseNotFound))
                elif day:
                    try:
                        res = manager.front_desk_daily_roster("a", None, day)
                        for i in range(len(res[0])):
                            course = res[0][i].__dict__         # the course objects
                            course.pop('lessons', None)
                            course_frame = pd.DataFrame([course])
                            st.subheader(f"Course {course['id']}: {course['name']}")
                            st.dataframe(course_frame, use_container_width = True, hide_index = True)
                            lesson_frame = pd.DataFrame(res[1][i])  # the lessons for that course
                            st.subheader(f"Lessons of Course {course['id']} {course['name']}")
                            st.dataframe(lesson_frame, use_container_width = True, hide_index = True)
                        st.success(f"Find the lesson of {day} successfully.")
                    except CourseNotFound:
                        st.error(str(CourseNotFound))
                else:
                    st.info("Please select a weekday or(and) a course name.")
    
def show_check_in_page(manager):
    # --- Student Check-in Section (now works correctly) ---
    st.subheader("Student Check-in")
    with st.form("check_in_form"):
        # To make this user-friendly, we should populate the dropdowns dynamically.
        # Get lists of student names and course names from the manager.
        student_list = {s.name: s.id for s in manager.students}
        course_list = {c.name: c.id for c in manager.courses}
        
        selected_student_name = st.selectbox("Select Student", student_list.keys(), index = None, placeholder = "Enter student name")
        selected_course_name = st.selectbox("Select Course", course_list.keys(), index = None, placeholder = "Enter course name")
        
        submitted = st.form_submit_button("Check-in Student")

        if submitted:
            with st.spinner(f"Checking in for student {selected_student_name} to {selected_course_name}"):
                time.sleep(2)
                # Convert the selected names back to IDs
                student_id = student_list[selected_student_name]
                course_id = course_list[selected_course_name]

                # This call now works because we implemented the method in PST3.
                success = manager.check_in(student_id, course_id)

                if success:
                    st.success(f"Checked in {selected_student_name} for {selected_course_name}!")
                else:
                    # The manager's print statements will go to the console, but we can add a GUI error too.
                    st.error("Check-in failed. See console for details. (Is the student enrolled in that course?)")

def show_enrollment_page(manager):
    st.subheader("Student Enrollment")

    student_list = {s.id: s.id for s in manager.students}
    course_list = {c.id: c.id for c in manager.courses}
    selected_student_id = st.selectbox("Select Student", student_list.keys(), index = None, placeholder = "Enter student name")
    if selected_student_id:
        try:
            student = manager.find_user_by_id(int(selected_student_id), "s")
            user_table(manager, "u", [student.__dict__])
        except UserNotFound as e:
            st.error(str(e))
    selected_course_id = st.selectbox("Select Course", course_list.keys(), index = None, placeholder = "Enter course name")
    with st.form("Enroll Student"):
        confirm = st.checkbox("Confirm Enrollment")

        submitted = st.form_submit_button("Enroll-in Student")
        if submitted:
            if selected_course_id and selected_student_id:
                with st.spinner(f"Enrolling student {selected_student_id} to course {selected_course_id}"):
                    time.sleep(2)
                    try:
                        course = manager.find_course_by_id(int(selected_course_id))
                        if not confirm:
                            st.info("Please confirm.")
                        elif int(selected_student_id) in course.get_enrolled_student_ids():
                            st.warning(f"Student {selected_student_id} already enrolled in course {selected_course_id}")
                        else:
                            manager.front_desk_enrol(selected_student_id, selected_course_id, "s")
                            st.success(f"Successfully enrolled student {selected_student_id} to course {selected_course_id}")
                    except Exception as e:
                        st.error(str(e))
            else:
                st.info("Please select the student and the course.")

def show_create_course_page(manager):
    st.subheader("Create New Course")
    with st.form("Create Course"):
        course_name = st.text_input(label = "Course Name", placeholder = "Enter the course name")
        course_instrument = st.text_input(label = "Instrument", placeholder = "Enter the instrument for this course")
        teacher_id = st.text_input(label = "Teacher ID", placeholder = "Enter the teacher ID for this course")
        submitted = st.form_submit_button("Create Course")

        if submitted:
            if course_name or course_instrument or teacher_id:
                with st.spinner(f"Updating course {course_name}..."):
                    time.sleep(2)
                    try:
                        manager.add_course(course_name = course_name, instrument = course_instrument, 
                                                        teacher_id = int(teacher_id))
                        manager.save_all()
                        st.success(f"Successfully created course {course_name} with ID {manager.id['next_course_id'] - 1}")
                    except Exception as e:
                        st.error(str(e))
            else:
                st.info("Please fill in all fields to create a new course.")

def show_update_course_page(manager):
    st.subheader("Update Course")
    with st.form("Update Course"):
        course_list = {c.name: c.id for c in manager.courses}
        selected_course_name = st.selectbox(label = "Select Course", options = list(course_list.keys()))
        course_name = st.text_input(label = "Course Name", placeholder = "Enter the new course name")
        course_instrument = st.text_input(label = "Instrument", placeholder = "Enter the new instrument for this course")
        teacher_id = st.text_input(label = "Teacher ID", placeholder = "Enter the teacher ID for this course")
        submitted = st.form_submit_button("Update Course")

        if submitted:
            if course_name or course_instrument or teacher_id or selected_course_name:
                course_id = course_list[selected_course_name]
                with st.spinner(f"Updating course {course_name}..."):
                    time.sleep(2)
                    try:
                        manager.update_course(course_id = course_id, course_name = course_name, 
                                              instrument = course_instrument, teacher_id = int(teacher_id))
                        manager.save_all()
                        st.success(f"Successfully update course {course_name} with ID {course_id}")
                    except Exception as e:
                        st.error(str(e))
            else:
                st.info("Please fill in all fields to update a course.")

def show_create_lesson_page(manager):
    st.subheader("Create New Lesson")
    with st.form("Create Lesson"):
        course_list = {c.name: c.id for c in manager.courses}
        selected_course_name = st.selectbox(label = "Select Course", options = list(course_list.keys()))
        lesson_id = manager.id['next_lesson_id']
        lesson_day = st.selectbox(label = "Day", options = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
        lesson_start_time = st.time_input(label = "Start Time")
        lesson_room = st.text_input(label = "Room", placeholder = "Enter the room for this lesson")
        submitted = st.form_submit_button("Create Lesson")

        if submitted:
            if lesson_id and lesson_day and lesson_start_time and lesson_room:
                course_id = course_list[selected_course_name]
                course = manager.find_course_by_id(course_id)
                with st.spinner(f"Creating lesson {lesson_id} for course {selected_course_name}..."):
                    time.sleep(2)
                    try:
                        # Assuming there's a method to add lessons, similar to add_course
                        manager.add_lessons(course, (lesson_id, lesson_day, str(lesson_start_time), lesson_room))
                        manager.save_all()
                        st.success(f"Successfully created lesson {lesson_id} for course {selected_course_name}")
                    except Exception as e:
                        st.error(str(e))
            else:
                st.info("Please fill in all fields to create a new lesson.")

def show_update_lesson_page(manager):
    st.subheader("Update New Lesson")
    with st.form("Update Lesson"):
        course_list = {c.name: c.id for c in manager.courses}
        selected_course_name = st.selectbox(label = "Select Course", options = list(course_list.keys()))
        checked = st.form_submit_button("Check Lesson Info")
        lesson_id = st.text_input(label = "Lesson ID", placeholder = "Enter the lesson id needed for update: ", key = "my_input")
        lesson_day = st.selectbox(label = "Day", options = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], index = None,
                                  placeholder = "Choose the new day for the lesson")
        lesson_start_time = st.time_input(label = "New Start Time")
        course_id = course_list[selected_course_name]
        course = manager.find_course_by_id(course_id)

        lesson_room = st.text_input(label = "New Room", placeholder = "Enter the new room for this lesson")
        submitted = st.form_submit_button("Update Lesson")

        if checked:
            _all_lesson_with_course(manager, selected_course_name)


        if submitted:
            if lesson_id and lesson_day and lesson_start_time and lesson_room:
                with st.spinner(f"Updating lesson {lesson_id} for course {selected_course_name}..."):
                    time.sleep(2)
                    try:
                        # Assuming there's a method to add lessons, similar to add_course
                        manager.update_lesson(course, (lesson_id, lesson_day, str(lesson_start_time), lesson_room))
                        manager.save_all()
                        st.success(f"Successfully update lesson {lesson_id} for course {selected_course_name}")
                    except Exception as e:
                        st.error(str(e))
            else:
                st.info("Please fill in all fields to update a lesson.")

def show_remove_course_page(manager):
    st.subheader("Remove Course")
    with st.form("Remove Course"):
        course_list = {c.name: c.id for c in manager.courses}
        selected_course_name = st.selectbox(label = "Select Course", options = list(course_list.keys()))
        checked = st.form_submit_button("Check Lesson Info")
        if checked:
            _all_lesson_with_course(manager, selected_course_name)

        dict_courses = []
        for course in manager.courses.copy():
            cur_course = Course(course.get_course_id(), course.get_course_name(), course.get_course_instrument(), course.get_course_teacher_id())
            cur_course.set_enroll_student_lst(course.get_enrolled_student_ids())
            cur_course.__dict__.pop('lessons', None)
            dict_courses.append(cur_course.__dict__)
        frame = pd.DataFrame(dict_courses)
        st.dataframe(frame, use_container_width = True, hide_index = True)

        remove_course_name = st.selectbox(label = "Select Course", options = list(course_list.keys()), index = None,
                                          placeholder = "Select the course need to be removed")
        submitted = st.form_submit_button("Remove Course")

        if submitted:
            if remove_course_name:
                course_id = course_list[remove_course_name]
                with st.spinner("Removing the course..."):
                    time.sleep(2)
                    try:
                        course = manager.find_course_by_id(course_id)
                        manager.remove_course(course)
                        manager.save_all()
                        st.success(f"Remove the Course {course_id} {remove_course_name} successfully.")
                    except Exception as e:
                        st.error(str(e))
            else:
                st.info("Please fill in the course name.")