# CAMPUSFLOW NEXT

# Engineer A (mercy ujih) — AI Learning Log

## Learning Cycle 1 — Ticket Validation and ID Generation

**Concept gap:** I needed to understand how to validate ticket information and generate unique ticket IDs without accepting invalid data or creating duplicate IDs.

**Question asked AI:** How can I validate ticket inputs and generate the next ticket ID safely, including when existing IDs have gaps?

**AI guidance:** Validate required fields and allowed values before creating a ticket. Generate the next ID from the highest existing numeric ticket ID plus one, rather than simply counting tickets.

**Independent experiment:** I tested valid and invalid ticket inputs and checked ID generation with existing IDs that had gaps.

**How I verified the guidance:** I ran unit tests covering invalid inputs, ticket validation, and ID generation. I checked that generated IDs followed the expected sequence and that invalid information was rejected.

**Engineering decision:** I kept ticket validation and ID generation in the ticket module and used automated tests to check their beahviour.

**What I learned:** Validating input before creating a ticket helps prevent bad data. Using the highest existing ID avoids duplicate IDs when earlier tickets have been deleted.

## Learning Cycle 2 — Safe Ticket Updates and JSON Storage

**Concept gap:** I needed to understand how to protect existing ticket data when an operation fails and how to load saved tickets without accepting an invalid collection.

**Question asked AI:** How can I validate ticket operations and safely load and save ticket data using JSON without leaving the program in an inconsistent state?

**AI guidance:** Check that an operation is valid before changing ticket data. When loading JSON, validate the complete collection before replacing the current data. Handle storage errors so failed operations do not silently corrupt existing information.

**Independent experiment:** I tested invalid ticket data, duplicate ticket IDs, and failed save operations to check whether existing information was preserved.

**How I verified the guidance:** I ran the storage and ticket unit tests, including tests for duplicate IDs, invalid data, and preserving an existing file when saving fails. I also ran the wider test suite to check that the changes did not break other features.

**Engineering decision:** I used validation before mutation and added safeguards around JSON loading and saving. I kept the storage logic separate from the CLI so it could be tested independently.

**What I learned:** A failed operation should not leave ticket data partially changed. Testing failure cases is just as important as testing successful operations.

## Engineer A — Teamwork Reflection

I focused on ticket validation, ID generation, and protecting ticket data. I worked with Engineer B, who handled search, reporting, and the Engineering Knowledge Check. We used Git branches and Pull Requests to review changes and worked together to integrate our features.

I learned that clear task ownership, focused commits, code reviews, and tests help a team work on separate features while maintaining one working application.

## Final Verification

I used AI to understand concepts, explore possible solutions, and debug problems. I checked suggestions against the project requirements, source code, and automated tests rather than accepting them without verification.

Before submitting this log, I confirmed that the test results and implementation details matched my actual work and latest test run.

## Engineer B (confidence odo) — Search, Reporting and Knowledge Check

### Learning Cycle 1 — Combined Ticket Search

**Concept gap:** I needed to understand how multiple search filters work together and how to verify that the search returns only matching tickets.

**Question asked AI:** How can I implement a ticket search that combines title, category, status, and priority filters while ignoring differences in letter case?

**AI guidance:** Check each supplied filter against every ticket. If a filter does not match, skip that ticket. Normalize user input before comparing values, and return the matching tickets without changing the original list.

**Independent experiment:** I used a small list of books to test how two conditions joined with `and` work together.

**How I verified the guidance:** I ran the search unit tests covering combined filters, empty filters, case-insensitive title matching, no matches, and preservation of the original ticket list. The search tests passed as part of the full test suite.

**Engineering decision:** I kept the search logic in `campusflow/search.py`, separate from CLI input and output. This makes the function easier to test and reuse.

**What I learned:** Combined filters using `and` become more restrictive as filters are added. A ticket must satisfy every supplied filter to appear in the results.

### Learning Cycle 2 — Testing the Engineering Knowledge Check

**Concept gap:** I needed to understand how to test interactive functions without requiring manual keyboard input and how to retry invalid answers.

**Question asked AI:** How can I test a Python knowledge check that accepts A/B/C/D answers, rejects invalid input, and calculates a score without manually answering each question?

**AI guidance:** Pass input and output functions into the quiz so tests can provide predictable answers. Keep asking when an answer is invalid, and return the final score so tests can check the result.

**What went wrong and how I corrected it:** My initial tests stalled because `input` had been captured as a default argument before the test replaced the built-in input function. I changed the function to accept `input_func=None` and assign `input` inside the function when no replacement is provided, I also corrected a missing function import in my test file so the test could call the function successfully.

**Independent experiment:** I supplied a small replacement input function that returned `"B"` and confirmed that the function received and returned the answer without interactive typing.

**How I verified the guidance:** I ran `python3 -m unittest tests.test_knowledge_check -v`. All five tests passed, covering the six-question count, valid answers, invalid-answer retries, full score, and zero score. I then ran the complete test suite, which passed all 78 tests.

**Engineering decision:** I kept the quiz logic in `campusflow/knowledge_check.py`, added automated tests in `tests/test_knowledge_check.py`, and integrated the quiz into the CLI menu.

**What I learned:** Default arguments are evaluated when a function is defined. Using `None` and assigning the default inside the function makes it easier to replace dependencies during testing.

## Engineer B — Reporting Reflection

I expanded the ticket reports to show totals by status, priority, and category, alongside resolved and unresolved counts and the resolution percentage.

I verified the report calculations using unit tests for empty ticket lists, category and priority counts, status counts, and resolution percentages.

**What I learned:** Reports should be checked against known test data, including empty and edge cases, rather than judged only by whether the output looks correct.

## Final Verification

My latest recorded full test run completed with **78 tests passing**. I also compiled `main.py` and `campusflow/knowledge_check.py` successfully with `py_compile`.

I used AI as a learning and debugging aid, then checked the resulting implementation using experiments, automated tests.
