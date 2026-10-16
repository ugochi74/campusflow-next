def list_tickets(tickets):
    if not tickets:
        print("No tickets available.")
        return

    for ticket in tickets:
        print(
            f"ID: {ticket['id']} | "
            f"Title: {ticket['title']} | "
            f"Priority: {ticket['priority']} | "
            f"Status: {ticket['status']}"
        )


def view_ticket(tickets, ticket_id):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket

    return None


def add_note(tickets, ticket_id, author, message):
    """Add a validated note to an open or in-progress ticket."""

    ticket = view_ticket(tickets, ticket_id)

    if ticket is None:
        return "Ticket not found."

    if ticket["status"] not in {"open", "in_progress"}:
        return "Cannot add notes to a resolved ticket. Reopen it first."

    if not isinstance(author, str) or not author.strip():
        return "Note author cannot be empty."

    if not isinstance(message, str):
        return "Note message must be between 5 and 300 characters."

    message = message.strip()
    if not 5 <= len(message) <= 300:
        return "Note message must be between 5 and 300 characters."

    # Build the notes list if handling a legacy in-memory ticket.
    notes = ticket.get("notes")
    if notes is None:
        notes = []
    elif not isinstance(notes, list):
        return "Ticket notes are invalid."



    # Validate existing note IDs before choosing the next ID.
    note_numbers = []
    seen_note_ids = set()

    for note in notes:
        if not isinstance(note, dict):
            return "Ticket notes are invalid."

        note_id = note.get("note_id", "")
        if (
            not isinstance(note_id, str)
            or len(note_id) < 2
            or note_id[0] != "N"
            or not note_id[1:].isdigit()
            or int(note_id[1:]) < 1
            or note_id in seen_note_ids
        ):
            return "Ticket notes are invalid."

        seen_note_ids.add(note_id)
        note_numbers.append(int(note_id[1:]))
    next_number = max(note_numbers, default=0) + 1
    new_note = {
        "note_id": f"N{next_number:03d}",
        "author": author.strip(),
        "message": message,
    }

    # Mutate the ticket only after every validation has succeeded.
    if "notes" not in ticket or ticket["notes"] is None:
        ticket["notes"] = []

    ticket["notes"].append(new_note)

    return f"Note {new_note['note_id']} added successfully."


def assign_ticket(tickets, ticket_id, staff_name):
    ticket = view_ticket(tickets, ticket_id)

    if ticket is None:
        return "Ticket not found."

    if ticket["status"] == "resolved":
        return "Cannot assign a resolved ticket. Reopen it first."

    if not isinstance(staff_name, str) or not staff_name.strip():
        return "Staff name cannot be empty."

    ticket["assigned_to"] = staff_name.strip()

    return f"Ticket {ticket['id']} assigned successfully."


def update_ticket_status(tickets, ticket_id, new_status):
    ticket = view_ticket(tickets, ticket_id)

    if ticket is None:
        return "Ticket not found."

    current_status = ticket["status"]

    if current_status == "resolved":
        return "Resolved tickets must be reopened first."

    if current_status == "open" and new_status == "in_progress":
        if not ticket["assigned_to"]:
            return "Assign the ticket before starting work."

        ticket["status"] = "in_progress"
        return f"Ticket {ticket['id']} is now in progress."

    if current_status == "in_progress" and new_status == "resolved":
        ticket["status"] = "resolved"
        return f"Ticket {ticket['id']} resolved successfully."

    return "Invalid status transition."


def reopen_ticket(tickets, ticket_id):
    ticket = view_ticket(tickets, ticket_id)

    if ticket is None:
        return "Ticket not found."

    if ticket["status"] != "resolved":
        return "Only resolved tickets can be reopened."

    ticket["status"] = "open"

    return f"Ticket {ticket['id']} reopened successfully."


def get_work_queue(tickets):
    priority_order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3
    }

    open_tickets = [
        ticket for ticket in tickets
        if ticket["status"] == "open"
    ]

    sorted_tickets = sorted(
        open_tickets,
        key=lambda ticket: (
            priority_order[ticket["priority"]],
            int(ticket["id"][1:])
        )
    )

    return sorted_tickets
