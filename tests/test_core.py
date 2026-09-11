from datetime import date

from core.brief import build_leaving_work_brief, build_morning_brief
from core.demo import hydrate_demo_tasks
from core.guardrails import check_official_style, external_action_gate
from core.inbox import parse_inbox
from core.meetings import process_meeting_notes
from core.projects import summarize_project


def test_inbox_parser_detects_work_project_and_call():
    result = parse_inbox("Позвонить юристу по договору Project Atlas в пятницу")

    assert result["scope"] == "Work"
    assert result["project"] == "Project Atlas"
    assert result["category"] == "Call"
    assert result["status"] == "Inbox"
    assert result["attention"] == "ACTION"


def test_inbox_parser_does_not_invent_deadline_and_marks_waiting():
    result = parse_inbox("Ждем ответ от клиента по договору Project Atlas")

    assert result["deadline"] == ""
    assert result["status"] == "Waiting"
    assert result["scope"] == "Work"


def test_inbox_parser_marks_decision_required():
    result = parse_inbox("Нужно решить, выбрать вариант запуска Client Portal")

    assert result["decision_required"] is True
    assert result["attention"] == "DECISION REQUIRED"


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


def test_morning_brief_separates_decisions_waiting_and_personal():
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
            "task": "Waiting",
            "scope": "Work",
            "priority": "Normal",
            "deadline": "",
            "status": "Waiting",
            "decision_required": False,
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
    assert [item["task"] for item in brief["overdue"]] == ["Waiting"]
    assert [item["task"] for item in brief["personal"]] == ["Personal"]


def test_leaving_work_brief_groups_practical_errands():
    today = date.today().isoformat()
    tasks = [
        {
            "task": "Finish client note",
            "scope": "Work",
            "priority": "High",
            "deadline": today,
            "status": "In progress",
            "category": "Task",
        },
        {
            "task": "Buy printer paper",
            "scope": "Personal",
            "priority": "Normal",
            "deadline": today,
            "status": "To do",
            "category": "Purchase",
        },
        {
            "task": "Pick up repaired laptop",
            "scope": "Personal",
            "priority": "Normal",
            "deadline": today,
            "status": "To do",
            "category": "Errand",
        },
    ]

    brief = build_leaving_work_brief(tasks)

    assert brief["before_leaving_work"][0]["task"] == "Finish client note"
    assert brief["buy"][0]["task"] == "Buy printer paper"
    assert brief["pick_up_or_stop_by"][0]["task"] == "Pick up repaired laptop"


def test_meeting_parser_extracts_follow_up_and_promises():
    result = process_meeting_notes(
        "Решили оставить пилот узким.\n"
        "Мы подготовим два варианта цены до пятницы.\n"
        "Клиент отправит список вопросов до четверга.\n"
        "Юрист должен проверить договор до пятницы.\n"
        "Вопрос: кто войдет в первую волну?"
    )

    assert len(result["decisions"]) == 1
    assert len(result["action_items"]) >= 2
    assert len(result["open_questions"]) == 1
    assert result["our_promises"][0].startswith("Мы подготовим")
    assert result["other_side_promises"][0].startswith("Клиент отправит")
    assert result["follow_up_required"] is True


def test_external_action_gate_requires_approval_for_important_message():
    gate = external_action_gate(
        action_type="external_message",
        explicit_approval=False,
        important_external_message=True,
    )

    assert gate["approval_required"] is True
    assert gate["allowed_mode"] == "draft_only"
    assert gate["attention"] == "DECISION REQUIRED"


def test_official_style_flags_em_dash_and_arrow():
    issues = check_official_style("Добрый день — направляем материалы → на проверку.")

    assert len(issues) == 2


def test_project_summary_returns_expected_fields():
    project = {
        "name": "Project Atlas",
        "goal": "Validate demand",
        "strategy": "Pilot first",
        "metrics": ["Conversion"],
        "decisions": [
            {
                "date": "2026-09-10",
                "decision": "Keep the pilot narrow",
                "reason": "Cleaner signal",
            }
        ],
        "risks": ["Slow sales"],
        "blockers": [],
        "next_actions": ["Interview clients"],
    }

    result = summarize_project(project)

    assert result["name"] == "Project Atlas"
    assert result["goal"] == "Validate demand"
    assert result["next_actions"] == ["Interview clients"]
    assert result["decisions"][0]["reason"] == "Cleaner signal"
