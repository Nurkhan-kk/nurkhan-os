from __future__ import annotations

from datetime import date, timedelta


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


def build_leaving_work_brief(tasks: list[dict]) -> dict[str, list[dict]]:
    today = date.today().isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    result: dict[str, list[dict]] = {
        "before_leaving_work": [],
        "buy": [],
        "pick_up_or_stop_by": [],
        "on_the_way": [],
        "at_home": [],
        "dont_forget": [],
        "move_to_tomorrow": [],
    }

    for task in sorted(tasks, key=_sort_key):
        if task.get("status") in {"Done", "Cancelled"}:
            continue

        title = str(task.get("task", ""))
        lowered = title.lower()
        scope = task.get("scope", "")
        deadline = task.get("deadline", "")
        category = task.get("category", "")

        if category == "Purchase" or any(marker in lowered for marker in ["buy", "купить", "заказать", "order"]):
            result["buy"].append(task)
        elif any(marker in lowered for marker in ["забрать", "заехать", "pick up", "stop by"]):
            result["pick_up_or_stop_by"].append(task)
        elif any(marker in lowered for marker in ["по пути", "on the way"]):
            result["on_the_way"].append(task)
        elif scope == "Personal" and any(marker in lowered for marker in ["дома", "домой", "at home", "home"]):
            result["at_home"].append(task)
        elif any(marker in lowered for marker in ["не забыть", "remember", "dont forget", "don't forget"]):
            result["dont_forget"].append(task)
        elif scope == "Work" and deadline == today:
            result["before_leaving_work"].append(task)
        elif deadline == tomorrow or (scope == "Work" and deadline and deadline > today):
            result["move_to_tomorrow"].append(task)
        elif scope == "Personal" and deadline == today:
            result["dont_forget"].append(task)

    return {key: value[:5] for key, value in result.items()}
