from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from core.brief import build_leaving_work_brief, build_morning_brief
from core.demo import hydrate_demo_tasks
from core.guardrails import check_official_style, external_action_gate
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
        str(value)
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
    attention = result.get("attention", "ACTION")
    if attention == "DECISION REQUIRED":
        st.warning(attention)
    elif attention == "FYI":
        st.info(attention)
    else:
        st.success(attention)

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
    morning_brief = build_morning_brief(tasks)
    leaving_brief = build_leaving_work_brief(tasks)

    with st.sidebar:
        st.title("Nurkhan OS")
        st.caption("AI Chief of Staff prototype")
        st.divider()
        st.markdown("**Demo mode**")
        st.caption("Synthetic data only. No external APIs are connected in v0.1.")
        st.divider()
        st.markdown("**Core principles**")
        st.caption("Natural input, Work / Personal separation, decision focus, human approval for important external actions.")

    st.title("Nurkhan OS")
    st.caption("Turn unstructured inputs into actions, decisions and focused operating context.")

    (
        home_tab,
        inbox_tab,
        meetings_tab,
        morning_tab,
        leaving_tab,
        projects_tab,
        action_guard_tab,
    ) = st.tabs(
        [
            "Overview",
            "Inbox",
            "Meetings",
            "Morning Brief",
            "Leaving Work",
            "Projects",
            "Action Guard",
        ]
    )

    with home_tab:
        st.subheader("Executive overview")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Open demo tasks", len([t for t in tasks if t.get("status") not in {"Done", "Cancelled"}]))
        c2.metric("Priority items", len(morning_brief["work_priorities"]))
        c3.metric("Decisions required", len(morning_brief["decisions"]))
        c4.metric("Active projects", len(projects))

        st.markdown("### Operating model")
        left, right = st.columns(2)
        with left:
            st.markdown("**Capture without forms**")
            st.write("Write naturally. The system infers scope, project, status, priority, deadline, category and next action.")
            st.markdown("**Separate Work and Personal**")
            st.write("Both can contribute to a daily schedule, but project analysis keeps the two contexts separate.")
            st.markdown("**Process meetings into operations**")
            st.write("Extract decisions, actions, owners, deadlines, promises, open questions and follow-up.")
        with right:
            st.markdown("**Surface attention, not task volume**")
            st.write("Use FYI, ACTION and DECISION REQUIRED to show what actually needs attention.")
            st.markdown("**Preserve decision history**")
            st.write("Store not only what was decided, but why it was decided, so rejected options are not recycled without new evidence.")
            st.markdown("**Gate important external actions**")
            st.write("Strategic, financial, legal, negotiation and important external-message actions stay draft-only until explicit human approval.")

        st.info("v0.1 is intentionally deterministic. The next version can replace demo rules with an LLM layer without changing the operating model.")

    with inbox_tab:
        st.subheader("Inbox")
        st.write("Capture a task, commitment, reminder, waiting item or decision in free form.")
        sample = "Позвонить юристу по договору Project Atlas в пятницу"
        text = st.text_area("New input", value=sample, height=120, key="inbox_input")
        if st.button("Structure task", type="primary", key="structure_task"):
            result = parse_inbox(text)
            render_task_draft(result)
            with st.expander("Raw structured data"):
                st.json(result)

    with meetings_tab:
        st.subheader("Meeting Processor")
        st.write("Turn rough notes into decisions, action items, promises, open questions and a follow-up path.")
        sample_path = BASE_DIR / "examples/meeting_notes.txt"
        sample_notes = sample_path.read_text(encoding="utf-8")
        notes = st.text_area("Meeting notes", value=sample_notes, height=260, key="meeting_notes")
        if st.button("Process meeting", type="primary", key="process_meeting"):
            result = process_meeting_notes(notes)

            left, right = st.columns(2)
            with left:
                st.markdown("### Decisions")
                for item in result["decisions"]:
                    st.write(f"- {item}")
                st.markdown("### Open questions")
                for item in result["open_questions"]:
                    st.write(f"- {item}")
            with right:
                st.markdown("### Action items")
                if not result["action_items"]:
                    for item in result["actions"]:
                        st.write(f"- {item}")
                for item in result["action_items"]:
                    with st.container(border=True):
                        st.markdown(f"**{item['action']}**")
                        st.caption(f"Owner: {item['owner']} | Deadline: {item['deadline']}")

            promise_left, promise_right = st.columns(2)
            with promise_left:
                st.markdown("### What we promised")
                if not result["our_promises"]:
                    st.caption("No explicit promise detected.")
                for item in result["our_promises"]:
                    st.write(f"- {item}")
            with promise_right:
                st.markdown("### What the other side promised")
                if not result["other_side_promises"]:
                    st.caption("No explicit promise detected.")
                for item in result["other_side_promises"]:
                    st.write(f"- {item}")

            st.markdown("### Follow-up")
            st.write(f"Next action: {result['next_action']}")
            st.write(f"Follow-up required: {'Yes' if result['follow_up_required'] else 'No'}")

    with morning_tab:
        st.subheader("Morning Brief")
        st.write("A focused view of what deserves attention today. Demo data is synthetic and uses relative dates.")

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
                if not morning_brief[key]:
                    st.caption("Nothing here in the demo dataset.")
                for task in morning_brief[key]:
                    render_task(task)

    with leaving_tab:
        st.subheader("Leaving Work Brief")
        st.write("Re-group unfinished tasks by what is useful to remember before leaving work.")
        sections = [
            ("Before leaving work", "before_leaving_work"),
            ("Buy", "buy"),
            ("Pick up / stop by", "pick_up_or_stop_by"),
            ("On the way", "on_the_way"),
            ("At home", "at_home"),
            ("Do not forget", "dont_forget"),
            ("Move to tomorrow", "move_to_tomorrow"),
        ]
        for title, key in sections:
            items = leaving_brief[key]
            if not items:
                continue
            with st.container(border=True):
                st.markdown(f"### {title}")
                for task in items:
                    render_task(task)

    with projects_tab:
        st.subheader("Project Context")
        st.write("Keep the minimum context needed for decisions, follow-up and continuity.")
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

        st.markdown("### Decision history")
        if not summary["decisions"]:
            st.caption("No recorded decisions in the demo project.")
        for decision in summary["decisions"]:
            with st.container(border=True):
                st.markdown(f"**{decision.get('date', '')} - {decision.get('decision', '')}**")
                st.caption(f"Reason: {decision.get('reason', '')}")

    with action_guard_tab:
        st.subheader("Action Guard")
        st.write("Important external actions are prepared first and executed only after explicit approval.")

        action_type = st.selectbox(
            "Action type",
            [
                "external_message",
                "strategic_decision",
                "financial_commitment",
                "legal_commitment",
                "negotiation_position",
                "external_promise",
            ],
        )
        important_message = st.checkbox("Important external message", value=True)
        explicit_approval = st.checkbox("Explicit human approval received", value=False)
        message = st.text_area(
            "Draft message",
            value="Добрый день. Подтверждаем, что получили материалы. Вернемся с ответом после внутренней проверки.",
            height=140,
        )

        gate = external_action_gate(
            action_type=action_type,
            explicit_approval=explicit_approval,
            important_external_message=important_message,
        )
        style_issues = check_official_style(message)

        gate_col, style_col = st.columns(2)
        with gate_col:
            st.markdown("### Execution gate")
            if gate["approval_required"]:
                st.warning("Draft only. Approval required before execution.")
            else:
                st.success("Execution allowed by the demo policy.")
            st.caption(gate["reason"])
        with style_col:
            st.markdown("### Official-text check")
            if style_issues:
                for issue in style_issues:
                    st.error(issue)
            else:
                st.success("No prohibited style patterns detected.")

        st.caption("This demo does not send messages or create real commitments.")

    st.divider()
    st.caption("Public demo repository. Synthetic data only. v0.2 operating-model foundation")


if __name__ == "__main__":
    main()
