from __future__ import annotations

import re


def _action_owner(line: str) -> str:
    match = re.match(
        r"^([A-ZА-ЯЁ][A-Za-zА-Яа-яЁё-]+)\s+(?:должен|должна|должны|нужно|should|must|will|подготовим|отправим|проверим|подготовит|отправит|проверит|вернемся|вернёмся|вернется|вернётся)\b",
        line.strip(),
        flags=re.IGNORECASE,
    )
    return match.group(1) if match else "Unassigned"


def _action_deadline_text(line: str) -> str:
    match = re.search(r"\b(?:до|by)\s+(.+?)(?:[.!?]|$)", line, flags=re.IGNORECASE)
    return match.group(1).strip() if match else "Not specified"


def _is_our_promise(lowered: str) -> bool:
    return any(
        marker in lowered
        for marker in [
            "мы должны",
            "мы подготовим",
            "мы отправим",
            "мы проверим",
            "мы вернемся",
            "мы вернёмся",
            "we will",
            "our team will",
        ]
    )


def _is_other_side_promise(lowered: str) -> bool:
    parties = ["клиент", "партнер", "партнёр", "контрагент", "customer", "partner", "vendor"]
    commitments = ["отправит", "подготовит", "проверит", "вернется", "вернётся", "will send", "will prepare", "will review"]
    return any(party in lowered for party in parties) and any(commitment in lowered for commitment in commitments)


def process_meeting_notes(text: str) -> dict[str, object]:
    lines = [line.strip(" -\t") for line in text.splitlines() if line.strip()]

    decisions: list[str] = []
    actions: list[str] = []
    action_items: list[dict[str, str]] = []
    open_questions: list[str] = []
    our_promises: list[str] = []
    other_side_promises: list[str] = []

    action_markers = [
        "нужно",
        "сделать",
        "подготовить",
        "подготовим",
        "подготовит",
        "отправить",
        "отправим",
        "отправит",
        "проверить",
        "проверим",
        "проверит",
        "созвониться",
        "написать",
        "должен",
        "должна",
        "должны",
        "вернемся",
        "вернёмся",
        "вернется",
        "вернётся",
        "should",
        "must",
        "prepare",
        "send",
        "review",
        "will",
    ]

    for line in lines:
        lowered = line.lower()

        if _is_our_promise(lowered):
            our_promises.append(line)
        if _is_other_side_promise(lowered):
            other_side_promises.append(line)

        if any(marker in lowered for marker in ["решили", "решение", "договорились", "утвердили", "decided", "agreed"]):
            decisions.append(line)
            continue

        if any(marker in lowered for marker in action_markers):
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

    next_action = "No next action identified."
    if action_items:
        next_action = action_items[0]["action"]
    elif open_questions and not open_questions[0].startswith("No explicit"):
        next_action = f"Resolve: {open_questions[0]}"

    return {
        "decisions": decisions,
        "actions": actions,
        "action_items": action_items,
        "open_questions": open_questions,
        "our_promises": our_promises,
        "other_side_promises": other_side_promises,
        "next_action": next_action,
        "follow_up_required": bool(action_items or our_promises or other_side_promises),
    }
