# CampusFlow — Design Decisions

This document explains some of the choices we made while building CampusFlow.

## 1. Why we used Python

We used Python because it is easy to read and was required for our project. We also wanted to practise writing functions and tests.

## 2. Why we made a terminal program

CampusFlow runs in the terminal. This kept the project simple and let us focus on making the features work before thinking about a website.

## 3. How we store a ticket

Each ticket is a Python dictionary. It holds information such as the ticket ID, title, category, urgency, priority, status, and assigned staff member.

We keep the tickets together in a list.

## 4. How we choose priority

The program uses urgency and the number of affected users to decide whether a ticket is critical, high, medium, or low priority.

This helps the team work on important problems first.

## 5. Why tickets have different statuses

We use three statuses: `open`, `in_progress`, and `resolved`.

A ticket must be assigned before work starts. A resolved ticket can be reopened if the problem comes back.

These rules help us track what is happening to each ticket.

## 6. How the work queue works

The queue shows only open tickets. Critical tickets come first, followed by high, medium, and low priority tickets.

When two tickets have the same priority, the ticket with the smaller ID comes first.

## 7. How reports work

The report counts all tickets and shows how many tickets belong to each status and priority level.

This gives a quick picture of the helpdesk's work.

## 8. Why we used JSON

We used JSON to save tickets so they are still available when the program closes.

JSON is simple, and Python can read and write it without installing anything extra.

## 9. Why we wrote tests

We used Python's `unittest` to check our functions. Tests help us notice mistakes when we change the code.

## 10. How we worked as a team

Engineer A worked on ticket creation and storage. Engineer B worked on workflow, reports, search and engineering knowledge check.

We used separate Git branches, reviewed each other's Pull Requests, and tested how our code worked together.

## What we learned

We learned how to split a program into smaller files, work together using GitHub, test Python code, and save information with JSON.

# CampusFlow-Next 

## 11. How we validate ticket information

We validate ticket information before accepting it. This helps prevent missing titles, invalid categories, incorrect urgency values, and invalid numbers of affected users. We also normalize certain values so that information is stored consistently.

## 12. How ticket IDs are generated

Each ticket receives a unique ID, such as `T001` or `T002`. We generate the next ID using the highest existing ticket number plus one, rather than simply counting the tickets. This prevents ID collisions when existing tickets have gaps in their numbering.

## 13. How search works

The search feature helps staff find tickets using the title, category, status, and priority. Title searches are case-insensitive, and users can combine filters. When multiple filters are provided, a ticket must match all of them to appear in the results.

## 14. Why we added the Engineering Knowledge Check

We added a nine-question multiple-choice knowledge check to help engineers test their understanding of the project. It accepts answers using options A, B, C, and D, provides feedback on answers, and calculates a score. This supports learning and helps team members prepare to explain their technical decisions during reviews and audits.

## 15. How we handle invalid operations and storage errors

We validate operations before changing ticket data. If an operation is rejected, the existing ticket information should remain unchanged. We also use safeguards when loading and saving JSON data to reduce the risk of partial updates or data loss.

## 16. Limitations and future improvements

CampusFlow currently uses a command-line interface and JSON file storage to keep the project simple. Future improvements could include a web interface, database storage, user authentication, and more advanced reporting as the application's needs growing.

## What we learned
Through this project, we improved our understanding of Python functions, input validation, data structures, JSON storage, testing, and GitHub collaboration.

We learned why it is important to test both valid and invalid inputs, and keep different responsibilities in separate modules.
