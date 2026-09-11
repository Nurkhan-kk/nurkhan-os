from __future__ import annotations

from dataclasses import asdict, dataclass


PROHIBITED_OFFICIAL_SYMBOLS = {
    "—": "Use a comma, colon, period, parentheses or a simple hyphen instead of an em dash.",
    "→": "Avoid decorative arrows in official text.",
    "⇒": "Avoid decorative arrows in official text.",
    "➜": "Avoid decorative arrows in official text.",
}


@dataclass
class ActionGate:
    attention: str
    approval_required: bool
    allowed_mode: str
    reason: str


def classify_attention(*, decision_required: bool = False, action_required: bool = True) -> str:
    if decision_required:
        return "DECISION REQUIRED"
    if action_required:
        return "ACTION"
    return "FYI"


def external_action_gate(
    *,
    action_type: str,
    explicit_approval: bool = False,
    creates_commitment: bool = False,
    important_external_message: bool = False,
) -> dict[str, object]:
    protected_types = {
        "strategic_decision",
        "financial_commitment",
        "legal_commitment",
        "negotiation_position",
        "external_promise",
    }
    protected = action_type in protected_types or creates_commitment or important_external_message

    if protected and not explicit_approval:
        gate = ActionGate(
            attention="DECISION REQUIRED",
            approval_required=True,
            allowed_mode="draft_only",
            reason="Human approval is required before an important external action or commitment.",
        )
        return asdict(gate)

    gate = ActionGate(
        attention="ACTION",
        approval_required=False,
        allowed_mode="execute",
        reason="The action is approved or does not create a protected external commitment.",
    )
    return asdict(gate)


def check_official_style(text: str) -> list[str]:
    issues: list[str] = []
    for symbol, message in PROHIBITED_OFFICIAL_SYMBOLS.items():
        if symbol in text:
            issues.append(message)

    lowered = text.lower()
    ai_like_phrases = [
        "надеюсь, это письмо застало вас в добром здравии",
        "i hope this email finds you well",
        "в рамках вышеизложенного",
    ]
    for phrase in ai_like_phrases:
        if phrase in lowered:
            issues.append("Rewrite generic or overly formal AI-like phrasing in a natural business style.")
            break

    return issues
