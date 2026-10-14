
def search_tickets(
    tickets,
    title="",
    category="",
    status="",
    priority=""
):
    """Return tickets matching all supplied search filters."""

    matching_tickets = []

    title = title.strip().lower()
    category = category.strip().lower()
    status = status.strip().lower()
    priority = priority.strip().lower()

    for ticket in tickets:
        if title and title not in ticket["title"].lower():
            continue

        if category and category != ticket["category"].lower():
            continue

        if status and status != ticket["status"].lower():
            continue

        if priority and priority != ticket["priority"].lower():
            continue

        matching_tickets.append(ticket)

    return matching_tickets
