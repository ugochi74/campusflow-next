
import unittest
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

        with patch("builtins.input", side_effect=lambda _: next(answers)):
            with patch("builtins.print") as mock_print:
                answer = get_valid_answer()

        self.assertEqual(answer, "A")
        mock_print.assert_called_once_with(
            "Invalid answer. Please enter A, B, C, or D."
        )

    def test_all_correct_answers_get_full_score(self):
        answers = iter(question["answer"] for question in QUESTIONS)

        score = run_knowledge_check(
            input_func=lambda _: next(answers),
            print_func=lambda message: None,
        )

        self.assertEqual(score, 6)

    def test_all_wrong_answers_get_zero_score(self):
        answers = iter(
            "A" if question["answer"] != "A" else "B"
            for question in QUESTIONS
        )

        score = run_knowledge_check(
            input_func=lambda _: next(answers),
            print_func=lambda message: None,
        )

        self.assertEqual(score, 0)


if __name__ == "__main__":
    unittest.main()
