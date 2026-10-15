# from try_integration import create_ticket
from campusflow.tickets import create_ticket

from campusflow.workflow import (
    list_tickets,
    view_ticket,
    assign_ticket,
    update_ticket_status,
    reopen_ticket,
    get_work_queue,
    add_note,
)
from campusflow.knowledge_check import run_knowledge_check
from campusflow.reports import generate_report
from campusflow.search import search_tickets

from campusflow.storage import load_tickets, save_tickets

def display_menu():
    print("\n========== CAMPUSFLOW ==========")
    print("Campus Helpdesk Ticket Manager")
    print("================================")
    print("1. Create Ticket")
    print("2. List All Tickets")
    print("3. View Ticket")
    print("4. Assign Ticket")
    print("5. Update Ticket Status")
    print("6. Reopen Ticket")
    print("7. View Priority Work Queue")
    print("8. Search Tickets")
    print("9. Generate Report")
    print("10. Engineering Knowledge Check")
    print("11. Add Note to Ticket")
    print("12. Exit")

def get_valid_ticket_input(prompt, validation_function, error_message):
    while True:
        value = input(prompt).strip()

        try:
            validation_function(value)
            return value
        except ValueError:
            print(error_message)


def main():

    try:
        tickets = load_tickets()
    except (ValueError, OSError) as error:
        print(f"Unable to load tickets: {error}")
        return

    while True:
        display_menu()

        choice = input("\nEnter your choice (1-12): ").strip()

        if choice == "12":
            print("\nThank you for using CampusFlow!")
            break

        elif choice == "1":
            print("\n--- Create New Ticket ---")

            while True:
                title = input("Enter ticket title: ").strip()

                if not title:
                    print("Title cannot be empty.")
                    continue

                break

            while True:
                category = input(
                    "Enter category (Network/Hardware/Software/Other): "
                ).strip()

                if category.title() not in {
                    "Network", "Hardware", "Software", "Other"
                }:
                    print(
                        "Category must be Network, Hardware, "
                        "Software, or Other."
                    )
                    continue

                category = category.title()
                break

            while True:
                urgency = input(
                    "Enter urgency (low/medium/high): "
                ).strip().lower()

                if urgency not in {"low", "medium", "high"}:
                    print("Urgency must be low, medium, or high.")
                    continue

                break

            while True:
                affected_users_input = input(
                    "Enter number of affected users: "
                ).strip()

                try:
                    affected_users = int(affected_users_input)

                    if affected_users <= 0:
                        print(
                            "Affected users must be greater than zero."
                        )
                        continue

                    break

                except ValueError:
                    print("Affected users must be a whole number.")

            try:
                new_ticket = create_ticket(
                    title,
                    category,
                    urgency,
                    affected_users,
                    tickets
                )

                tickets.append(new_ticket)
                save_tickets(tickets)

                print(
                    f"\nTicket {new_ticket['id']} created successfully!"
                )
                print(f"Priority: {new_ticket['priority']}")

            except ValueError as error:
                print(f"\nCould not create ticket: {error}")

        elif choice == "2":
            list_tickets(tickets)

        elif choice == "3":
            print("\n--- View Ticket ---")

            ticket_id = input("Enter ticket ID: ").strip().upper()

            ticket = view_ticket(tickets, ticket_id)

            if ticket is None:
                print("\nTicket not found.")

            else:
                print("\nTicket Details")
                print("--------------------------")
                print(f"ID: {ticket['id']}")
                print(f"Title: {ticket['title']}")
                print(f"Category: {ticket['category']}")
                print(f"Urgency: {ticket['urgency']}")
                print(f"Affected Users: {ticket['affected_users']}")
                print(f"Priority: {ticket['priority']}")
                print(f"Status: {ticket['status']}")
                print(
                    f"Assigned To: "
                    f"{ticket['assigned_to'] or 'Unassigned'}"
                )

                print("\nNotes")
                print("--------------------------")

                notes = ticket.get("notes", [])

                if not notes:
                    print("No notes yet.")
                else:
                    for note in notes:
                        print(
                            f"{note['note_id']} | "
                            f"{note['author']}: {note['message']}"
                        )

        elif choice == "4":
            print("\n--- Assign Ticket ---")

            ticket_id = input("Enter ticket ID: ").strip().upper()
            staff_name = input("Enter staff name: ").strip()

            result = assign_ticket(tickets, ticket_id, staff_name)

            if result == "Ticket assigned successfully.":
                save_tickets(tickets)

            print(f"\n{result}")

        elif choice == "5":
            print("\n--- Update Ticket Status ---")

            ticket_id = input("Enter ticket ID: ").strip().upper()

            print("\nAvailable status updates:")
            print("1. Start Work (in_progress)")
            print("2. Resolve Ticket (resolved)")

            status_choice = input("Choose an option (1-2): ").strip()

            if status_choice == "1":
                new_status = "in_progress"

            elif status_choice == "2":
                new_status = "resolved"

            else:
                print("\nInvalid status option.")
                continue

            result = update_ticket_status(tickets, ticket_id, new_status)

            if result in (
                "Ticket is now in progress.",
                "Ticket resolved successfully."
            ):
                save_tickets(tickets)

            print(f"\n{result}")

        elif choice == "6":
            print("\n--- Reopen Ticket ---")

            ticket_id = input("Enter ticket ID: ").strip().upper()

            result = reopen_ticket(tickets, ticket_id)

            if result == "Ticket reopened successfully.":
                save_tickets(tickets)

            print(f"\n{result}")

        elif choice == "7":
            print("\n--- Priority Work Queue ---")

            work_queue = get_work_queue(tickets)

            if not work_queue:
                print("No open tickets in the work queue.")

            else:
                for ticket in work_queue:
                    print(
                        f"ID: {ticket['id']} | "
                        f"Title: {ticket['title']} | "
                        f"Priority: {ticket['priority']} | "
                        f"Status: {ticket['status']}"
                    )


        elif choice == "8":
            print("\n--- Search Tickets ---")
            print("Leave a filter blank to skip it.")

            title = input("Search by title: ").strip()
            category = input("Filter by category: ").strip()
            status = input("Filter by status: ").strip()
            priority = input("Filter by priority: ").strip()

            # Reuse the existing category validation message.
            valid_categories = {
                "network", "hardware", "software", "other"
            }

            if category and category.lower() not in valid_categories:
                print(
                    "\nCategory must be Network, Hardware, "
                    "Software, or Other."
                )
                continue

            valid_statuses = {"open", "in_progress", "resolved"}

            if status and status.lower() not in valid_statuses:
                print("\nInvalid status option.")
                continue

            valid_priorities = {"critical", "high", "medium", "low"}

            if priority and priority.lower() not in valid_priorities:
                print("\nInvalid priority option.")
                continue

            results = search_tickets(
                tickets,
                title=title,
                category=category,
                status=status,
                priority=priority
            )

            if not results:
                print("\nNo matching tickets found.")
            else:
                print(f"\nFound {len(results)} matching ticket(s):")

                for ticket in results:
                    print(
                        f"ID: {ticket['id']} | "
                        f"Title: {ticket['title']} | "
                        f"Category: {ticket['category']} | "
                        f"Priority: {ticket['priority']} | "
                        f"Status: {ticket['status']} | "
                        f"Assigned To: "
                        f"{ticket['assigned_to'] or 'Unassigned'}"
                    )

        elif choice == "9":
            print("\n========== CAMPUSFLOW REPORT ==========")

            report = generate_report(tickets)

            print(f"\nTotal Tickets: {report['total']}")

            print("\nTickets by Status:")
            print(f"  Open: {report['by_status']['open']}")
            print(f"  In Progress: {report['by_status']['in_progress']}")
            print(f"  Resolved: {report['by_status']['resolved']}")

            print("\nTickets by Priority:")
            print(f"  Critical: {report['by_priority']['critical']}")
            print(f"  High: {report['by_priority']['high']}")
            print(f"  Medium: {report['by_priority']['medium']}")
            print(f"  Low: {report['by_priority']['low']}")

            print("\nTickets by Category:")
            print(f"  Network: {report['by_category']['Network']}")
            print(f"  Hardware: {report['by_category']['Hardware']}")
            print(f"  Software: {report['by_category']['Software']}")
            print(f"  Other: {report['by_category']['Other']}")

            print("\nResolution Summary:")
            print(f"  Resolved Tickets: {report['resolved']}")
            print(f"  Unresolved Tickets: {report['unresolved']}")
            print(
                f"  Resolution Percentage: "
                f"{report['resolution_percentage']:.1f}%"
            )

        elif choice == "10":
            run_knowledge_check()



        elif choice == "11":
            print("\n--- Add Note to Ticket ---")

            ticket_id = input("Enter ticket ID: ").strip().upper()
            author = input("Enter your name: ").strip()
            message = input("Enter note (5-300 characters): ").strip()

            result = add_note(tickets, ticket_id, author, message)
            print(result)

            if result.startswith("Note added successfully"):
                try:
                    save_tickets(tickets)
                except (ValueError, OSError) as error:
                    print(f"Unable to save note: {error}")

        else:
            print("\nInvalid option. Please enter a number from 1 to 12.")


if __name__ == "__main__":
    main()
