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

    if "сегодня" in lowered:
        return today.isoformat()
    if "завтра" in lowered:
        return (today + timedelta(days=1)).isoformat()

    weekdays = {
        "понедельник": 0,
        "вторник": 1,
        "сред": 2,
        "четверг": 3,
        "пятниц": 4,
        "суббот": 5,
        "воскрес": 6,
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
        "клиент", "договор", "проект", "офд", "business", "amian", "встреч", "юрист",
        "презентац", "коммерчес", "партнер", "отчет", "команда",
    ]
    personal_markers = [
        "купить", "дом", "забрать", "врач", "семья", "заехать", "заказать", "личн",
    ]

    work_score = sum(marker in lowered for marker in work_markers)
    personal_score = sum(marker in lowered for marker in personal_markers)
    scope = "Work" if work_score >= personal_score and work_score > 0 else "Personal"

    project = "General"
    project_map = {
        "офд": "OFD",
        "business go": "Business Go",
        "amian": "Amian",
        "greenmag": "GreenMag",
        "мври": "МВРИ",
    }
    for marker, name in project_map.items():
        if marker in lowered:
            project = name
            break

    priority = "High" if any(word in lowered for word in ["срочно", "важно", "критично"]) else "Normal"
    deadline = _extract_deadline(cleaned)

    category = "Task"
    if any(word in lowered for word in ["позвонить", "созвон", "набрать"]):
        category = "Call"
    elif any(word in lowered for word in ["купить", "заказать"]):
        category = "Purchase"
    elif any(word in lowered for word in ["встретиться", "встреча", "созвониться"]):
        category = "Meeting"
    elif any(word in lowered for word in ["проверить", "сверить"]):
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
