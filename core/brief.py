from __future__ import annotations

from datetime import date


def build_morning_brief(tasks: list[dict]) -> dict[str, list[dict]]:
    today = date.today().isoformat()

    work_priorities = []
    decisions = []
    overdue = []
    personal = []
    can_wait = []

    for task in tasks:
        status = task.get("status", "")
        if status in {"Done", "Cancelled"}:
            continue

        deadline = task.get("deadline", "")
        scope = task.get("scope", "")
        priority = task.get("priority", "Normal")
        needs_decision = task.get("decision_required", False)

        if deadline and deadline < today:
            overdue.append(task)
            continue

        if needs_decision:
            decisions.append(task)
            continue

        if scope == "Personal":
            if deadline == today or priority == "High":
                personal.append(task)
            else:
                can_wait.append(task)
            continue

        if priority == "High" or deadline == today:
            work_priorities.append(task)
        else:
            can_wait.append(task)

    return {
        "work_priorities": work_priorities[:5],
        "decisions": decisions[:5],
        "overdue": overdue[:5],
        "personal": personal[:5],
        "can_wait": can_wait[:5],
    }
