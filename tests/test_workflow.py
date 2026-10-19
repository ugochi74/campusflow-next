import unittest

from campusflow.workflow import (
    view_ticket,
    add_note,
    assign_ticket,
    update_ticket_status,
    reopen_ticket,
    get_work_queue,
)


class TestViewTicket(unittest.TestCase):

    def test_existing_ticket(self):
        tickets = [
            {"id": "T001", "title": "Wi-Fi problem"},
            {"id": "T002", "title": "Broken keyboard"},
        ]

        result = view_ticket(tickets, "T002")

        self.assertEqual(result["title"], "Broken keyboard")

    def test_nonexistent_ticket(self):
        tickets = [
            {"id": "T001", "title": "Wi-Fi problem"}
        ]

        result = view_ticket(tickets, "T009")

        self.assertIsNone(result)

    def test_empty_ticket_list(self):
        result = view_ticket([], "T001")

        self.assertIsNone(result)


class TestAssignTicket(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "status": "open",
                "assigned_to": None,
            },
            {
                "id": "T002",
                "status": "resolved",
                "assigned_to": "Mary",
            },
        ]

    def test_successful_assignment(self):
        result = assign_ticket(self.tickets, "T001", "David")

        self.assertEqual(
            result,
            "Ticket T001 assigned successfully."
        )
        self.assertEqual(self.tickets[0]["assigned_to"], "David")

    def test_unknown_ticket(self):
        result = assign_ticket(self.tickets, "T009", "John")

        self.assertEqual(result, "Ticket not found.")
        self.assertIsNone(self.tickets[0]["assigned_to"])

    def test_empty_staff_name(self):
        result = assign_ticket(self.tickets, "T001", "   ")

        self.assertEqual(result, "Staff name cannot be empty.")
        self.assertIsNone(self.tickets[0]["assigned_to"])

    def test_resolved_ticket(self):
        result = assign_ticket(self.tickets, "T002", "Peter")

        self.assertEqual(
            result,
            "Cannot assign a resolved ticket. Reopen it first."
        )
        self.assertEqual(self.tickets[1]["assigned_to"], "Mary")


class TestTicketLifecycle(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "status": "open",
                "assigned_to": None,
            }
        ]

    def test_cannot_start_unassigned_ticket(self):
        result = update_ticket_status(
            self.tickets, "T001", "in_progress"
        )

        self.assertEqual(
            result,
            "Assign the ticket before starting work."
        )
        self.assertEqual(self.tickets[0]["status"], "open")

    def test_start_assigned_ticket(self):
        self.tickets[0]["assigned_to"] = "Sarah"

        result = update_ticket_status(
            self.tickets, "T001", "in_progress"
        )

        self.assertEqual(
            result,
            "Ticket T001 is now in progress."
        )
        self.assertEqual(self.tickets[0]["status"], "in_progress")

    def test_resolve_ticket(self):
        self.tickets[0]["status"] = "in_progress"

        result = update_ticket_status(
            self.tickets, "T001", "resolved"
        )

        self.assertEqual(
            result,
            "Ticket T001 resolved successfully."
        )
        self.assertEqual(self.tickets[0]["status"], "resolved")

    def test_cannot_skip_to_resolved(self):
        result = update_ticket_status(
            self.tickets, "T001", "resolved"
        )

        self.assertEqual(result, "Invalid status transition.")
        self.assertEqual(self.tickets[0]["status"], "open")

    def test_reopen_resolved_ticket(self):
        self.tickets[0]["status"] = "resolved"

        result = reopen_ticket(self.tickets, "T001")

        self.assertEqual(
            result,
            "Ticket T001 reopened successfully."
        )
        self.assertEqual(self.tickets[0]["status"], "open")

    def test_cannot_reopen_open_ticket(self):
        result = reopen_ticket(self.tickets, "T001")

        self.assertEqual(
            result,
            "Only resolved tickets can be reopened."
        )
        self.assertEqual(self.tickets[0]["status"], "open")

    def test_unknown_ticket(self):
        result = update_ticket_status(
            self.tickets, "T999", "in_progress"
        )

        self.assertEqual(result, "Ticket not found.")


class TestWorkQueue(unittest.TestCase):

    def test_priority_order(self):
        tickets = [
            {"id": "T001", "priority": "low", "status": "open"},
            {"id": "T002", "priority": "critical", "status": "open"},
            {"id": "T003", "priority": "high", "status": "open"},
            {"id": "T004", "priority": "medium", "status": "open"},
        ]

        queue = get_work_queue(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T002", "T003", "T004", "T001"],
        )

    def test_excludes_non_open_tickets(self):
        tickets = [
            {"id": "T001", "priority": "critical", "status": "resolved"},
            {"id": "T002", "priority": "high", "status": "in_progress"},
            {"id": "T003", "priority": "low", "status": "open"},
        ]

        queue = get_work_queue(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T003"],
        )

    def test_numeric_id_order(self):
        tickets = [
            {"id": "T010", "priority": "high", "status": "open"},
            {"id": "T002", "priority": "high", "status": "open"},
        ]

        queue = get_work_queue(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T002", "T010"],
        )

    def test_empty_queue(self):
        self.assertEqual(get_work_queue([]), [])


class TestAddNote(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "status": "open",
                "assigned_to": "David",
                "notes": [],
            }
        ]

    def test_add_note_successfully(self):
        result = add_note(
            self.tickets,
            "T001",
            "Engineer A",
            "Investigating the Wi-Fi issue",
        )

        self.assertEqual(result, "Note N001 added successfully.")
        self.assertEqual(
            self.tickets[0]["notes"],
            [
                {
                    "note_id": "N001",
                    "author": "Engineer A",
                    "message": "Investigating the Wi-Fi issue",
                }
            ],
        )

    def test_cannot_add_note_to_resolved_ticket(self):
        self.tickets[0]["status"] = "resolved"

        result = add_note(
            self.tickets,
            "T001",
            "Engineer A",
            "Investigating the Wi-Fi issue",
        )

        self.assertEqual(
            result,
            "Cannot add notes to a resolved ticket. Reopen it first.",
        )
        self.assertEqual(self.tickets[0]["notes"], [])

    def test_rejects_short_message_without_mutation(self):
        result = add_note(
            self.tickets, "T001", "Engineer A", "bad"
        )

        self.assertEqual(
            result,
            "Note message must be between 5 and 300 characters.",
        )
        self.assertEqual(self.tickets[0]["notes"], [])

    def test_rejects_empty_author_without_mutation(self):
        result = add_note(
            self.tickets,
            "T001",
            "   ",
            "Investigating the Wi-Fi issue",
        )

        self.assertEqual(result, "Note author cannot be empty.")
        self.assertEqual(self.tickets[0]["notes"], [])

    def test_note_ids_increment(self):
        add_note(
            self.tickets,
            "T001",
            "Engineer A",
            "Investigating the Wi-Fi issue",
        )

        result = add_note(
            self.tickets,
            "T001",
            "Engineer B",
            "Testing the network connection",
        )

        self.assertEqual(result, "Note N002 added successfully.")
        self.assertEqual(
            [note["note_id"] for note in self.tickets[0]["notes"]],
            ["N001", "N002"],
        )


if __name__ == "__main__":
    unittest.main()
