from __future__ import annotations

from datetime import date, timedelta


def _resolve_deadline(value: str, today: date) -> str:
    token = (value or "").strip().upper()

    if token == "TODAY":
        return today.isoformat()
    if token == "TOMORROW":
        return (today + timedelta(days=1)).isoformat()
    if token.startswith("OVERDUE_"):
        try:
            days = int(token.split("_", 1)[1])
            return (today - timedelta(days=days)).isoformat()
        except (ValueError, IndexError):
            return value
    if token.startswith("IN_"):
        try:
            days = int(token.split("_", 1)[1])
            return (today + timedelta(days=days)).isoformat()
        except (ValueError, IndexError):
            return value

    return value


def hydrate_demo_tasks(tasks: list[dict], today: date | None = None) -> list[dict]:
    """Return a copy of demo tasks with relative deadline tokens resolved."""
    current_day = today or date.today()
    hydrated: list[dict] = []

    for task in tasks:
        item = dict(task)
        item["deadline"] = _resolve_deadline(str(item.get("deadline", "")), current_day)
        hydrated.append(item)

    return hydrated
