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


def assign_ticket(tickets, ticket_id, staff_name):
    ticket = view_ticket(tickets, ticket_id)

    if ticket is None:
        return "Ticket not found."

    if ticket["status"] == "resolved":
        return "Cannot assign a resolved ticket. Reopen it first."

    if not isinstance(staff_name, str) or not staff_name.strip():
        return "Staff name cannot be empty."

    ticket["assigned_to"] = staff_name.strip()

    return "Ticket assigned successfully."


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
        return "Ticket is now in progress."

    if current_status == "in_progress" and new_status == "resolved":
        ticket["status"] = "resolved"
        return "Ticket resolved successfully."

    return "Invalid status transition."


def reopen_ticket(tickets, ticket_id):
    ticket = view_ticket(tickets, ticket_id)

    if ticket is None:
        return "Ticket not found."

    if ticket["status"] != "resolved":
        return "Only resolved tickets can be reopened."

    ticket["status"] = "open"

    return "Ticket reopened successfully."


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