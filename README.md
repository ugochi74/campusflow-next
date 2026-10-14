# CampusFlow

CampusFlow is a simple Python program that helps a school manage IT problems. For example, students can report Wi-Fi or computer problems, and staff can track them until they are solved.

We built CampusFlow as a two-person Python project. It runs in the terminal and saves tickets in a JSON file. It does not need extra Python packages.

## What the program can do

- Create a new support ticket.
- Give each ticket an ID, such as `T001`.
- Set a priority: critical, high, medium, or low.
- Show all tickets or find one ticket.
- Assign a ticket to a staff member.
- Change a ticket from `open` to `in_progress` to `resolved`.
- Reopen a resolved ticket.
- Show open tickets in priority order.
- Show a report of ticket numbers and statuses.
- Save and load tickets using JSON.

## How to run it

You need Python 3 installed.

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run:

```bash
python3 main.py
```

Choose an option from the menu and follow the instructions.

## How to run the tests

From the project folder, run:

```bash
python3 -m unittest discover -s tests -v
```

The tests help us check that ticket creation, workflow, and storage work as expected.

## Project files

- `main.py` — starts the program and shows the menu.
- `campusflow/tickets.py` — creates tickets and calculates priority.
- `campusflow/workflow.py` — handles assignments, status changes, and the queue.
- `campusflow/storage.py` — saves and loads tickets.
- `campusflow/reports.py` — counts tickets for reports.
- `tests/` — contains our tests.
- `docs/` — contains project notes.

## Team members

**Engineer A:** Ticket creation, validation, priority calculation, and JSON storage.

**Engineer B:** Ticket assignment, status changes, work queue, and reporting.

We both helped with testing and reviewing the code.