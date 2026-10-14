import unittest

from campusflow.reports import generate_report


class TestGenerateReport(unittest.TestCase):

    def setUp(self):
        # Sample tickets used for testing
        self.tickets = [
            {
                "id": "T001",
                "status": "open",
                "priority": "critical"
            },
            {
                "id": "T002",
                "status": "in_progress",
                "priority": "high"
            },
            {
                "id": "T003",
                "status": "resolved",
                "priority": "medium"
            },
            {
                "id": "T004",
                "status": "open",
                "priority": "low"
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

        self.assertEqual(
            report["by_status"],
            {
                "open": 0,
                "in_progress": 0,
                "resolved": 0
            }
        )

        self.assertEqual(
            report["by_priority"],
            {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0
            }
        )


if __name__ == "__main__":
    unittest.main()