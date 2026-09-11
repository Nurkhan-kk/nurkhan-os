from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, timedelta
import re

from core.guardrails import classify_attention


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
    attention: str
    decision_required: bool


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


def _detect_status(lowered: str) -> str:
    if any(marker in lowered for marker in ["ждем", "ждём", "ожидаем", "waiting for", "awaiting"]):
        return "Waiting"
    if any(marker in lowered for marker in ["уже делаю", "в работе", "начал", "начала", "in progress"]):
        return "In progress"
    return "Inbox"


def _detect_decision_required(lowered: str) -> bool:
    markers = [
        "нужно решить",
        "надо решить",
        "выбрать вариант",
        "принять решение",
        "что выбрать",
        "решить,",
        "decision required",
        "choose option",
        "need to decide",
    ]
    return any(marker in lowered for marker in markers)


def parse_inbox(text: str) -> dict[str, object]:
    cleaned = " ".join(text.strip().split())
    lowered = cleaned.lower()

    work_markers = [
        "client",
        "клиент",
        "contract",
        "договор",
        "project",
        "проект",
        "meeting",
        "встреч",
        "legal",
        "юрист",
        "presentation",
        "презентац",
        "commercial",
        "коммерчес",
        "partner",
        "партнер",
        "отчет",
        "report",
        "team",
        "команда",
    ]
    personal_markers = [
        "buy",
        "купить",
        "home",
        "дом",
        "pick up",
        "забрать",
        "doctor",
        "врач",
        "family",
        "семья",
        "заехать",
        "order",
        "заказать",
        "personal",
        "личн",
    ]

    work_score = sum(marker in lowered for marker in work_markers)
    personal_score = sum(marker in lowered for marker in personal_markers)
    scope = "Work" if work_score >= personal_score and work_score > 0 else "Personal"

    project = "General" if scope == "Work" else "Personal"
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
    status = _detect_status(lowered)
    decision_required = _detect_decision_required(lowered)

    category = "Task"
    if any(word in lowered for word in ["позвонить", "созвон", "набрать", "call"]):
        category = "Call"
    elif any(word in lowered for word in ["купить", "заказать", "buy", "order"]):
        category = "Purchase"
    elif any(word in lowered for word in ["встретиться", "встреча", "созвониться", "meeting"]):
        category = "Meeting"
    elif any(word in lowered for word in ["проверить", "сверить", "check", "review"]):
        category = "Check"

    action_required = bool(cleaned) and not any(
        marker in lowered for marker in ["к сведению", "просто информация", "fyi", "for information"]
    )
    attention = classify_attention(
        decision_required=decision_required,
        action_required=action_required,
    )

    if status == "Waiting":
        next_action = "Track the dependency and follow up when appropriate."
    elif attention == "FYI":
        next_action = "No action required."
    elif decision_required:
        next_action = "Prepare options and request a decision."
    else:
        next_action = cleaned or "Clarify the next action."

    draft = TaskDraft(
        task=cleaned or "Untitled task",
        scope=scope,
        project=project,
        priority=priority,
        deadline=deadline,
        context="Captured from free-form inbox input. No deadline is invented when none is stated.",
        owner="Me",
        status=status,
        next_action=next_action,
        category=category,
        attention=attention,
        decision_required=decision_required,
    )
    return asdict(draft)
