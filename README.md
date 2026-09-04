# Project Manager

Project Manager is a lightweight desktop project-management application built
with Python and CustomTkinter. It organizes work into projects, tasks, and
subtasks, stores data locally, and provides automations for deadline and status
events.

## Features

- Create, edit, and delete projects, tasks, and subtasks.
- Organize tasks and subtasks under their parent objects.
- Track item names, descriptions, statuses, and deadlines.
- Select deadlines with a calendar and editable `HH:MM` time field.
- Add automation controls to projects, tasks, and subtasks.
- Configure multiple triggers for an automation:
  - **Status**: run when an item has a selected status.
  - **Deadline**: run when a selected date and time is reached.
- Configure actions that:
  - Change an item status.
  - Write a timestamped log file.
  - Send an email through SMTP.
- Evaluate newly created automations immediately.
- Run deadline automations in a background polling thread.
- Persist changes to a local Pickle database.
- Customize the application appearance with the included themes.

## Requirements

- Windows, macOS, or Linux
- Python 3.10 or newer
- `customtkinter`
- `Pillow`
- `python-dotenv` (required for email configuration)

## Installation

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/anthonycradockwatson/project-manager.git
cd project-manager
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS/Linux
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Running the application

Start the desktop application from the repository root:

```bash
python main.py
```

The application starts the automation polling thread and then opens the main
project window. Keep the process running for deadline automations to be
evaluated.

## Using the application

### Projects, tasks, and subtasks

1. Start the application and create a project.
2. Open a project to add tasks.
3. Add subtasks from the task list.
4. Use edit mode to change an item's name, description, status, or deadline.
5. Use the refresh controls after making changes in another window.

Deleting a project also deletes its tasks and subtasks. Deleting a task removes
its subtasks and updates the parent project's stored relationships.

### Deadlines

The deadline picker provides:

- A calendar for selecting the date.
- An `HH:MM` input for selecting the time.
- A **Clear** button for removing a deadline.

Deadlines are stored as Python `datetime` values. Empty deadlines are stored as
`None`, and deadlines must be in the future when assigned.

## Automations

Open the workflow button beside a project, task, or subtask to view its
automations. Create an automation by providing a name, one or more triggers,
and an action.

When a new automation is saved, its status and deadline triggers are checked
immediately. Deadline triggers are also checked by the background worker every
five seconds while `main.py` is running.

Automations are one-shot: after a trigger fires, the action runs and the
automation is removed from the item. The updated item is then saved.

### Actions

#### Status

Sets the associated item's status to the selected value. Status values currently
used by the interface are:

- `Not Started`
- `In Progress`
- `Completed`

#### Log

Writes a timestamped log entry to the `logs` directory. Log files are generated
when the action executes.

#### Email

Sends an email using SMTP. Configure the SMTP connection in a `.env` file in
the repository root:

```dotenv
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your-user
SMTP_PASSWORD=your-password
```

The sender address, recipient address, subject, and message are configured on
the automation itself. Do not commit `.env` or real credentials to source
control.

## Project architecture

The application is intentionally split into layers:

```text
GUI -> View models -> Manager -> ObjectStore
```

- `gui/`: CustomTkinter windows, widgets, and view models.
  - `gui/main/`: main project list.
  - `gui/project/`: project, task, and subtask views and editing.
  - `gui/automations/`: automation list and editing windows.
  - `gui/shared/`: reusable widgets and base view-model behavior.
- `classes.py`: domain objects (`Project`, `Task`, `SubTask`, and `Item`).
- `automations.py`: automation, trigger, and action domain classes.
- `manager.py`: application-level operations and persistence façade.
- `db_function.py`: Pickle-backed `ObjectStore`.
- `main.py`: application entry point and deadline polling worker.
- `assets/`: themes and image assets used by the interface.
- `data/UserProjects.pkl`: default local data file created and updated by the
  application.

The Manager keeps storage access out of the GUI and domain objects. The object
store saves the complete object graph to the Pickle file whenever an object is
added, updated, or deleted.

## Data and backups

Data is stored locally in `data/UserProjects.pkl`. Pickle files can execute
code when loaded, so only open data files from trusted sources. Back up the
data file before making manual changes or experimenting with incompatible code
changes.

The `logs/` directory contains log-action output and can be safely archived or
cleared when the application is not writing to it.

## Development

Run commands from the repository root with the virtual environment activated.
Dependencies are listed in `requirements.txt`; the project currently has no
dedicated test suite or dependency lock file.
Before submitting changes:

1. Check Python syntax for modified modules.
2. Run the application and exercise the affected UI flow.
3. Verify that changes remain after restarting the application.
4. Avoid committing `.env`, Pickle data, generated logs, or virtual-environment
   files.

## Contributing

Open an issue to describe a bug or proposed feature before making substantial
changes. Pull requests should explain the behavior changed and include focused
validation steps.

## License

No license file is currently included. Until a license is added, the repository
should be treated as source-available rather than freely redistributable.
