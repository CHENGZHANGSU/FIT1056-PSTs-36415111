class EnrollmentError(Exception):
    pass

def enroll_student(student_id, course_id, *, repo):
    course = repo.get_course(course_id)
    student = repo.get_student(student_id)

    if course['status'] != 'OPEN':
        raise EnrollmentError("Course not open")

    if student_id in course['enrolled_ids']:
        raise EnrollmentError("Already Enrolled")

    if len(course['enrolled_ids']) >= course['capacity']:
        raise EnrollmentError("Course full")

    missing = set(course['prereq_ids']) - set(student['passed_course_ids'])
    if missing:
        raise EnrollmentError("Missing prerequisites")

    repo.add_enrollment(student_id, course_id)
    return True