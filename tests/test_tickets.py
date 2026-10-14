
import unittest
from campusflow.tickets import calculate_priority, validate_ticket_input, generate_ticket_id, create_ticket

class TestCalculatePriority(unittest.TestCase):

    def test_high_urgency_and_many_users_is_critical(self):
        self.assertEqual(calculate_priority("high", 12), "critical")

    def test_high_urgency_alone_is_high(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_many_users_alone_is_high(self):
        self.assertEqual(calculate_priority("low", 10), "high")

    def test_medium_urgency_is_medium(self):
        self.assertEqual(calculate_priority("medium", 1), "medium")

    def test_three_users_is_medium(self):
        self.assertEqual(calculate_priority("low", 3), "medium")

    def test_low_urgency_and_few_users_is_low(self):
        self.assertEqual(calculate_priority("low", 1), "low")




class TestValidateTicketInput(unittest.TestCase):

    def test_valid_input_is_normalized(self):
        result = validate_ticket_input(
            "  Wi-Fi is down  ", "NETWORK", "HIGH", 5
        )
        self.assertEqual(result, ("Wi-Fi is down", "Network", "high", 5))

    def test_blank_title_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_ticket_input("   ", "Network", "high", 5)

    def test_invalid_category_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_ticket_input("Wi-Fi is down", "Food", "high", 5)

    def test_invalid_urgency_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_ticket_input("Wi-Fi is down", "Network", "urgent", 5)

    def test_zero_affected_users_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_ticket_input("Wi-Fi is down", "Network", "high", 0)

    def test_decimal_affected_users_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_ticket_input("Wi-Fi is down", "Network", "high", 2.5)




class TestGenerateTicketId(unittest.TestCase):

    def test_generates_next_ticket_id(self):
        existing_tickets = [
            {"id": "T001"},
            {"id": "T002"},
            {"id": "T005"},
        ]

        result = generate_ticket_id(existing_tickets)

        self.assertEqual(result, "T006")

    def test_first_ticket_id_when_list_is_empty(self):
        existing_tickets = []

        result = generate_ticket_id(existing_tickets)

        self.assertEqual(result, "T001")

    def test_ignores_invalid_ticket_ids(self):
        existing_tickets = [
            {"id": "T002"},
            {"id": "INVALID"},
            {"id": "T005"},
        ]

        result = generate_ticket_id(existing_tickets)

        self.assertEqual(result, "T006")





class TestCreateTicket(unittest.TestCase):   
    def test_create_ticket_successfully(self):
        existing_tickets = [
            {"id": "T001"},
            {"id": "T002"}
        ]

        ticket = create_ticket(
            "Wi-Fi is down",
            "NETWORK",
            "HIGH",
            12,
            existing_tickets
        )

        self.assertEqual(ticket["id"], "T003")
        self.assertEqual(ticket["title"], "Wi-Fi is down")
        self.assertEqual(ticket["category"], "Network")
        self.assertEqual(ticket["urgency"], "high")
        self.assertEqual(ticket["affected_users"], 12)
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])


    def test_create_ticket_rejects_blank_title(self):
        existing_tickets = []

        with self.assertRaises(ValueError):
            create_ticket(
                "",
                "Network",
                "high",
                12,
                existing_tickets
            )

if __name__ == "__main__":
    unittest.main()



