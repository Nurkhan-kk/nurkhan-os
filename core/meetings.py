from __future__ import annotations

import re


def _action_owner(line: str) -> str:
    match = re.match(
        r"^([A-ZА-ЯЁ][A-Za-zА-Яа-яЁё-]+)\s+(?:должен|должна|должны|нужно|should|must)\b",
        line.strip(),
        flags=re.IGNORECASE,
    )
    return match.group(1) if match else "Unassigned"


def _action_deadline_text(line: str) -> str:
    match = re.search(r"\b(?:до|by)\s+(.+?)(?:[.!?]|$)", line, flags=re.IGNORECASE)
    return match.group(1).strip() if match else "Not specified"


def process_meeting_notes(text: str) -> dict[str, list]:
    lines = [line.strip(" -\t") for line in text.splitlines() if line.strip()]

    decisions: list[str] = []
    actions: list[str] = []
    action_items: list[dict[str, str]] = []
    open_questions: list[str] = []

    for line in lines:
        lowered = line.lower()

        if any(marker in lowered for marker in ["решили", "решение", "договорились", "утвердили", "decided", "agreed"]):
            decisions.append(line)
            continue

        if any(
            marker in lowered
            for marker in [
                "нужно",
                "сделать",
                "подготовить",
                "отправить",
                "проверить",
                "созвониться",
                "написать",
                "должен",
                "должна",
                "should",
                "must",
                "prepare",
                "send",
                "review",
            ]
        ):
            actions.append(line)
            action_items.append(
                {
                    "action": line,
                    "owner": _action_owner(line),
                    "deadline": _action_deadline_text(line),
                }
            )
            continue

        if "?" in line or any(marker in lowered for marker in ["вопрос", "уточнить", "непонятно", "question", "clarify"]):
            open_questions.append(line)

    if not decisions and lines:
        decisions.append("No explicit decision markers found in the demo parser.")
    if not actions and lines:
        possible = [line for line in lines if re.search(r"\b(надо|нужно|должен|должна|should|must)\b", line.lower())]
        actions.extend(possible or ["No explicit action items found in the demo parser."])
        for item in possible:
            action_items.append(
                {
                    "action": item,
                    "owner": _action_owner(item),
                    "deadline": _action_deadline_text(item),
                }
            )
    if not open_questions:
        open_questions.append("No explicit open questions found in the demo parser.")

    return {
        "decisions": decisions,
        "actions": actions,
        "action_items": action_items,
        "open_questions": open_questions,
    }
