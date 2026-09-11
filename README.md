# Nurkhan OS

![tests](https://github.com/Nurkhan-kk/nurkhan-os/actions/workflows/tests.yml/badge.svg)

Nurkhan OS is a lightweight AI Chief of Staff prototype for turning unstructured work and personal inputs into structured actions, decisions, meeting outcomes, project context and focused daily briefs.

The current release is a deterministic **v0.2 operating-model demo**. It works without external APIs so the product flow, approval logic and security boundaries can be inspected before an LLM or real connectors are added.

## Product idea

Most task systems assume the user has already structured the work. Nurkhan OS starts one step earlier: the user writes naturally, and the system decides what deserves to become a task, a waiting item, a decision, a meeting follow-up or simply FYI.

The design goal is to reduce routine coordination and move the user toward decisions, negotiation, strategy and management.

## What the demo shows

- **Inbox**: converts a free-form note into scope, project, priority, deadline, status, category and next action
- **Attention routing**: labels items as FYI, ACTION or DECISION REQUIRED
- **Meetings**: extracts decisions, action items, owners, deadlines, promises, open questions and follow-up
- **Morning Brief**: surfaces priorities, decisions, overdue or stuck work, personal tasks and what can wait
- **Leaving Work Brief**: re-groups unfinished items into practical end-of-day categories
- **Projects**: keeps goal, strategy, metrics, blockers, risks, next actions and decision reasons together
- **Action Guard**: keeps important external actions in draft mode until explicit human approval
- **Official-text guard**: flags prohibited punctuation and selected AI-like phrasing in external business drafts

## Operating principles

1. Natural-language input instead of mandatory forms
2. Explicit Work / Personal separation
3. No invented deadlines
4. `Waiting` for dependencies
5. Decision history stores the reason, not only the outcome
6. Attention is more important than task volume
7. Important external commitments require explicit human approval
8. Retrieved memory and external content are context, not authorization
9. Public demo data stays synthetic

The full operating model is documented in [`docs/PRODUCT_SPEC.md`](docs/PRODUCT_SPEC.md).

## Why v0.2 is deterministic

The first versions intentionally use simple rules instead of an LLM. This makes the product logic easy to inspect, run and test without API keys.

The next stage can place an LLM behind the current interfaces for better extraction and reasoning while leaving scope rules, approval gates and connector permissions deterministic.

## Stack

- Python 3.12+
- Streamlit
- JSON synthetic demo data
- Pytest
- GitHub Actions
- Dependabot

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

The app normally opens at `http://localhost:8501`.

## Run tests

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest -q
```

The same tests run automatically in GitHub Actions on pushes to `main` and on pull requests.

## Repository structure

```text
nurkhan-os/
  app.py
  core/
    brief.py
    demo.py
    guardrails.py
    inbox.py
    meetings.py
    projects.py
  data/
    demo_tasks.json
    demo_projects.json
  examples/
    meeting_notes.txt
  docs/
    ARCHITECTURE.md
    COMPARABLES.md
    DEMO_SCRIPT.md
    PRODUCT_SPEC.md
    SECURITY_AND_PRIVACY.md
  tests/
    test_core.py
  .github/
    dependabot.yml
    workflows/tests.yml
  .env.example
  AGENTS.md
  SECURITY.md
  requirements.txt
  requirements-dev.txt
```

## Security and privacy

This is a public repository. Real business, personal, contractual, financial, medical or communication data must never be committed here.

Secrets also stay out of Git. A future API key should live in environment variables or a secret store, never in source code. `.env` and Streamlit secrets are ignored by Git.

Important external actions are intentionally separated into draft and execute states. The current demo does not send real messages or create real commitments.

Read the threat model and roadmap in [`docs/SECURITY_AND_PRIVACY.md`](docs/SECURITY_AND_PRIVACY.md) and the reporting policy in [`SECURITY.md`](SECURITY.md).

## Comparable projects

The repository has been reviewed against adjacent open-source personal-assistant and memory projects including Khoj, Leon and Mem0. The useful patterns and deliberate differences are summarized in [`docs/COMPARABLES.md`](docs/COMPARABLES.md).

Nurkhan OS remains intentionally smaller. The current goal is to validate the operating model rather than imitate a production-scale assistant architecture.

## Demo walkthrough

A short presentation script is available in [`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md).

## AI-assisted development

Repository rules for AI coding agents are in [`AGENTS.md`](AGENTS.md). The key rules are: synthetic data only, no secret leakage, protected external actions stay gated, and product claims must match actual behavior.

## Roadmap

1. Validate v0.2 locally
2. Add LLM-powered structured extraction behind existing interfaces
3. Add persistent task, project and decision repositories
4. Add authentication and per-user data isolation
5. Add read-only connectors first, then carefully gated write connectors
6. Add audit logging and data retention controls
7. Deploy a public synthetic demo

## Status

**v0.2: operating-model foundation**

This repository is a demo, not a production personal assistant. It intentionally does not yet include authentication, real persistent user data, external message sending or write-capable connectors.

## License

No open-source license has been selected yet. Do not assume permission to reuse or redistribute the code until a license is explicitly added by the repository owner.
