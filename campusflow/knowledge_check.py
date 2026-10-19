
import random
from pathlib import Path

QUESTIONS = [
    {
        "question": "Ticket T001 is open and unassigned. A user tries to move it to in_progress. What should happen?",
        "options": {
            "A": "Accept",
            "B": "Reject and preserve all data",
            "C": "Resolve it automatically",
            "D": "Remove ticket",
        },
        "answer": "B",
    },
    {
        "question": "The app has zero tickets. What should resolution percentage display?",
        "options": {
            "A": "Crash",
            "B": "100%",
            "C": "0%",
            "D": "Divide by one without explanation",
        },
        "answer": "C",
    },
    {
        "question": "Filter title='wifi', category='Network', status='open'. Which records should match?",
        "options": {
            "A": "Any record matching one filter",
            "B": "Only records matching all supplied filters",
            "C": "All network records",
            "D": "All open records",
        },
        "answer": "B",
    },
    {
        "question": "A resolved ticket receives 'Add note'. What should happen?",
        "options": {
            "A": "Append anyway",
            "B": "Delete old notes",
            "C": "Reject until reopened",
            "D": "Change status silently",
        },
        "answer": "C",
    },
    {
        "question": "The JSON file includes two tickets with the same ID. What should load do?",
        "options": {
            "A": "Keep both",
            "B": "Replace memory with duplicates",
            "C": "Reject the load without changing current memory",
            "D": "Rename IDs silently",
        },
        "answer": "C",
    },
    {
        "question": "A PR changes validation but has no negative-case tests. What is the best review action?",
        "options": {
            "A": "Approve because it runs",
            "B": "Request focused tests and reasoning",
            "C": "Merge immediately",
            "D": "Ask AI to approve it",
        },
        "answer": "B",
    },
]


def get_valid_answer(input_func=None, print_func=None):
    """Keep asking until the user enters A, B, C, or D."""

    if input_func is None:
        input_func = input

    if print_func is None:
        print_func = print

    while True:
        answer = input_func("Your answer (A/B/C/D): ").strip().upper()

        if answer in {"A", "B", "C", "D"}:
            return answer

        print_func("Invalid answer. Please enter A, B, C, or D.")




def run_knowledge_check(input_func=None, print_func=None, notes_path=None):
    """Run the quiz and save the user's written explanations."""

    if input_func is None:
        input_func = input

    if print_func is None:
        print_func = print

    # Set the location of the notes file.
    if notes_path is None:
        notes_path = (
            Path(__file__).resolve().parent.parent
            / "docs"
            / "understanding-check-notes.txt"
        )
    else:
        notes_path = Path(notes_path)

    score = 0
    answers = []

    print_func("\n========== ENGINEERING KNOWLEDGE CHECK ==========")

    # Stage 1: Ask all multiple-choice questions.
    for question_number, question in enumerate(QUESTIONS, start=1):
        print_func(f"\nQuestion {question_number}: {question['question']}")

        for letter, option in question["options"].items():
            print_func(f"{letter}. {option}")

        answer = get_valid_answer(input_func, print_func)
        answers.append(answer)

        if answer == question["answer"]:
            score += 1

        print_func("Answer recorded.")

    # Stage 2: Ask the user to explain two random questions.
    print_func("\n========== EXPLAIN YOUR REASONING ==========")
    print_func("Explain why you chose your answers to these two questions.")

    selected_questions = random.sample(
        list(enumerate(QUESTIONS, start=1)),
        k=min(2, len(QUESTIONS)),
    )

    # Create the docs folder if it does not exist.
    notes_path.parent.mkdir(parents=True, exist_ok=True)

    # Append explanations to the notes file.
    with notes_path.open("a", encoding="utf-8") as notes_file:
        notes_file.write("\n========== KNOWLEDGE CHECK ==========\n")

        for question_number, question in selected_questions:
            print_func(
                f"\nQuestion {question_number}: {question['question']}"
            )
            print_func(
                f"Your selected answer: {answers[question_number - 1]}"
            )

            explanation = input_func(
                "Explain your reasoning: "
            ).strip()

            while not explanation:
                print_func("Your explanation cannot be empty.")
                explanation = input_func(
                    "Explain your reasoning: "
                ).strip()

            notes_file.write(
                f"\nQuestion {question_number}: "
                f"{question['question']}\n"
            )
            notes_file.write(
                f"Selected answer: {answers[question_number - 1]}\n"
            )
            notes_file.write(
                f"Your explanation: {explanation}\n"
            )

    print_func(f"\nYour explanations were saved to: {notes_path}")

    # Stage 3: Display the answer review without explanations.
    print_func("\n========== ANSWERS AND REVIEW ==========")

    for question_number, question in enumerate(QUESTIONS, start=1):
        user_answer = answers[question_number - 1]
        correct_answer = question["answer"]

        print_func(f"\nQuestion {question_number}: {question['question']}")
        print_func(f"Your answer: {user_answer}")
        print_func(f"Correct answer: {correct_answer}")

        if user_answer == correct_answer:
            print_func("Result: Correct")
        else:
            print_func("Result: Incorrect")

    # Stage 4: Display the final score.
    total_questions = len(QUESTIONS)

    percentage = (
        (score / total_questions) * 100
        if total_questions
        else 0
    )

    print_func("\n========== FINAL RESULT ==========")
    print_func(f"Your final score: {score}/{total_questions}")
    print_func(f"Your percentage: {percentage:.1f}%")

    if percentage >= 80:
        print_func("Excellent work!")
    elif percentage >= 50:
        print_func("Good effort! Keep practising.")
    else:
        print_func("Keep learning and try again.")

    return score
