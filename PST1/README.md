# Music School Management System (MSMS)

## Overview

MSMS (Music School Management System) is an educational prototype that demonstrates how a small, in-memory application can evolve into a production-ready system across five staged upgrades. The Stage 1 implementation in this folder is a single-file CLI prototype (`MSMS.py`) that models Students and Teachers, supports registration and enrolment, and includes simple search and sorting utilities for searching purposes.

This README documents the Stage 1 behaviour, the staged roadmap, and guidance for progressing the project to production-quality software.

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

- In-memory data models: `Student` and `Teacher` objects with simple attributes.
- Basic front-desk CLI: register students, enrol students, lookup records, list and remove entries.
- Educational algorithms: `merge_sort` and `binary_search` implemented over object lists to perform stable searching and sorting.
- Case-insensitive search helpers for student and teacher lookup.
- From list of objects to csv file in `database_csv_navigator` function, for providing more obvious and convenient for offline data management. 

## Staged Roadmap

The project is designed to progress through five stages. Each stage should be implemented as an incremental upgrade to the previous stage.

- Stage 1 — Prototype: single-file script with in-memory lists and a CLI(command line interface) (`MSMS.py`).
- Stage 2 — Upgrade.
- Stage 3 — Architecture.
- Stage 4 — User Interface.
- Stage 5 — Quality Assurance.

## Installation

Requirements: Python 3.8+
Current project is run on Python 3.14.5.

1. Clone this repository and open the `PST1` folder.
2. (Optional) Create a virtual environment and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. (Stage 1) One external dependencies are required. If  add libraries later, recorded in `requirements.txt`.
- Pandas library
    - Install pandas to your virtual environment.
```
pip install pandas
```

## Usage

To run the Stage 1 CLI prototype execute:

```powershell
python MSMS.py
```

Menu operations include:
- Register a new student and enrol them in an instrument.
- Enrol an existing student by id.
- Lookup students or teachers by name or speciality (for teachers).
- List all students or teachers (admin).
- Remove a student or teacher by name (admin).
- Output students or teachers' database with .csv file (admin). 

Notes:
- Data is stored in memory only and will be lost when the program exits, use the csv function to store your changes offline or to device.
- The CLI prompts are minimal by design; input validation and confirmations are planned further.

## Development notes

- Key functions live in `MSMS.py` for Stage 1; refactor into modules for Stage 2 or further.
- `merge_sort` and `binary_search` are implemented for special needs in python objects comparison. 
- Consider adding type annotations, logging, and structured error handling before adding persistence.

## How to Contribute?

Suggested workflow:

1. Fork the repository and create a branch named `stageX/your-feature`.
2. Keep changes focused to a single stage or improvement.
3. Add tests for new behaviour and run them locally.
4. Open a pull request describing the change and which stage it targets.

## Tests

Stage 1 contains basic unit tests for core and front desk function, shown in `test.py` for:

- teachers and students database construction
- front-desk working flows and logic (`front_desk_register`, `front_desk_enrol`)
- search and sort utilities for remove function
- `database_to_csv` function is checked manually. 

## Credits

Author: SU CHENGZHANG and teaching materials provided by Monash University Malaysia — educational exercise in progressive software development.

## License

This work is provided for educational purposes. Add a permissive open-source license when publishing later if needed.

## Reference
- The format of readme file is taken from links below as a reference.
- 2022 edX Boot Camps LLC. . (2024). Professional README guide. In coding-boot-camp.github.io. https://coding-boot-camp.github.io/full-stack/github/professional-readme-guide
