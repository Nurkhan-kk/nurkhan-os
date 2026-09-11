# Nurkhan OS

![tests](https://github.com/Nurkhan-kk/nurkhan-os/actions/workflows/tests.yml/badge.svg)

Nurkhan OS is a lightweight AI Chief of Staff prototype for turning unstructured work and personal inputs into structured actions, meeting outcomes, project context and focused daily briefs.

The current release is a deterministic v0.1 demo. It works without external APIs so the product flow can be tested first. The next stage is to add an LLM layer while keeping the same operating model.

## Product idea

Most task systems assume the user already knows how to structure information. Nurkhan OS starts one step earlier: the user writes naturally, and the system turns raw input into operational context.

The prototype demonstrates four core workflows:

- **Inbox**: converts a free-form note into a structured task draft
- **Meetings**: separates decisions, action items and open questions from rough notes
- **Morning Brief**: highlights priorities, decisions required, overdue items, personal tasks and work that can wait
- **Projects**: keeps goal, strategy, metrics, blockers, risks and next actions in one compact view

## Why v0.1 is deterministic

The first version intentionally uses simple rules instead of an LLM. This makes the product flow easy to inspect, run and test without API keys. Once the UX is validated, the deterministic parsers can be replaced by model-backed services without changing the user-facing workflow.

## Stack

- Python 3.12+
- Streamlit
- JSON demo data
- Pytest
- GitHub Actions

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

On Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The app opens in your browser, usually at `http://localhost:8501`.

## Run tests

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest -q
```

The same tests also run automatically on GitHub Actions after pushes to `main` and on pull requests.

## Repository structure

```text
nurkhan-os/
  app.py
  core/
    brief.py
    demo.py
    inbox.py
    meetings.py
    projects.py
  data/
    demo_tasks.json
    demo_projects.json
  examples/
    meeting_notes.txt
  tests/
    test_core.py
  .github/workflows/
    tests.yml
  .env.example
  requirements.txt
  requirements-dev.txt
```

## Demo data

All scenarios are synthetic. Demo deadlines use relative tokens such as `TODAY`, `TOMORROW` and `OVERDUE_2`, which are resolved at runtime so the Morning Brief stays meaningful regardless of when the repository is opened.

## Privacy

This is a public repository. Real business, personal, contractual, financial, medical or communication data should never be committed here. The repository contains only synthetic examples.

Secrets must also stay out of Git. A future API key should live in a local `.env` or secret store, never in source code. `.env` and Streamlit secrets are already ignored by Git.

## Roadmap

1. Validate the v0.1 UX locally
2. Add LLM-powered Inbox and Meeting parsing
3. Add persistent storage
4. Add a structured decision history for projects
5. Add optional calendar, email and task integrations
6. Deploy a public demo

## Status

**v0.1: demo-ready foundation**

The current goal is not to be a full production assistant. It is to demonstrate a clear product concept with working flows, readable code, tests and safe public demo data.
