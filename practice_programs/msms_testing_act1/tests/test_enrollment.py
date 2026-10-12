import pytest
from domain.enrollment import enroll_student, EnrollmentError
from confest import repo

# repo = repo()

def test_enroll_success_when_open_and_capacity_and_prereqs(repo):
    ok = enroll_student("S1", "C201", repo = repo)
    assert ok is True
    assert "S1" in repo.get_course("C201")['enrolled_ids']

@pytest.mark.parametrize("sid, cid, expected_msg", [
    ("S1", "C301", "Course not open"),
    ("S1", "C201", "Already Enrolled"),
])

def test_enroll_failures(repo, sid, cid, expected_msg):
    if expected_msg == "Already Enrolled":
        repo.add_enrollment("S1", "C201")
        with pytest.raises(EnrollmentError) as e:
            enroll_student(sid, cid, repo = repo)
            assert expected_msg in str(e.value)

def test_course_full(repo):
    repo.add_enrollment("S1", "C101")
    repo.add_enrollment("S2", "C101")
    with pytest.raises(EnrollmentError) as e:
        enroll_student("S1", "C101", repo = repo)
        assert "Course full" in str(e.value)

def test_prereq_missing(repo):
    with pytest.raises(EnrollmentError) as e:
        enroll_student("S2", "C201", repo = repo)
        assert "Missing prerequisites" in str(e.value)