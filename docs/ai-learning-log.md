# CampusFlow — AI Learning Log

We used AI for guidance while building CampusFlow. We checked suggestions against our code, tests, and reviews instead of accepting every answer immediately.

## Engineer A — Ticket Management and JSON Storage

**Question 1:** How can I validate ticket titles, categories, urgency, and affected users in Python?

**AI suggestion:** Create a `validate_ticket_input()` function to reject invalid inputs and normalize valid values.

**What I did to verify it:** Tested valid and invalid inputs in `tests/test_tickets.py`, including blank titles, invalid categories, and decimal affected-user values.

**What I learned:** Validation prevents incorrect data from entering the system and keeps ticket information consistent.

**Question 2:** How can I save tickets to JSON and load them safely?

**AI suggestion:** Use `json` in `storage.py` to save and load tickets, handling missing files, invalid JSON, and duplicate IDs.

**What I did to verify it:** Ran the storage tests for saving, loading, invalid JSON, duplicate IDs, and failed saves. My recorded test run passed all 40 tests.

**What I learned:** JSON preserves ticket data after the program closes, while validation and error handling help protect data integrity.

**Question 3:** How should I organize my storage code and tests to avoid errors?

**Original AI suggestion:** Separate ticket saving and loading into functions and test their behaviour.

**What I independently corrected or improved:** I removed an unnecessary self-import in `storage.py` that caused a circular-import error. I also corrected validation and test issues.

**How I verified my change:** Reran the automated test suite and confirmed that all 40 tests passed.

**What I learned:** AI suggestions must be checked against the existing code. Debugging, validation, and testing help ensure the implementation works correctly.


## Engineer B — Workflow and Reporting

**Question 1:** How do I assign a ticket, deal with blank names, and stop someone assigning a resolved ticket?

**AI suggestion:** Find the ticket by ID, check that the staff name is not blank, remove spaces around the name with `.strip()`, and require a resolved ticket to be reopened before assignment.

**What I did to verify it:** I tested assignment using a name with extra spaces, such as `  Sarah  `, and saw that it was stored as `Sarah` or in normalized form in the version being tested. I also checked assignment and status rules in the workflow tests.

**What I learned:** I learned that user input needs checking before a ticket is changed.

**Question 2:** How do I stop invalid status changes, and how should tickets with the same priority be ordered?

**AI suggestion:** Only allow `open` to `in_progress` after assignment, then `in_progress` to `resolved`; use a separate action to reopen a resolved ticket. Show only open tickets in the queue, ordered by priority and then ticket number.

**What I did to verify it:** I tried an invalid status change and confirmed the status did not change. I also checked a priority tie and observed that the ticket with the lower ID came first.

**What I learned:** I learned that workflow rules must be enforced in code, not just explained to users.

**Question 3:** How should I check the complete save-and-reload process after a reviewer asked whether ticket IDs would stay unique?

**Original AI suggestion:** AI suggested testing the whole process with a `try_integration.py` script: create `T001`, save it, reload it, then create `T002`. An earlier suggestion also proposed committing an integration test to the repository.

**What I independently corrected, improved, or rejected:** I rejected the idea of committing my temporary `try_integration.py` script. I wanted that file only for local checking, not as part of the submitted project. I kept temporary testing separate from permanent project tests.

**How I verified my change:** The existing unit-test run showed **40 passing tests**. The temporary save–reload–create scenario was prepared for a separate check.

**What I learned:** AI suggestions can be useful without being followed exactly. I learned to choose what belongs in the project and what should stay as a local experiment.

## What we learned together

AI helped us understand errors, plan functions, and think of tests. But we still had to check the code ourselves. Reviewing each other's work helped us spot problems before merging.
