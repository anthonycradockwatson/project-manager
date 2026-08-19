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
- Automation model
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
- Notifications: window popups, optional logging, and email notifications for scheduled reminders or rule-triggered alerts

Screenshots
If you want screenshots in the README, add them to the repository under `docs/screenshots/` or `.github/images/` and I will embed them here.

Example markdown to include after you upload images:

![Dashboard screenshot](docs/screenshots/dashboard.png)
![Task detail screenshot](docs/screenshots/task_detail.png)

Tech stack
- Python (100% of repo)
- GUI: CustomTkinter
- Storage: Python Pickle (.pkl / .pkldb) object DB
- Optional / likely deps: Pillow (for images/icons), schedule or APScheduler (if you use background scheduling), pandas (for CSV import). List real packages in `requirements.txt` for reproducible installs.

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
- Automation settings (rules, recurrence rules, backup paths, auto-assign rules) are stored in the same Pickle DB or in a config file depending on your implementation.
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

Automation model (how automations actually work)
This project implements a flexible rule-based automation system built from two core concepts: triggers and actions.

- Triggers
  - A trigger is a condition that can be time-based or status-based. Triggers may be combined so that a single action requires one or more triggers to be satisfied before running.
  - Time-based triggers: fire when a deadline or time window is reached (for example, "due in 24 hours", "on a specific date/time", or on a recurring schedule).
  - Status-based triggers: fire when a task or project changes state (for example, "task status becomes Completed", "priority changes to High").

- Actions
  - An action is what the automation performs when its triggers are satisfied. Typical actions implemented in this project include:
    - Send an email notification to a configured address (SMTP settings can be configured in-app or via config)
    - Create a timestamped log entry (audit trail) in the application log
    - Change task or project metadata (status updates, reassignment, priority changes)
  - Actions may run immediately when triggers fire, or be scheduled/delayed according to rule settings.

- Putting it together: Actions with multiple triggers
  - You can create an automation action and attach one or more triggers. By default, all configured triggers must be satisfied for the action to run (logical AND). If you prefer OR semantics or more complex boolean logic, tell me and I can add guidance or UI changes to support it.

Examples
- Example 1 — Reminder + escalation
  - Triggers: time-based — task due in 24 hours; status-based — status is "In Progress"
  - Actions: send email to assignee; add log entry

- Example 2 — Auto-archive completed items
  - Triggers: status-based — status changed to "Completed" AND task completed date is older than 30 days
  - Actions: change status to "Archived"; add log entry

- Example 3 — Auto-assign based on tag
  - Triggers: status-based — new task created with tag "frontend"
  - Actions: change assignee to "Alice"; add log entry

Where to configure automations
- The app's Automations panel (Tools > Automations or Automations in the Settings menu) provides a UI to create, edit, enable/disable rules. When creating a rule you:
  1. Create a new Action (give it a name and optional description)
  2. Add one or more Triggers (choose time or status, configure parameters)
  3. Add one or more Actions (send email, create log entry, change status)
  4. Save and enable the rule — rules can be tested immediately using the Test button (if available) or by creating a test task that matches the trigger conditions.

If your UI uses different menu names or flows, paste those exact names and I'll update this section to match the app screens.

Development
- Run with a dev virtualenv (see Installation)
- Linting and formatting suggestions: black, flake8. Add pre-commit hooks if desired.

Tests
- If you have automated tests (pytest, unittest), add instructions to run them (`pytest` or `python -m pytest`). If you don't yet have tests, I can add a basic test scaffold.

Contributing
Contributions welcome — open an issue to discuss features/bugs and submit pull requests. Please include tests for new behavior and follow existing formatting/linting rules. If you'd like a CONTRIBUTING.md I can add a template.

License
Add your project's license here (MIT, Apache-2.0, GPL-3.0, etc.). Tell me which license you prefer and I will add a LICENSE file.

Contact
Maintainer: anthonycradockwatson
Email: anthonycradockwatson@gmail.com

---

What I changed
- Clarified the automation model: how triggers and actions work, types of triggers (time/status), examples, and where to configure automations in the UI
- Kept earlier content about frameworks (CustomTkinter) and Pickle storage and expanded the Automation section with concrete examples and expected behaviors

Next steps I can take
- Embed screenshots into the README if you upload them to `docs/screenshots/` or provide links — tell me which screenshot goes where (Dashboard, Task detail, Automations panel, etc.)
- Create a `requirements.txt` with the packages you use (CustomTkinter and any scheduling libs you rely on)
- Add a LICENSE or CONTRIBUTING.md file
- Add exact quickstart commands if you tell me the app entrypoint file (e.g., `main.py`)

Would you like me to add a `requirements.txt` with default pins for `customtkinter`, `pillow`, and `schedule` and to create a LICENSE (MIT) file for you?