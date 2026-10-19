
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from campusflow.knowledge_check import (
    QUESTIONS,
    get_valid_answer,
    run_knowledge_check,
)


class TestKnowledgeCheck(unittest.TestCase):

    def test_quiz_has_six_questions(self):
        self.assertEqual(len(QUESTIONS), 6)

    def test_valid_answer_is_returned(self):
        with patch("builtins.input", return_value="a"):
            answer = get_valid_answer()

        self.assertEqual(answer, "A")

    def test_invalid_answer_is_rejected(self):
        answers = iter(["X", "A"])
        messages = []

        answer = get_valid_answer(
            input_func=lambda _: next(answers),
            print_func=messages.append,
        )

        self.assertEqual(answer, "A")
        self.assertEqual(
            messages,
            ["Invalid answer. Please enter A, B, C, or D."],
        )

    def run_quiz_with_answers(self, answers, messages=None):
        """Run the quiz with test answers and written explanations."""

        answer_iterator = iter(answers)

        def fake_input(prompt):
            if "explain your reasoning" in prompt.lower():
                return "I chose this answer because it follows the project rules."

            return next(answer_iterator)

        if messages is None:
            messages = []

        with tempfile.TemporaryDirectory() as temp_dir:
            notes_path = Path(temp_dir) / "understanding-check-notes.txt"

            score = run_knowledge_check(
                input_func=fake_input,
                print_func=messages.append,
                notes_path=notes_path,
            )

            # Confirm that both written explanations were saved.
            notes = notes_path.read_text(encoding="utf-8")
            self.assertEqual(notes.count("Your explanation:"), 2)

        return score, messages

    def test_all_correct_answers_get_full_score(self):
        answers = [question["answer"] for question in QUESTIONS]

        score, _ = self.run_quiz_with_answers(answers)

        self.assertEqual(score, 6)

    def test_all_wrong_answers_get_zero_score(self):
        answers = [
            "B" if question["answer"] != "B" else "A"
            for question in QUESTIONS
        ]

        score, _ = self.run_quiz_with_answers(answers)

        self.assertEqual(score, 0)

    def test_perfect_score_displays_100_percent(self):
        answers = [question["answer"] for question in QUESTIONS]

        _, messages = self.run_quiz_with_answers(answers)

        self.assertIn("Your percentage: 100.0%", messages)
        self.assertIn("Excellent work!", messages)

    def test_zero_score_displays_feedback(self):
        answers = [
            "B" if question["answer"] != "B" else "A"
            for question in QUESTIONS
        ]

        _, messages = self.run_quiz_with_answers(answers)

        self.assertIn("Your percentage: 0.0%", messages)
        self.assertIn("Keep learning and try again.", messages)


if __name__ == "__main__":
    unittest.main()
