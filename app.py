from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from core.brief import build_morning_brief
from core.demo import hydrate_demo_tasks
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


def render_task_draft(result: dict) -> None:
    left, right = st.columns(2)
    with left:
        st.markdown("**Task**")
        st.write(result.get("task", ""))
        st.markdown("**Scope / Project**")
        st.write(f"{result.get('scope', '')} / {result.get('project', '')}")
        st.markdown("**Priority / Deadline**")
        deadline = result.get("deadline") or "Not set"
        st.write(f"{result.get('priority', '')} / {deadline}")
    with right:
        st.markdown("**Status / Owner**")
        st.write(f"{result.get('status', '')} / {result.get('owner', '')}")
        st.markdown("**Category**")
        st.write(result.get("category", ""))
        st.markdown("**Next action**")
        st.write(result.get("next_action", ""))


def main() -> None:
    st.set_page_config(page_title="Nurkhan OS", page_icon="N", layout="wide")

    tasks = hydrate_demo_tasks(load_json("data/demo_tasks.json"))
    projects = load_json("data/demo_projects.json")
    brief = build_morning_brief(tasks)

    with st.sidebar:
        st.title("Nurkhan OS")
        st.caption("AI Chief of Staff prototype")
        st.divider()
        st.markdown("**Demo mode**")
        st.caption("Synthetic data only. No external APIs are connected in v0.1.")
        st.divider()
        st.markdown("**Prototype scope**")
        st.caption("Inbox, meetings, daily brief and project context.")

    st.title("Nurkhan OS")
    st.caption("Turn unstructured inputs into actions, decisions and focused daily context.")

    home_tab, inbox_tab, meetings_tab, brief_tab, projects_tab = st.tabs(
        ["Overview", "Inbox", "Meetings", "Morning Brief", "Projects"]
    )

    with home_tab:
        st.subheader("Executive overview")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Open demo tasks", len([t for t in tasks if t.get("status") not in {"Done", "Cancelled"}]))
        c2.metric("Priority items", len(brief["work_priorities"]))
        c3.metric("Decisions required", len(brief["decisions"]))
        c4.metric("Active projects", len(projects))

        st.markdown("### What this prototype demonstrates")
        left, right = st.columns(2)
        with left:
            st.markdown("**Capture and structure**")
            st.write("Convert a free-form task into scope, project, priority, deadline, status and next action.")
            st.markdown("**Process meetings**")
            st.write("Extract explicit decisions, action items and open questions from notes.")
        with right:
            st.markdown("**Focus the day**")
            st.write("Separate priorities, decisions, overdue items, personal tasks and work that can wait.")
            st.markdown("**Keep project context**")
            st.write("Show goal, strategy, metrics, blockers, risks and next actions in one view.")

        st.info("v0.1 is intentionally deterministic. The next version will replace demo rules with an LLM layer after the product flow is validated.")

    with inbox_tab:
        st.subheader("Inbox")
        st.write("Write a task naturally. The prototype turns it into a structured task draft.")
        sample = "Позвонить юристам по договору OFD в пятницу"
        text = st.text_area("New input", value=sample, height=120, key="inbox_input")
        if st.button("Structure task", type="primary", key="structure_task"):
            result = parse_inbox(text)
            st.success("Structured draft created")
            render_task_draft(result)
            with st.expander("Raw structured data"):
                st.json(result)

    with meetings_tab:
        st.subheader("Meeting Processor")
        st.write("Paste rough meeting notes. The prototype separates what was decided, what needs to happen and what remains open.")
        sample_path = BASE_DIR / "examples/meeting_notes.txt"
        sample_notes = sample_path.read_text(encoding="utf-8")
        notes = st.text_area("Meeting notes", value=sample_notes, height=240, key="meeting_notes")
        if st.button("Process meeting", type="primary", key="process_meeting"):
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
        st.write("A focused view of what deserves attention today. Demo data is synthetic and uses relative dates so the scenario stays fresh.")

        sections = [
            ("Main work priorities", "work_priorities"),
            ("Decision required", "decisions"),
            ("Overdue / stuck", "overdue"),
            ("Personal today", "personal"),
            ("Can wait", "can_wait"),
        ]

        for title, key in sections:
            with st.container(border=True):
                st.markdown(f"### {title}")
                if not brief[key]:
                    st.caption("Nothing here in the demo dataset.")
                for task in brief[key]:
                    render_task(task)

    with projects_tab:
        st.subheader("Project Context")
        st.write("One compact place for the context needed to make the next decision.")
        names = [project["name"] for project in projects]
        selected = st.selectbox("Project", names)
        project = next(item for item in projects if item["name"] == selected)
        summary = summarize_project(project)

        st.markdown(f"### {summary['name']}")
        goal_col, strategy_col = st.columns(2)
        with goal_col:
            with st.container(border=True):
                st.markdown("**Goal**")
                st.write(summary["goal"])
        with strategy_col:
            with st.container(border=True):
                st.markdown("**Strategy**")
                st.write(summary["strategy"])

        left, right = st.columns(2)
        with left:
            with st.container(border=True):
                st.markdown("**Metrics**")
                for item in summary["metrics"]:
                    st.write(f"- {item}")
            with st.container(border=True):
                st.markdown("**Blockers**")
                for item in summary["blockers"] or ["No blockers"]:
                    st.write(f"- {item}")
        with right:
            with st.container(border=True):
                st.markdown("**Risks**")
                for item in summary["risks"]:
                    st.write(f"- {item}")
            with st.container(border=True):
                st.markdown("**Next actions**")
                for item in summary["next_actions"]:
                    st.write(f"- {item}")

    st.divider()
    st.caption("Public demo repository. Synthetic data only. v0.1")


if __name__ == "__main__":
    main()
