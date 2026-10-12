from datetime import time

class SchedulingError(Exception):
    pass

BUSINESS_HOURS = (time(8, 0), time(21, 0))

def schedule_lesson(teacher_id, student_id, start, end, room, *, repo, is_holiday):
    if end <= start:
        raise SchedulingError("End before start")

    # business hours
    if not(BUSINESS_HOURS[0] <= start.time() and end.time() <= BUSINESS_HOURS[1]):
        raise SchedulingError("Outside business hours")

    if (end - start).total_seconds() < 30 * 60:
        raise SchedulingError("Too short")

    if is_holiday(start.date()):
        raise SchedulingError("Public holiday")

    # conflicts
    for ev in repo.get_events_between(start, end):
        if ev['teacher_id'] == teacher_id or ev['room'] == room:
            raise SchedulingError("Conflict")

    repo.add_event(dict(teacher_id = teacher_id, student_id = student_id, start = start, end = end, room = room))
    return True