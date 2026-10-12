import datetime as dt
import pytest

@pytest.fixture
def repo():
    class Repo:
        def __init__(self):
            self.courses = {
                "C101":{"id":"C101", "title":"Piano Basics", "description":"Intro", "capacity":2, "enrolled_ids":[],
                        "prereq_ids":[], "status":"OPEN", "level":"beginner", "instrument":"piano", "active":True},
                "C201":{"id":"C201", "title":"Advanced Violin", "description":"Bow mastery", "capacity":1, "enrolled_ids":["S9"],
                        "prereq_ids":["C150"], "status":"OPEN", "level":"advanced", "instrument":"violin", "active":True},
                "C301":{"id":"C301", "title":"Jazz Theory", "description":"Harmony", "capacity":3, "enrolled_ids":[],
                        "prereq_ids":[], "status":"CLOSED", "level":"intermediate", "instrument":"theory", "active":False}
            }
            self.students = {
                "S1":{"id":"S1", "passed_course_ids":["C150"]},
                "S2":{"id":"S2", "passed_course_ids":[]},
            }
            self.events = []

        def get_course(self, cid):
            return self.courses[cid]

        def get_student(self, sid):
            return self.students[sid]

        def add_enrollment(self, sid, cid):
            self.courses[cid]['enrolled_ids'].append(sid)

        def get_events_between(self, start, end):
            return [e for e in self.events if not (e['end'] <= start or e['start'] >= end)]

        def add_event(self, ev):
            self.events.append(ev)

        def list_courses(self):
            return list(self.courses.values())

    return Repo()

@pytest.fixture
def monday_10am():
    return dt.datetime(2025, 9, 22, 10, 0)