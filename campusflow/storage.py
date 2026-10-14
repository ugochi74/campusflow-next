
import json
import os
import tempfile
from pathlib import Path


VALID_STATUSES = {"open", "in_progress", "resolved"}
VALID_PRIORITIES = {"critical", "high", "medium", "low"}
VALID_CATEGORIES = {"Network", "Hardware", "Software", "Other"}
VALID_URGENCIES = {"low", "medium", "high"}


def load_tickets(filename="tickets.json"):
    """Load tickets from a JSON file and validate their data."""

    filepath = Path(filename)

    if not filepath.exists():
        return []

    try:
        with filepath.open("r", encoding="utf-8") as file:
            tickets = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in {filename}: {error}"
        ) from error

    if not isinstance(tickets, list):
        raise ValueError("Invalid ticket data: expected a list.")

    required_fields = {
        "id",
        "title",
        "category",
        "urgency",
        "affected_users",
        "priority",
        "status",
        "assigned_to",
    }

    seen_ids = set()

    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise ValueError(
                "Invalid ticket data: every ticket must be a dictionary."
            )

        if set(ticket.keys()) != required_fields:
            raise ValueError(
                "Invalid ticket data: incorrect ticket fields."
            )

        ticket_id = ticket["id"]

        if not isinstance(ticket_id, str) or not ticket_id.strip():
            raise ValueError("Invalid ticket ID.")

        if ticket_id in seen_ids:
            raise ValueError(
                f"Duplicate ticket ID found: {ticket_id}"
            )

        seen_ids.add(ticket_id)

        # Validate title.
        title = ticket["title"]

        if not isinstance(title, str) or not title.strip():
            raise ValueError(
                f"Invalid title for ticket {ticket_id}."
            )

        # Validate category.
        category = ticket["category"]

        if (
            not isinstance(category, str)
            or category not in VALID_CATEGORIES
        ):
            raise ValueError(
                f"Invalid category for ticket {ticket_id}."
            )

        # Validate urgency.
        urgency = ticket["urgency"]

        if (
            not isinstance(urgency, str)
            or urgency not in VALID_URGENCIES
        ):
            raise ValueError(
                f"Invalid urgency for ticket {ticket_id}."
            )

        # Validate affected users.
        affected_users = ticket["affected_users"]

        if (
            isinstance(affected_users, bool)
            or not isinstance(affected_users, int)
            or affected_users <= 0
        ):
            raise ValueError(
                f"Invalid affected users for ticket {ticket_id}."
            )

        # Validate priority.
        priority = ticket["priority"]

        if (
            not isinstance(priority, str)
            or priority not in VALID_PRIORITIES
        ):
            raise ValueError(
                f"Invalid priority for ticket {ticket_id}: {priority}"
            )

        # Validate status.
        status = ticket["status"]

        if (
            not isinstance(status, str)
            or status not in VALID_STATUSES
        ):
            raise ValueError(
                f"Invalid status for ticket {ticket_id}: {status}"
            )

        # Validate assigned user.
        assigned_to = ticket["assigned_to"]

        if assigned_to is not None and (
            not isinstance(assigned_to, str)
            or not assigned_to.strip()
        ):
            raise ValueError(
                f"Invalid assignee for ticket {ticket_id}."
            )

    return tickets


def save_tickets(tickets, filename="tickets.json"):
    """Save tickets safely using a temporary file."""

    filepath = Path(filename)
    temporary_path = None

    try:
        # Write to a temporary file in the same directory.
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=filepath.parent,
            prefix=f".{filepath.name}.",
            suffix=".tmp",
            delete=False,
        ) as file:
            temporary_path = Path(file.name)

            json.dump(tickets, file, indent=4)

            # Make sure the data is written before replacing the file.
            file.flush()
            os.fsync(file.fileno())

        # Replace the original file only after writing succeeds.
        os.replace(temporary_path, filepath)

    finally:
        # Remove the temporary file if saving fails.
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()
