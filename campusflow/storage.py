
import json
import os
import tempfile
from pathlib import Path


VALID_STATUSES = {"open", "in_progress", "resolved"}
VALID_PRIORITIES = {"critical", "high", "medium", "low"}
VALID_CATEGORIES = {"Network", "Hardware", "Software", "Other"}
VALID_URGENCIES = {"low", "medium", "high"}

REQUIRED_TICKET_FIELDS = {
    "id",
    "title",
    "category",
    "urgency",
    "affected_users",
    "priority",
    "status",
    "assigned_to",
    "notes",
}

LEGACY_TICKET_FIELDS = REQUIRED_TICKET_FIELDS - {"notes"}
REQUIRED_NOTE_FIELDS = {"note_id", "author", "message"}


def _validate_note(note, ticket_id, seen_note_ids):
    """Validate one note without modifying it."""

    if not isinstance(note, dict):
        raise ValueError(
            f"Invalid note for ticket {ticket_id}: "
            "each note must be a dictionary."
        )

    if set(note) != REQUIRED_NOTE_FIELDS:
        raise ValueError(
            f"Invalid note fields for ticket {ticket_id}."
        )

    note_id = note["note_id"]

    if (
        not isinstance(note_id, str)
        or len(note_id) < 2
        or note_id[0] != "N"
        or not note_id[1:].isdigit()
        or int(note_id[1:]) < 1
    ):
        raise ValueError(
            f"Invalid note ID for ticket {ticket_id}."
        )

    if note_id in seen_note_ids:
        raise ValueError(
            f"Duplicate note ID {note_id} for ticket {ticket_id}."
        )

    seen_note_ids.add(note_id)

    author = note["author"]
    if not isinstance(author, str) or not author.strip():
        raise ValueError(
            f"Invalid note author for ticket {ticket_id}."
        )

    message = note["message"]
    if (
        not isinstance(message, str)
        or not 5 <= len(message.strip()) <= 300
    ):
        raise ValueError(
            f"Invalid note message for ticket {ticket_id}: "
            "must be 5–300 characters."
        )


def _validate_ticket(ticket, seen_ticket_ids):
    """Validate a ticket and normalize a legacy missing notes field."""

    if not isinstance(ticket, dict):
        raise ValueError(
            "Invalid ticket data: every ticket must be a dictionary."
        )

    fields = set(ticket)

    # Accept older tickets without notes and migrate them in memory.
    if fields == LEGACY_TICKET_FIELDS:
        ticket["notes"] = []
    elif fields != REQUIRED_TICKET_FIELDS:
        raise ValueError(
            "Invalid ticket data: incorrect ticket fields."
        )

    ticket_id = ticket["id"]

    if (
        not isinstance(ticket_id, str)
        or not ticket_id.strip()
        or not ticket_id.startswith("T")
        or not ticket_id[1:].isdigit()
        or int(ticket_id[1:]) < 1
    ):
        raise ValueError("Invalid ticket ID.")

    if ticket_id in seen_ticket_ids:
        raise ValueError(f"Duplicate ticket ID found: {ticket_id}")

    seen_ticket_ids.add(ticket_id)

    title = ticket["title"]
    if not isinstance(title, str) or not title.strip():
        raise ValueError(f"Invalid title for ticket {ticket_id}.")

    category = ticket["category"]
    if not isinstance(category, str) or category not in VALID_CATEGORIES:
        raise ValueError(f"Invalid category for ticket {ticket_id}.")

    urgency = ticket["urgency"]
    if not isinstance(urgency, str) or urgency not in VALID_URGENCIES:
        raise ValueError(f"Invalid urgency for ticket {ticket_id}.")

    affected_users = ticket["affected_users"]
    if (
        isinstance(affected_users, bool)
        or not isinstance(affected_users, int)
        or affected_users <= 0
    ):
        raise ValueError(
            f"Invalid affected users for ticket {ticket_id}."
        )

    priority = ticket["priority"]
    if not isinstance(priority, str) or priority not in VALID_PRIORITIES:
        raise ValueError(
            f"Invalid priority for ticket {ticket_id}: {priority}"
        )

    # Confirm priority agrees with the existing business rules.
    if urgency == "high" and affected_users >= 10:
        expected_priority = "critical"
    elif urgency == "high" or affected_users >= 10:
        expected_priority = "high"
    elif urgency == "medium" or affected_users >= 3:
        expected_priority = "medium"
    else:
        expected_priority = "low"

    if priority != expected_priority:
        raise ValueError(
            f"Inconsistent priority for ticket {ticket_id}: "
            f"expected {expected_priority}, got {priority}."
        )

    status = ticket["status"]
    if not isinstance(status, str) or status not in VALID_STATUSES:
        raise ValueError(f"Invalid status for ticket {ticket_id}: {status}")

    assigned_to = ticket["assigned_to"]
    if assigned_to is not None and (
        not isinstance(assigned_to, str) or not assigned_to.strip()
    ):
        raise ValueError(f"Invalid assignee for ticket {ticket_id}.")

    notes = ticket["notes"]
    if not isinstance(notes, list):
        raise ValueError(
            f"Invalid notes for ticket {ticket_id}: expected a list."
        )

    seen_note_ids = set()
    for note in notes:
        _validate_note(note, ticket_id, seen_note_ids)


def load_tickets(filename="tickets.json"):
    """Load and validate all tickets before returning the collection."""

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

    # Validate the entire collection before returning it.
    # Work on copies so validation failures do not partially migrate
    # the original parsed ticket dictionaries.
    validated_tickets = []
    seen_ticket_ids = set()

    for original_ticket in tickets:
        if not isinstance(original_ticket, dict):
            raise ValueError(
                "Invalid ticket data: every ticket must be a dictionary."
            )

        ticket = original_ticket.copy()
        if "notes" not in ticket and set(ticket) == LEGACY_TICKET_FIELDS:
            ticket["notes"] = []

        _validate_ticket(ticket, seen_ticket_ids)
        validated_tickets.append(ticket)

    return validated_tickets


def save_tickets(tickets, filename="tickets.json"):
    """Validate and safely save tickets using an atomic file replacement."""

    if not isinstance(tickets, list):
        raise ValueError("Invalid ticket data: expected a list.")

    # Validate copies so saving cannot partially mutate caller data.
    validated_tickets = []
    seen_ticket_ids = set()

    for original_ticket in tickets:
        if not isinstance(original_ticket, dict):
            raise ValueError(
                "Invalid ticket data: every ticket must be a dictionary."
            )

        ticket = original_ticket.copy()
        if "notes" not in ticket and set(ticket) == LEGACY_TICKET_FIELDS:
            ticket["notes"] = []

        _validate_ticket(ticket, seen_ticket_ids)
        validated_tickets.append(ticket)

    filepath = Path(filename)
    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=filepath.parent,
            prefix=f".{filepath.name}.",
            suffix=".tmp",
            delete=False,
        ) as file:
            temporary_path = Path(file.name)
            json.dump(validated_tickets, file, indent=4)
            file.flush()
            os.fsync(file.fileno())

        os.replace(temporary_path, filepath)

    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()
