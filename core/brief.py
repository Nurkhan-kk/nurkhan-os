from __future__ import annotations

from datetime import date


def _sort_key(task: dict) -> tuple[int, str]:
    priority_rank = 0 if task.get("priority") == "High" else 1
    deadline = task.get("deadline") or "9999-12-31"
    return priority_rank, deadline


def build_morning_brief(tasks: list[dict]) -> dict[str, list[dict]]:
    today = date.today().isoformat()

    work_priorities: list[dict] = []
    decisions: list[dict] = []
    overdue_or_stuck: list[dict] = []
    personal: list[dict] = []
    can_wait: list[dict] = []

    for task in tasks:
        status = task.get("status", "")
        if status in {"Done", "Cancelled"}:
            continue

        deadline = task.get("deadline", "")
        scope = task.get("scope", "")
        priority = task.get("priority", "Normal")
        needs_decision = bool(task.get("decision_required", False))

        if needs_decision:
            decisions.append(task)
            continue

        if (deadline and deadline < today) or status == "Waiting":
            overdue_or_stuck.append(task)
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
        "work_priorities": sorted(work_priorities, key=_sort_key)[:5],
        "decisions": sorted(decisions, key=_sort_key)[:5],
        "overdue": sorted(overdue_or_stuck, key=_sort_key)[:5],
        "personal": sorted(personal, key=_sort_key)[:5],
        "can_wait": sorted(can_wait, key=_sort_key)[:5],
    }
