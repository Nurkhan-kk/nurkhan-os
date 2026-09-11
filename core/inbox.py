from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, timedelta
import re


@dataclass
class TaskDraft:
    task: str
    scope: str
    project: str
    priority: str
    deadline: str
    context: str
    owner: str
    status: str
    next_action: str
    category: str


def _extract_deadline(text: str) -> str:
    lowered = text.lower()
    today = date.today()

    if "сегодня" in lowered or "today" in lowered:
        return today.isoformat()
    if "завтра" in lowered or "tomorrow" in lowered:
        return (today + timedelta(days=1)).isoformat()

    weekdays = {
        "понедельник": 0,
        "monday": 0,
        "вторник": 1,
        "tuesday": 1,
        "сред": 2,
        "wednesday": 2,
        "четверг": 3,
        "thursday": 3,
        "пятниц": 4,
        "friday": 4,
        "суббот": 5,
        "saturday": 5,
        "воскрес": 6,
        "sunday": 6,
    }
    for name, target_weekday in weekdays.items():
        if name in lowered:
            days_ahead = (target_weekday - today.weekday()) % 7
            days_ahead = 7 if days_ahead == 0 else days_ahead
            return (today + timedelta(days=days_ahead)).isoformat()

    explicit = re.search(r"\b(\d{1,2})[./](\d{1,2})(?:[./](\d{2,4}))?\b", lowered)
    if explicit:
        day, month, year = explicit.groups()
        year_value = int(year) if year else today.year
        if year_value < 100:
            year_value += 2000
        try:
            return date(year_value, int(month), int(day)).isoformat()
        except ValueError:
            return ""

    return ""


def parse_inbox(text: str) -> dict[str, str]:
    cleaned = " ".join(text.strip().split())
    lowered = cleaned.lower()

    work_markers = [
        "client", "клиент", "contract", "договор", "project", "проект", "meeting", "встреч",
        "legal", "юрист", "presentation", "презентац", "commercial", "коммерчес", "partner",
        "партнер", "report", "отчет", "team", "команда",
    ]
    personal_markers = [
        "buy", "купить", "home", "дом", "pick up", "забрать", "doctor", "врач", "family",
        "семья", "заехать", "order", "заказать", "personal", "личн",
    ]

    work_score = sum(marker in lowered for marker in work_markers)
    personal_score = sum(marker in lowered for marker in personal_markers)
    scope = "Work" if work_score >= personal_score and work_score > 0 else "Personal"

    project = "General"
    project_map = {
        "project atlas": "Project Atlas",
        "atlas": "Project Atlas",
        "client portal": "Client Portal",
        "portal": "Client Portal",
    }
    for marker, name in project_map.items():
        if marker in lowered:
            project = name
            break

    priority = "High" if any(word in lowered for word in ["срочно", "важно", "критично", "urgent", "critical"]) else "Normal"
    deadline = _extract_deadline(cleaned)

    category = "Task"
    if any(word in lowered for word in ["позвонить", "созвон", "набрать", "call"]):
        category = "Call"
    elif any(word in lowered for word in ["купить", "заказать", "buy", "order"]):
        category = "Purchase"
    elif any(word in lowered for word in ["встретиться", "встреча", "созвониться", "meeting"]):
        category = "Meeting"
    elif any(word in lowered for word in ["проверить", "сверить", "check", "review"]):
        category = "Check"

    draft = TaskDraft(
        task=cleaned or "Untitled task",
        scope=scope,
        project=project,
        priority=priority,
        deadline=deadline,
        context="Captured from free-form inbox input.",
        owner="Me",
        status="Inbox",
        next_action=cleaned or "Clarify the next action.",
        category=category,
    )
    return asdict(draft)
