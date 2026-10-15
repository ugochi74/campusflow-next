
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from campusflow.storage import load_tickets, save_tickets


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        self.filename = str(
            Path(self.temp_dir.name) / "tickets.json"
        )

        self.tickets = [
            {
                "id": "T001",
                "title": "Wi-Fi not working",
                "category": "Network",
                "urgency": "high",
                "affected_users": 15,
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
                "notes": [],
            }
        ]

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_missing_file_returns_empty_list(self):
        self.assertEqual(load_tickets(self.filename), [])

    def test_save_and_load_tickets(self):
        save_tickets(self.tickets, self.filename)

        result = load_tickets(self.filename)

        self.assertEqual(result, self.tickets)
    def test_save_and_load_preserves_notes(self):
        self.tickets[0]["notes"] = [
            {
                "note_id": "N001",
                "author": "Engineer A",
                "message": "Investigating the Wi-Fi issue",
            }
        ]

        save_tickets(self.tickets, self.filename)
        result = load_tickets(self.filename)

        self.assertEqual(result[0]["notes"], self.tickets[0]["notes"])

    def test_legacy_ticket_without_notes_loads_with_empty_notes(self):
        legacy_ticket = self.tickets[0].copy()
        del legacy_ticket["notes"]

        Path(self.filename).write_text(
            json.dumps([legacy_ticket]),
            encoding="utf-8",
        )

        result = load_tickets(self.filename)

        self.assertEqual(result[0]["notes"], [])

    def test_invalid_json_raises_error(self):
        Path(self.filename).write_text(
            "{invalid json",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "Invalid JSON"):
            load_tickets(self.filename)

    def test_non_list_json_raises_error(self):
        Path(self.filename).write_text(
            json.dumps({"id": "T001"}),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "expected a list"):
            load_tickets(self.filename)

    def test_duplicate_ticket_ids_raise_error(self):
        duplicate_tickets = [
            self.tickets[0],
            self.tickets[0].copy(),
        ]

        Path(self.filename).write_text(
            json.dumps(duplicate_tickets),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "Duplicate ticket ID"):
            load_tickets(self.filename)

    def test_invalid_ticket_structure_raises_error(self):
        Path(self.filename).write_text(
            json.dumps([{"id": "T001"}]),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "incorrect ticket fields"):
            load_tickets(self.filename)

    def test_non_dictionary_ticket_is_rejected(self):
        Path(self.filename).write_text(
            json.dumps(["not a ticket"]),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "must be a dictionary"):
            load_tickets(self.filename)

    def test_invalid_ticket_id_is_rejected(self):
        invalid_ticket = self.tickets[0].copy()
        invalid_ticket["id"] = ""

        Path(self.filename).write_text(
            json.dumps([invalid_ticket]),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "Invalid ticket ID"):
            load_tickets(self.filename)

    def test_invalid_status_is_rejected(self):
        invalid_ticket = self.tickets[0].copy()
        invalid_ticket["status"] = "completed"

        Path(self.filename).write_text(
            json.dumps([invalid_ticket]),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "Invalid status"):
            load_tickets(self.filename)

    def test_non_string_status_is_rejected(self):
        invalid_ticket = self.tickets[0].copy()
        invalid_ticket["status"] = ["open"]

        Path(self.filename).write_text(
            json.dumps([invalid_ticket]),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "Invalid status"):
            load_tickets(self.filename)

    def test_invalid_priority_is_rejected(self):
        invalid_ticket = self.tickets[0].copy()
        invalid_ticket["priority"] = "urgent"

        Path(self.filename).write_text(
            json.dumps([invalid_ticket]),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "Invalid priority"):
            load_tickets(self.filename)

    def test_non_string_priority_is_rejected(self):
        invalid_ticket = self.tickets[0].copy()
        invalid_ticket["priority"] = ["high"]

        Path(self.filename).write_text(
            json.dumps([invalid_ticket]),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "Invalid priority"):
            load_tickets(self.filename)

    def test_invalid_title_is_rejected(self):
        invalid_ticket = self.tickets[0].copy()
        invalid_ticket["title"] = "   "

        Path(self.filename).write_text(
            json.dumps([invalid_ticket]),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "Invalid title"):
            load_tickets(self.filename)

    def test_non_string_title_is_rejected(self):
        invalid_ticket = self.tickets[0].copy()
        invalid_ticket["title"] = 123

        Path(self.filename).write_text(
            json.dumps([invalid_ticket]),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "Invalid title"):
            load_tickets(self.filename)

    def test_invalid_category_is_rejected(self):
        invalid_ticket = self.tickets[0].copy()
        invalid_ticket["category"] = "Finance"

        Path(self.filename).write_text(
            json.dumps([invalid_ticket]),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "Invalid category"):
            load_tickets(self.filename)

    def test_invalid_urgency_is_rejected(self):
        invalid_ticket = self.tickets[0].copy()
        invalid_ticket["urgency"] = "urgent"

        Path(self.filename).write_text(
            json.dumps([invalid_ticket]),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "Invalid urgency"):
            load_tickets(self.filename)

    def test_invalid_affected_users_is_rejected(self):
        invalid_ticket = self.tickets[0].copy()
        invalid_ticket["affected_users"] = -2

        Path(self.filename).write_text(
            json.dumps([invalid_ticket]),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "Invalid affected users"):
            load_tickets(self.filename)

    def test_boolean_affected_users_is_rejected(self):
        invalid_ticket = self.tickets[0].copy()
        invalid_ticket["affected_users"] = True

        Path(self.filename).write_text(
            json.dumps([invalid_ticket]),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "Invalid affected users"):
            load_tickets(self.filename)

    def test_non_integer_affected_users_is_rejected(self):
        invalid_ticket = self.tickets[0].copy()
        invalid_ticket["affected_users"] = "15"

        Path(self.filename).write_text(
            json.dumps([invalid_ticket]),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "Invalid affected users"):
            load_tickets(self.filename)

    def test_invalid_assignee_is_rejected(self):
        invalid_ticket = self.tickets[0].copy()
        invalid_ticket["assigned_to"] = "   "

        Path(self.filename).write_text(
            json.dumps([invalid_ticket]),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "Invalid assignee"):
            load_tickets(self.filename)

    def test_non_string_assignee_is_rejected(self):
        invalid_ticket = self.tickets[0].copy()
        invalid_ticket["assigned_to"] = 123

        Path(self.filename).write_text(
            json.dumps([invalid_ticket]),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "Invalid assignee"):
            load_tickets(self.filename)

    def test_failed_save_preserves_existing_file(self):
        original_content = json.dumps(self.tickets, indent=4)

        Path(self.filename).write_text(
            original_content,
            encoding="utf-8",
        )

        with patch(
            "campusflow.storage.json.dump",
            side_effect=OSError("Simulated write failure"),
        ):
            with self.assertRaises(OSError):
                save_tickets(self.tickets, self.filename)

        saved_content = Path(self.filename).read_text(
            encoding="utf-8",
        )

        self.assertEqual(saved_content, original_content)

    def test_failed_save_removes_temporary_file(self):
        with patch(
            "campusflow.storage.json.dump",
            side_effect=OSError("Simulated write failure"),
        ):
            with self.assertRaises(OSError):
                save_tickets(self.tickets, self.filename)

        remaining_files = list(Path(self.filename).parent.iterdir())

        self.assertEqual(remaining_files, [])


if __name__ == "__main__":
    unittest.main()
