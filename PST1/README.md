# Music School Management System (MSMS)

## Overview

MSMS (Music School Management System) is an educational prototype that demonstrates how a small, in-memory application can evolve into a production-ready system across five staged upgrades. The Stage 1 implementation in this folder is a single-file CLI prototype (`MSMS.py`) that models Students and Teachers, supports registration and enrolment, and includes simple search and sorting utilities for learning purposes.

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
- Educational algorithms: `merge_sort` and `binary_search` implemented over object lists.
- Case-insensitive search helpers for student and teacher lookup.

## Staged Roadmap

The project is designed to progress through five stages. Each stage should be implemented as an incremental upgrade to the previous stage.

- Stage 1 — Prototype: single-file script with in-memory lists and a CLI (`MSMS.py`).
- Stage 2 — Upgrade.
- Stage 3 — Architecture.
- Stage 4 — User Interface.
- Stage 5 — Quality Assurance.

## Installation

Requirements: Python 3.8+

1. Clone this repository and open the `PST1` folder.
2. (Optional) Create a virtual environment and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. (Stage 1) No external dependencies are required. If you add libraries later, record them in `requirements.txt`.

## Usage

To run the Stage 1 CLI prototype execute:

```powershell
python MSMS.py
```

Menu operations include:
- Register a new student and enrol them in an instrument.
- Enrol an existing student by ID.
- Lookup students or teachers by name or speciality.
- List all students or teachers (admin).
- Remove a student or teacher by name (admin).

Notes:
- Data is stored in memory only and will be lost when the program exits.
- The CLI prompts are minimal by design; input validation and confirmations are planned for Stage 2.

## Development notes

- Key functions live in `MSMS.py` for Stage 1; refactor into modules for Stage 2.
- `merge_sort` and `binary_search` are implemented for educational clarity. For production use, prefer Python's built-ins (`sorted`, `bisect`) and a proper indexed datastore.
- Consider adding type annotations, logging, and structured error handling before adding persistence.

## Contributing

Suggested workflow:

1. Fork the repository and create a branch named `stageX/your-feature`.
2. Keep changes focused to a single stage or improvement.
3. Add tests for new behaviour and run them locally.
4. Open a pull request describing the change and which stage it targets.

## Tests

Stage 1 contains no formal tests. When you refactor (Stage 2) and add API or persistence (Stages 3–4), include `pytest` tests for:

- model constructors and validation
- front-desk flows (`front_desk_register`, `front_desk_enrol`)
- search and sort utilities

## Credits

Author: SU CHENGZHANG and teaching materials provided by Monash University Malaysia — educational exercise in progressive software development.

## License

This work is provided for educational purposes. Add a permissive open-source license when publishing.
