
import unittest

from campusflow.reports import generate_report


class TestGenerateReport(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "status": "open",
                "priority": "critical",
                "category": "Network"
            },
            {
                "id": "T002",
                "status": "in_progress",
                "priority": "high",
                "category": "Hardware"
            },
            {
                "id": "T003",
                "status": "resolved",
                "priority": "medium",
                "category": "Software"
            },
            {
                "id": "T004",
                "status": "open",
                "priority": "low",
                "category": "Network"
            }
        ]

    def test_total_tickets(self):
        report = generate_report(self.tickets)
        self.assertEqual(report["total"], 4)

    def test_tickets_by_status(self):
        report = generate_report(self.tickets)
        self.assertEqual(report["by_status"]["open"], 2)
        self.assertEqual(report["by_status"]["in_progress"], 1)
        self.assertEqual(report["by_status"]["resolved"], 1)

    def test_tickets_by_priority(self):
        report = generate_report(self.tickets)
        self.assertEqual(report["by_priority"]["critical"], 1)
        self.assertEqual(report["by_priority"]["high"], 1)
        self.assertEqual(report["by_priority"]["medium"], 1)
        self.assertEqual(report["by_priority"]["low"], 1)

    def test_empty_ticket_list(self):
        report = generate_report([])
        self.assertEqual(report["total"], 0)
        self.assertEqual(report["by_status"]["open"], 0)
        self.assertEqual(report["by_status"]["in_progress"], 0)
        self.assertEqual(report["by_status"]["resolved"], 0)
        self.assertEqual(report["unresolved"], 0)
        self.assertEqual(report["resolved"], 0)
        self.assertEqual(report["resolution_percentage"], 0)

    def test_tickets_by_category(self):
        report = generate_report(self.tickets)
        self.assertEqual(report["by_category"]["Network"], 2)
        self.assertEqual(report["by_category"]["Hardware"], 1)
        self.assertEqual(report["by_category"]["Software"], 1)
        self.assertEqual(report["by_category"]["Other"], 0)

    def test_resolved_and_unresolved_tickets(self):
        report = generate_report(self.tickets)
        self.assertEqual(report["resolved"], 1)
        self.assertEqual(report["unresolved"], 3)

    def test_resolution_percentage(self):
        report = generate_report(self.tickets)
        self.assertEqual(report["resolution_percentage"], 25.0)


if __name__ == "__main__":
    unittest.main()
