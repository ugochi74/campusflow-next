
import unittest

from campusflow.search import search_tickets


class TestSearchTickets(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "title": "WiFi connection is down",
                "category": "Network",
                "priority": "critical",
                "status": "open",
                "assigned_to": None
            },
            {
                "id": "T002",
                "title": "Laptop screen is broken",
                "category": "Hardware",
                "priority": "high",
                "status": "in_progress",
                "assigned_to": "Ada"
            },
            {
                "id": "T003",
                "title": "WiFi is slow",
                "category": "Network",
                "priority": "medium",
                "status": "resolved",
                "assigned_to": "John"
            }
        ]

    def test_search_title_case_insensitive(self):
        results = search_tickets(self.tickets, title="WIFI")
        self.assertEqual(
            [ticket["id"] for ticket in results],
            ["T001", "T003"]
        )

    def test_filter_by_category(self):
        results = search_tickets(self.tickets, category="network")
        self.assertEqual(
            [ticket["id"] for ticket in results],
            ["T001", "T003"]
        )

    def test_filter_by_status(self):
        results = search_tickets(self.tickets, status="open")
        self.assertEqual(
            [ticket["id"] for ticket in results],
            ["T001"]
        )

    def test_filter_by_priority(self):
        results = search_tickets(self.tickets, priority="HIGH")
        self.assertEqual(
            [ticket["id"] for ticket in results],
            ["T002"]
        )

    def test_combined_filters(self):
        results = search_tickets(
            self.tickets,
            title="wifi",
            category="Network",
            status="open"
        )
        self.assertEqual(
            [ticket["id"] for ticket in results],
            ["T001"]
        )

    def test_empty_filters_return_all_tickets(self):
        results = search_tickets(self.tickets)
        self.assertEqual(len(results), 3)

    def test_no_matches_returns_empty_list(self):
        results = search_tickets(
            self.tickets,
            title="printer"
        )
        self.assertEqual(results, [])

    def test_search_does_not_modify_original_tickets(self):
        original_ids = [
            ticket["id"] for ticket in self.tickets
        ]

        search_tickets(self.tickets, category="Network")

        self.assertEqual(
            [ticket["id"] for ticket in self.tickets],
            original_ids
        )


if __name__ == "__main__":
    unittest.main()
