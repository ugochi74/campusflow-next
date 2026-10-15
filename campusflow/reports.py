
def generate_report(tickets):
    report = {
        "total": len(tickets),
        "by_status": {
            "open": 0,
            "in_progress": 0,
            "resolved": 0
        },
        "by_priority": {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        },
        "by_category": {
            "Network": 0,
            "Hardware": 0,
            "Software": 0,
            "Other": 0
        },
        "unresolved": 0,
        "resolved": 0,
        "resolution_percentage": 0
    }

    for ticket in tickets:
        status = ticket["status"]
        priority = ticket["priority"]
        category = ticket["category"]

        report["by_status"][status] += 1
        report["by_priority"][priority] += 1
        report["by_category"][category] += 1

        if status == "resolved":
            report["resolved"] += 1
        else:
            report["unresolved"] += 1

    if report["total"] > 0:
        report["resolution_percentage"] = (
            report["resolved"] / report["total"]
        ) * 100

    return report
