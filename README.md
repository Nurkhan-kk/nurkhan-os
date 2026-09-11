# Nurkhan OS

Nurkhan OS is a small AI Chief of Staff prototype for turning unstructured work and personal inputs into structured actions, meeting outcomes, project context and daily briefs.

The current version is a deterministic demo that works without external APIs. It is designed to show the product flow first. An LLM layer can be added later.

## What it does

- Inbox: converts a free-form note into a structured task draft
- Meetings: extracts decisions, action items and open questions from meeting notes
- Morning Brief: highlights priorities, decisions required, overdue items and personal tasks
- Projects: shows compact context for active projects

## Demo stack

- Python
- Streamlit
- JSON demo data

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

On Windows, activate the environment with:

```bash
.venv\Scripts\activate
```

## Repository structure

```text
nurkhan-os/
  app.py
  core/
    inbox.py
    meetings.py
    brief.py
    projects.py
  data/
    demo_tasks.json
    demo_projects.json
  examples/
    meeting_notes.txt
```

## Privacy

This public repository contains demo data only. Real business, personal, contractual and communication data should never be committed to the repository.

## Next steps

1. Add LLM-powered parsing for inbox and meetings
2. Add persistent storage
3. Add authentication
4. Add integrations for calendar, email and task systems
5. Deploy a public demo
