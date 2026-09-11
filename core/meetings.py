from __future__ import annotations

import re


def process_meeting_notes(text: str) -> dict[str, list[str]]:
    lines = [line.strip(" -\t") for line in text.splitlines() if line.strip()]

    decisions: list[str] = []
    actions: list[str] = []
    open_questions: list[str] = []

    for line in lines:
        lowered = line.lower()

        if any(marker in lowered for marker in ["решили", "решение", "договорились", "утвердили"]):
            decisions.append(line)
            continue

        if any(marker in lowered for marker in ["нужно", "сделать", "подготовить", "отправить", "проверить", "созвониться", "написать"]):
            actions.append(line)
            continue

        if "?" in line or any(marker in lowered for marker in ["вопрос", "уточнить", "непонятно"]):
            open_questions.append(line)

    if not decisions and lines:
        decisions.append("No explicit decision markers found in the demo parser.")
    if not actions and lines:
        possible = [line for line in lines if re.search(r"\b(надо|нужно|должен|должна)\b", line.lower())]
        actions.extend(possible or ["No explicit action items found in the demo parser."])
    if not open_questions:
        open_questions.append("No explicit open questions found in the demo parser.")

    return {
        "decisions": decisions,
        "actions": actions,
        "open_questions": open_questions,
    }
