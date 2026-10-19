# Music School Management System (MSMS) — Stage 5

## Overview

MSMS is an educational music-school management application developed through five stages. Stage 4 builds on Stage 3's object-oriented schedule manager and replaces its command-line interaction with a multipage [Streamlit](https://streamlit.io/) web interface. Stage 5 adds automated pytest unit tests for the schedule manager. The interface keeps the scheduling and persistence logic in `app/` and presents student, course, lesson, roster, and attendance workflows through interactive pages.

This is a local prototype. Its JSON file is the data store, and its demonstration authentication and payment workflows are not intended for production use.

## Features

- Multipage navigation for student and course management, with a dashboard showing current student, teacher, and course totals.
- Register, find, update, and remove students; view the student list and download an ordered student CSV.
- Generate and download a student card.
- Create and update courses, enrol students, and remove courses.
- Create and update course lessons, and view rosters by course and/or weekday.
- Check students in to courses and persist attendance records.
- Customizable Streamlit theme settings in `.streamlit/config.toml`.
- A payments page placeholder for a future stage.

## Staged roadmap

| Stage | Focus | Application shape |
| --- | --- | --- |
| 1 | Prototype | Single-file command-line application |
| 2 | Data | Improved database structure and storage |
| 3 | Architecture | Object-oriented models, schedule controller, and CLI view |
| 4 | User interface | Multipage Streamlit interface using the Stage 3 operations |
| 5 | Quality assurance | Pytest unit tests for schedule-manager operations |

Stage 4 changes how users interact with the system; it is not a rewrite of the schedule manager. The Streamlit pages collect input and display results while `app/schedule.py` continues to own the scheduling operations and JSON persistence.

## Installation

Use Python and install the application's third-party dependencies from the `PST4` directory:

```powershell
cd PST4
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`streamlit` provides the UI and multipage navigation, `pandas` formats tables and CSV exports, and `bcrypt` is used by the prototype's export verification.
The Streamlit minimum version provides the `st.Page` and `st.navigation` interfaces used by the app.

## Usage

Run Streamlit from the `PST4` directory so that the relative data path resolves to `PST4/data/msms.json`:

```powershell
python -m streamlit run main.py
```

Streamlit prints a local URL in the terminal. Open it in a browser to use the app. The sidebar groups the pages into **Overview**, **Student Management**,
**Course Management**, and **Other**. Select **Dashboard** for the overview; the other pages provide student registration/search/update/removal and card downloads, course and lesson administration, roster lookup, enrollment, and check-in. Student CSV download is available from the **Students** page.

### How Stage 4 uses Streamlit

The Stage 4 interface is organized around Streamlit's multipage and rerun model:

- `main.py` launches the application with `streamlit run`.
- `gui/main_dashboard.py` sets the browser page title, icon, layout, and navigation using `st.set_page_config`, `st.Page`, and `st.navigation`.
- The schedule manager is kept in `st.session_state` for the current browser session, so navigating between pages does not create a new manager each time.
- Functions in `gui/student_pages.py` and `gui/roster_pages.py` build each screen with Streamlit inputs, forms, tables, messages, and download buttons.
- The page functions call the existing schedule manager for business operations and persistence rather than keeping a separate copy of the application data in the interface.

Form submission and page navigation rerun the Streamlit script. Use session state for values that must remain available across reruns; use forms to collect related inputs before submitting an operation.

### Customize the Streamlit theme and configuration

Streamlit reads `.streamlit/config.toml` at startup. This project already provides a dark theme; edit the color and font values to match a preferred palette. For example, the following shows the available theme areas used by this project:

```toml
[theme]
base = "dark"
primaryColor = "#7C4DFF"               # Buttons and accent elements
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#1B2230"
textColor = "#FAFAFA"
font = "sans serif"

[theme.sidebar]
backgroundColor = "#0080FF80"
```

The theme values are examples; change them to your own colors. For example, `base` can be `"light"` or `"dark"`, and `primaryColor` controls the accent
color. Theme configuration is separate from `st.set_page_config` in `gui/main_dashboard.py`, which controls page-specific settings such as title, icon, and layout.

Add optional sections only when needed, and consult the [Streamlit configuration reference](https://docs.streamlit.io/develop/api-reference/configuration/config.toml) for supported names and values. Save the file and restart the Streamlit server to apply configuration changes.

## Development notes

- `main.py` is the Streamlit launcher; `gui/main_dashboard.py` defines page configuration, session setup, the dashboard, and navigation.
- `gui/student_pages.py` and `gui/roster_pages.py` contain the Streamlit page functions and call into the schedule manager.
- `app/schedule.py` owns JSON persistence and the business operations. The model classes and sorting/search algorithms remain in `app/` and `algorithms/`.
- The schedule manager is stored in `st.session_state` so it is retained as the user changes pages within a Streamlit session.
- Records are stored in `data/msms.json`. Run the application from `PST4` because the manager's data path is relative to the current working directory.
- The export verification is a demonstration feature, not production authentication. Do not use the prototype to protect real personal or financial data.

## Stage 5: pytest unit testing

The schedule-manager unit tests are in `tests/test_schedule_manager.py`. They use a pytest fixture to create a fresh manager with a test data file, and check teacher and course operations, student registration and enrollment, user and course lookup, user removal and updates, payment recording and history, and synchronization between courses and students.

Run the tests from the `PST5` project directory. Set `PYTHONPATH` so Python can import the `app` package, then run pytest in verbose mode:

```powershell
$env:PYTHONPATH="."
pytest -vv
```

## Manual UI checks

For a manual UI smoke test, launch the app and verify that:

1. The dashboard and each sidebar page render.
2. Student registration, search, update, removal, and card download work.
3. Course and lesson creation/update/removal work with valid data.
4. Roster filters, enrollment, check-in, and CSV download behave as expected.
5. Theme or optional configuration changes in `.streamlit/config.toml` are
   visible after restarting the app.

Stage 3's controller and data tests remain in `PST3/tests`.

## Contributing

Keep changes focused on the relevant stage, add tests for new behavior, and describe the affected stage in the pull request.

## Credits and license

Author: SU CHENGZHANG. Teaching materials provided by Monash University Malaysia. This project is provided for educational purposes; add an open-source license before redistributing it.
