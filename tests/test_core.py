from datetime import date

from core.brief import build_morning_brief
from core.demo import hydrate_demo_tasks
from core.inbox import parse_inbox
from core.meetings import process_meeting_notes
from core.projects import summarize_project


def test_inbox_parser_detects_work_project_and_call():
    result = parse_inbox("Позвонить юристу по договору Project Atlas в пятницу")

    assert result["scope"] == "Work"
    assert result["project"] == "Project Atlas"
    assert result["category"] == "Call"
    assert result["status"] == "Inbox"


def test_demo_deadlines_are_resolved_relative_to_today():
    tasks = [
        {"task": "A", "deadline": "TODAY"},
        {"task": "B", "deadline": "TOMORROW"},
        {"task": "C", "deadline": "OVERDUE_2"},
    ]

    hydrated = hydrate_demo_tasks(tasks, today=date(2026, 9, 11))

    assert hydrated[0]["deadline"] == "2026-09-11"
    assert hydrated[1]["deadline"] == "2026-09-12"
    assert hydrated[2]["deadline"] == "2026-09-09"


def test_morning_brief_separates_decisions_overdue_and_personal():
    tasks = [
        {
            "task": "Priority",
            "scope": "Work",
            "priority": "High",
            "deadline": date.today().isoformat(),
            "status": "To do",
            "decision_required": False,
        },
        {
            "task": "Decision",
            "scope": "Work",
            "priority": "High",
            "deadline": "",
            "status": "To do",
            "decision_required": True,
        },
        {
            "task": "Personal",
            "scope": "Personal",
            "priority": "Normal",
            "deadline": date.today().isoformat(),
            "status": "To do",
            "decision_required": False,
        },
    ]

    brief = build_morning_brief(tasks)

    assert [item["task"] for item in brief["work_priorities"]] == ["Priority"]
    assert [item["task"] for item in brief["decisions"]] == ["Decision"]
    assert [item["task"] for item in brief["personal"]] == ["Personal"]


def test_meeting_parser_extracts_main_sections():
    result = process_meeting_notes(
        "Решили оставить пилот узким.\n"
        "Нужно подготовить два варианта цены.\n"
        "Вопрос: кто войдет в первую волну?"
    )

    assert len(result["decisions"]) == 1
    assert len(result["actions"]) == 1
    assert len(result["open_questions"]) == 1


def test_project_summary_returns_expected_fields():
    project = {
        "name": "Project Atlas",
        "goal": "Validate demand",
        "strategy": "Pilot first",
        "metrics": ["Conversion"],
        "risks": ["Slow sales"],
        "blockers": [],
        "next_actions": ["Interview clients"],
    }

    result = summarize_project(project)

    assert result["name"] == "Project Atlas"
    assert result["goal"] == "Validate demand"
    assert result["next_actions"] == ["Interview clients"]
