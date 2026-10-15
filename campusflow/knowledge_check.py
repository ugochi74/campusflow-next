QUESTIONS = [
    {
        "question": "What is the main purpose of CampusFlow?",
        "options": {
            "A": "Manage helpdesk tickets",
            "B": "Design websites",
            "C": "Send emails only",
            "D": "Create computer games",
        },
        "answer": "A",
        "explanation": "CampusFlow helps users create, manage, and track helpdesk tickets.",
    },
    {
        "question": "Why do we write unit tests?",
        "options": {
            "A": "To make files larger",
            "B": "To check that code behaves as expected",
            "C": "To replace all documentation",
            "D": "To avoid writing functions",
        },
        "answer": "B",
        "explanation": "Unit tests help us detect errors and verify individual pieces of code.",
    },
    {
        "question": "What does a Python dictionary store?",
        "options": {
            "A": "Only numbers",
            "B": "Only strings",
            "C": "Key-value pairs",
            "D": "Only functions",
        },
        "answer": "C",
        "explanation": "A dictionary stores information as key-value pairs.",
    },
    {
        "question": "What is the purpose of Git branches?",
        "options": {
            "A": "To delete the repository",
            "B": "To work on changes separately",
            "C": "To run Python tests",
            "D": "To install Python",
        },
        "answer": "B",
        "explanation": "Branches allow developers to work on changes independently.",
    },
    {
        "question": "What does a function return when it uses return?",
        "options": {
            "A": "A value to the caller",
            "B": "A new Git branch",
            "C": "A test report automatically",
            "D": "A Python installation",
        },
        "answer": "A",
        "explanation": "The return statement sends a value back to the caller.",
    },
    {
        "question": "Why should ticket input be validated?",
        "options": {
            "A": "To make every ticket critical",
            "B": "To prevent all tickets from being saved",
            "C": "To ensure input follows the expected rules",
            "D": "To remove the ticket ID",
        },
        "answer": "C",
        "explanation": "Validation rejects invalid data before it causes problems.",
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
        "explanation": "Filters combine with AND, so every supplied filter must match.",
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
        "explanation": "Resolved tickets are closed; notes are allowed only after a valid reopen.",
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
        "explanation": "An empty dataset should be handled without dividing by zero.",
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


def run_knowledge_check(input_func=None, print_func=None):
    """Run the engineering knowledge check and return the score."""

    if input_func is None:
        input_func = input

    if print_func is None:
        print_func = print

    score = 0

    print_func("\n========== ENGINEERING KNOWLEDGE CHECK ==========")

    for question_number, question in enumerate(QUESTIONS, start=1):
        print_func(f"\nQuestion {question_number}: {question['question']}")

        for letter, option in question["options"].items():
            print_func(f"{letter}. {option}")

        answer = get_valid_answer(input_func, print_func)

        if answer == question["answer"]:
            score += 1
            print_func("Correct!")
        else:
            print_func(
                f"Incorrect. The correct answer is {question['answer']}."
            )

        explanation = question.get("explanation")
        if explanation:
            print_func(f"Explanation: {explanation}")

    total_questions = len(QUESTIONS)
    percentage = (
        (score / total_questions) * 100 if total_questions else 0
    )

    print_func(f"\nYour final score: {score}/{total_questions}")
    print_func(f"Your percentage: {percentage:.1f}%")

    if percentage >= 80:
        print_func("Excellent work!")
    elif percentage >= 50:
        print_func("Good effort! Keep practising.")
    else:
        print_func("Keep learning and try again.")

    return score