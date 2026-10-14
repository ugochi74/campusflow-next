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

Engineer A worked on ticket creation and storage. Engineer B worked on workflow and reports.

We used separate Git branches, reviewed each other's Pull Requests, and tested how our code worked together.

## What we learned

We learned how to split a program into smaller files, work together using GitHub, test Python code, and save information with JSON.
