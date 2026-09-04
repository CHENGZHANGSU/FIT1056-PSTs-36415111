# Music School Management System (MSMS) — Stage 3

## Overview

MSMS (Music School Management System) is an educational prototype that demonstrates how a small application can evolve across five staged upgrades. Stage 3 refactors the Stage 2 data-handling program into an object-oriented command-line application. The system separates the view functions in `main.py` from the business logic in `app/schedule.py` and represents users and courses with dedicated classes.

Stage 3 loads the school database from JSON, converts records into objects, keeps student and course enrollments synchronized, and saves changes back to JSON. It also manages teachers, courses, lessons, attendance records, student cards, and CSV exports.

This README documents the Stage 3 behavior, the staged roadmap, and guidance for progressing the project to production-quality software.

## Table of contents
- [Features](#features)
- [Staged Roadmap](#staged-roadmap)
- [Installation](#installation)
- [Usage](#usage)
- [Development notes](#development-notes)
- [Contributing](#contributing)
- [Tests](#tests)
- [Credits](#credits)
- [License](#license)

## Features

- Object-oriented data models: `User`, `StudentUser`, `TeacherUser`, and `Course`.
- JSON persistence through `ScheduleManager`, including loading, object conversion, saving, and ID counters.
- Front-desk workflows to register students, add teachers, enrol students or teachers, update users, and remove users.
- Course administration for adding, updating, and removing courses.
- Lesson administration for adding, updating, viewing, and removing lessons associated with courses.
- Daily roster views that display lessons for a selected day or all days.
- Attendance recording with `check_in()` and attendance-list display.
- Automatic synchronization between student enrollments and the student IDs stored by each course.
- Student-card generation as a text file in the `data` directory.
- CSV export for student, teacher, attendance, or all supported databases using pandas.
- `merge_sort` and `binary_search` algorithms for ordered database views and user lookup.

## Staged Roadmap

The project is designed to progress through five stages. Each stage should be implemented as an incremental upgrade to the previous stage.

- Stage 1 — Prototype: single-file script with in-memory lists and a CLI(command line interface) (`MSMS.py`).
- Stage 2 — Upgrade: refractor the database structure for more efficient use and storage (`pst2_main.py`). 
- Stage 3 — Architecture: refactor the dictionary database into OOP operations with a controller, model classes, and a CLI view layer (`main.py` and `app/`).
- Stage 4 — User Interface.
- Stage 5 — Quality Assurance.

## Installation

Requirements: Python 3.8+
The project is currently run on Python 3.14.5. Stage 3 also uses pandas for CSV export.

1. Clone this repository and open the `PST3` folder.
2. (Optional) Create a virtual environment and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install & Import the Stage 3 dependency:
```
import json
import datetime
import re
import pandas as pd
import os
```

## Usage

To run the Stage 3 CLI application, change into the `PST3` directory and execute:

```powershell
python main.py
```

The application reads from `data/msms.json` by default. Menu operations include:
- View a daily roster for a selected day or all days.
- List students, teachers, courses, or attendance records.
- Add students, teachers, courses, and lessons.
- Enrol a student in a course or assign / reassign a teacher to a course.
- Update or remove users, courses, and lessons.
- Print a student card to `data/{student_id}_card.txt`.
- Export student, teacher, attendance, or complete supported data sets to `output_csv/`.
- Save changes and quit with `q`.

Notes:
- Data is kept in memory while the application runs and is persisted to `data/msms.json` when the application saves.
- The default data path is relative to the current working directory, so run the command from `PST3`.
- The CLI uses short choices such as `s` for students, `t` for teachers, `c` for courses, and `a` for attendance.
- Course and student enrolment lists are synchronized at the start of each menu loop.

## Development notes

- `main.py` is the view layer and collects user input before delegating operations to `ScheduleManager`.
- `app/schedule.py` is the application controller. It owns persistence, searching, sorting, enrolment, course, lesson, attendance, and export operations.
- `app/user.py` defines the base `User` model; `app/student.py` and `app/teacher.py` define specialized users via inheritance and the `Course` model.
- `algorithms/algorithm.py` contains `merge_sort` and `binary_search`.
- `data/msms.json` stores students, teachers, courses, attendance records, lessons, and the next available IDs.
- JSON records are converted to model objects by `_to_object()` after loading and converted back for persistence or CSV export.
- Changes will only be saved once the user choice option `Save and Quit`.

## How to Contribute?

Suggested workflow:

1. Fork the repository and create a branch named `stageX/your-feature`.
2. Keep changes focused to a single stage or improvement.
3. Add tests for new behaviour and run them locally.
4. Open a pull request describing the change and which stage it targets.

## Tests

Stage 3 does include a dedicated test module in the `PST3/tests` folder. The interactive application can be started with:

```powershell
cd PST3
python .\tests\stage3_test.py
```

Manual cover:

- JSON loading and saving through `ScheduleManager`.
- Student and teacher registration, enrolment, update, and removal.
- Course and lesson creation, update, display, and removal. (**half way**)
- Synchronization between student and course enrolment records.
- Attendance check-in and attendance display. (**Manually checked**)
- Student-card and CSV output generation. (**Manually checked**)
- Ascending and descending user searches using the supplied algorithms.

## Credits

Author: SU CHENGZHANG and teaching materials provided by Monash University Malaysia — educational exercise in progressive software development.

## License

This work is provided for educational purposes. Add a permissive open-source license when publishing later if needed.

## Reference
- The format of readme file is taken from links below as a reference.
- 2022 edX Boot Camps LLC. . (2024). Professional README guide. In coding-boot-camp.github.io. https://coding-boot-camp.github.io/full-stack/github/professional-readme-guide
