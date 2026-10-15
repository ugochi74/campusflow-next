import unittest
from unittest.mock import patch

from campusflow.knowledge_check import (
    QUESTIONS,
    get_valid_answer,
    run_knowledge_check,
)


class TestKnowledgeCheck(unittest.TestCase):

    def test_quiz_has_nine_questions(self):
        self.assertEqual(len(QUESTIONS), 9)

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

    def test_all_correct_answers_get_full_score(self):
        answers = iter(question["answer"] for question in QUESTIONS)

        score = run_knowledge_check(
            input_func=lambda _: next(answers),
            print_func=lambda message: None,
        )

        self.assertEqual(score, 9)

    def test_all_wrong_answers_get_zero_score(self):
        answers = iter(
            "B" if question["answer"] != "B" else "A"
            for question in QUESTIONS
        )

        score = run_knowledge_check(
            input_func=lambda _: next(answers),
            print_func=lambda message: None,
        )

        self.assertEqual(score, 0)

    def test_perfect_score_displays_100_percent(self):
        answers = iter(question["answer"] for question in QUESTIONS)
        messages = []

        run_knowledge_check(
            input_func=lambda _: next(answers),
            print_func=messages.append,
        )

        self.assertIn("Your percentage: 100.0%", messages)
        self.assertIn("Excellent work!", messages)

    def test_zero_score_displays_feedback(self):
        answers = iter(
            "B" if question["answer"] != "B" else "A"
            for question in QUESTIONS
        )
        messages = []

        run_knowledge_check(
            input_func=lambda _: next(answers),
            print_func=messages.append,
        )

        self.assertIn("Your percentage: 0.0%", messages)
        self.assertIn("Keep learning and try again.", messages)


if __name__ == "__main__":
    unittest.main()