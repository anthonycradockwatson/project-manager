# Project Manager

A lightweight, Python-based project management desktop app with a focus on automation features (GUI built with CustomTkinter, data stored using Pickle). Use this README as the canonical site for quickstart, usage, and the automation capabilities that make this project stand out.

Short repository description (use for GitHub repo description):
Project Manager — a Python desktop app (CustomTkinter) with Pickle-backed storage and powerful automation to help you schedule, prioritize and bulk-manage tasks.

Table of contents
- Features (automation-focused)
- Screenshots
- Tech stack
- Installation
- Configuration
- Usage
- Automation features (detailed)
- Development
- Tests
- Contributing
- License
- Contact

Features (high level)
- GUI desktop app built with CustomTkinter for a modern native-like look and feel
- Simple object DB using Python's pickle (PKL) for single-file storage — lightweight and portable
- Add, edit, and remove projects and tasks
- Assign tasks to people and track status and progress
- Search and filter tasks

Automation-focused features (what this project emphasizes)
- Automatic scheduling: define due dates and recurrence rules; the app can automatically create recurring tasks and reschedule completed ones
- Smart prioritization: automation rules that prioritize tasks based on due date proximity, project importance, and estimated effort
- Auto-assignment: create rules that auto-assign tasks to users based on workload or tags
- Bulk automation operations: import CSV / bulk-create tasks, bulk-update statuses, and run automated cleanups (archive completed tasks older than X days)
- Auto-backup: scheduled backups of the PKL database file to a configurable folder
- Notifications (optional): window popups and optional logging for scheduled reminders

If any of the above automation behaviors are not implemented exactly as written, tell me which are different and I will update this section to match the exact behavior and UI flow.

Screenshots
If you want screenshots in the README, add them to the repository under `docs/screenshots/` or `.github/images/` and I will embed them here.

Example markdown to include after you upload images:

![Dashboard screenshot](docs/screenshots/dashboard.png)
![Task detail screenshot](docs/screenshots/task_detail.png)

Tech stack
- Python (100% of repo)
- GUI: CustomTkinter
- Storage: Python Pickle (.pkl / .pkldb) object DB
- Optional / likely deps: Pillow (for images/icons), schedule or APscheduler (if you use background scheduling). List real packages in `requirements.txt` for reproducible installs.

Installation
1. Clone the repo

```bash
git clone https://github.com/anthonycradockwatson/project-manager.git
cd project-manager
```

2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

If this project doesn't have a `requirements.txt` yet, create one with the dependencies (for example: `customtkinter`, `pillow`, `schedule`) or tell me which packages to pin and I can create it and commit it.

Configuration
- The app uses a local Pickle file to persist data. By default the DB file is stored as `data/db.pkl` (adjust path in the app if different).
- Automation settings (recurrence rules, backup paths, auto-assign rules) are stored in the same Pickle DB or in a config file depending on your implementation.
- If you prefer a `.env` or `config.ini`, add a sample file (e.g., `.env.example`) and I will add usage instructions.

Usage
- GUI: run the main application file. Common example commands (adjust to match your actual entrypoint):

```bash
python main.py
# or, if your package provides a module entrypoint
python -m project_manager
```

- The GUI provides menus and dialogs to create projects and tasks. See the Automation section below for how to configure automation rules.

Automation features — how to use them (examples)
- Recurring tasks
  - Create a task and mark it as recurring (daily/weekly/monthly). The app will auto-create the next occurrence when the current one is completed.
- Smart prioritization
  - Define project importance and estimated effort. Enable the prioritization automation rule and the app will reorder task lists to surface the highest priority items.
- Auto-assignment
  - Define rules (e.g., tasks tagged "frontend" assigned to "Alice", or round-robin assignment among team members). Use the Automations panel to add/edit rules.
- Bulk operations
  - Import CSV files to create many tasks at once. Use the Import action in Tools > Import CSV. The same Tools menu can run bulk status updates or archive operations.
- Auto-backup
  - Enable scheduled backups and pick a target folder. The app will create timestamped copies of the Pickle DB on the schedule you configure.

If you have concrete UI text or menu names for these flows, paste them here and I'll update the README to show step-by-step GUI interactions with exact names and screenshots.

Development
- Run with a dev virtualenv (see Installation)
- Linting and formatting suggestions: black, flake8. Add pre-commit hooks if desired.

Tests
- If you have automated tests (pytest, unittest), add instructions to run them (`pytest` or `python -m pytest`). If you don't yet have tests, I can add a basic test scaffold.

Contributing
Contributions welcome — open an issue to discuss features/bugs and submit pull requests. Please include tests for new behavior and follow existing formatting/linting rules. If you'd like a CONTRIBUTING.md, tell me any rules or a template and I'll create one.

License
Add your project's license here (MIT, Apache-2.0, GPL-3.0, etc.). Tell me which license you prefer and I will add a LICENSE file.

Contact
Maintainer: anthonycradockwatson
Email: anthonycradockwatson@gmail.com

---

What I changed
- Updated README.md to reflect the real GUI framework (CustomTkinter) and the Pickle-based storage you told me about
- Re-focused the README to highlight the automation features as the primary selling point

Next steps I can take right away
- Embed screenshots into the README if you upload them to `docs/screenshots/` or provide links — tell me which screenshot goes where (Dashboard, Task detail, Automations panel, etc.)
- Create a `requirements.txt` with the packages you use (CustomTkinter and any scheduling libs you rely on)
- Add a LICENSE or CONTRIBUTING.md file
- Add quickstart commands or correct `main.py` entrypoint if you tell me the actual filename or module to run

Tell me which of those you'd like me to do next, and/or upload any screenshots you want included.
