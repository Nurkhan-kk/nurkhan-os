from __future__ import annotations


def summarize_project(project: dict) -> dict[str, object]:
    return {
        "name": project.get("name", "Unnamed project"),
        "goal": project.get("goal", ""),
        "strategy": project.get("strategy", ""),
        "metrics": project.get("metrics", []),
        "risks": project.get("risks", []),
        "blockers": project.get("blockers", []),
        "next_actions": project.get("next_actions", []),
    }
