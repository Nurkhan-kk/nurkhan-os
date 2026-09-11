from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from core.brief import build_morning_brief
from core.inbox import parse_inbox
from core.meetings import process_meeting_notes
from core.projects import summarize_project


BASE_DIR = Path(__file__).parent


@st.cache_data
def load_json(relative_path: str):
    with open(BASE_DIR / relative_path, "r", encoding="utf-8") as file:
        return json.load(file)


def render_task(task: dict) -> None:
    title = task.get("task", "Untitled task")
    meta = " | ".join(
        value
        for value in [
            task.get("scope", ""),
            task.get("project", ""),
            task.get("priority", ""),
            task.get("deadline", ""),
            task.get("status", ""),
        ]
        if value
    )
    st.markdown(f"**{title}**")
    if meta:
        st.caption(meta)


def main() -> None:
    st.set_page_config(page_title="Nurkhan OS", page_icon="🧭", layout="wide")

    st.title("Nurkhan OS")
    st.caption("AI Chief of Staff prototype for tasks, meetings, project context and daily briefs")

    inbox_tab, meetings_tab, brief_tab, projects_tab = st.tabs(
        ["Inbox", "Meetings", "Morning Brief", "Projects"]
    )

    with inbox_tab:
        st.subheader("Inbox")
        st.write("Write a task in natural language. The demo parser converts it into a structured draft.")
        sample = "Позвонить юристам по договору OFD в пятницу"
        text = st.text_area("New input", value=sample, height=120)
        if st.button("Structure task", type="primary"):
            result = parse_inbox(text)
            st.success("Task draft created")
            st.json(result)

    with meetings_tab:
        st.subheader("Meeting Processor")
        sample_path = BASE_DIR / "examples/meeting_notes.txt"
        sample_notes = sample_path.read_text(encoding="utf-8")
        notes = st.text_area("Meeting notes", value=sample_notes, height=220)
        if st.button("Process meeting"):
            result = process_meeting_notes(notes)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("### Decisions")
                for item in result["decisions"]:
                    st.write(f"- {item}")
            with col2:
                st.markdown("### Action items")
                for item in result["actions"]:
                    st.write(f"- {item}")
            with col3:
                st.markdown("### Open questions")
                for item in result["open_questions"]:
                    st.write(f"- {item}")

    with brief_tab:
        st.subheader("Morning Brief")
        tasks = load_json("data/demo_tasks.json")
        brief = build_morning_brief(tasks)

        sections = [
            ("Main work priorities", "work_priorities"),
            ("Decision required", "decisions"),
            ("Overdue / stuck", "overdue"),
            ("Personal today", "personal"),
            ("Can wait", "can_wait"),
        ]

        for title, key in sections:
            st.markdown(f"### {title}")
            if not brief[key]:
                st.caption("Nothing here in the demo dataset.")
            for task in brief[key]:
                render_task(task)

    with projects_tab:
        st.subheader("Project Context")
        projects = load_json("data/demo_projects.json")
        names = [project["name"] for project in projects]
        selected = st.selectbox("Project", names)
        project = next(item for item in projects if item["name"] == selected)
        summary = summarize_project(project)

        st.markdown(f"### {summary['name']}")
        st.markdown("**Goal**")
        st.write(summary["goal"])
        st.markdown("**Strategy**")
        st.write(summary["strategy"])

        left, right = st.columns(2)
        with left:
            st.markdown("**Metrics**")
            for item in summary["metrics"]:
                st.write(f"- {item}")
            st.markdown("**Blockers**")
            for item in summary["blockers"] or ["No blockers"]:
                st.write(f"- {item}")
        with right:
            st.markdown("**Risks**")
            for item in summary["risks"]:
                st.write(f"- {item}")
            st.markdown("**Next actions**")
            for item in summary["next_actions"]:
                st.write(f"- {item}")

    st.divider()
    st.caption("Public demo repository. Uses synthetic data only.")


if __name__ == "__main__":
    main()
