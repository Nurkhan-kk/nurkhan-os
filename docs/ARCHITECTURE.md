# Architecture

Nurkhan OS v0.2 is intentionally small. The goal is to validate the operating model before adding real connectors, personal data or a large agent framework.

## Core principle

The model may interpret and recommend, but deterministic policy layers own permissions, scope boundaries and protected external actions.

```text
Natural input
  -> Input Router
  -> Structured event
  -> Task / Project / Decision state
  -> Briefing and drafting logic
  -> Action Guard
  -> Connector adapter
```

Connectors are not implemented in the public demo yet.

## Layers

### 1. Interface

`app.py` contains the Streamlit interface and demonstrates:

- Overview
- Inbox
- Meetings
- Morning Brief
- Leaving Work Brief
- Projects
- Action Guard

The interface should orchestrate modules, not become the source of business rules.

### 2. Core logic

The `core/` package contains deterministic prototype logic:

- `inbox.py`: free-form input to structured task draft
- `meetings.py`: decisions, actions, owners, deadlines, promises, open questions and follow-up
- `brief.py`: Morning Brief and Leaving Work Brief grouping
- `projects.py`: project context and decision history
- `guardrails.py`: FYI / ACTION / DECISION REQUIRED, external-action approval and official-text style checks
- `demo.py`: relative synthetic dates so the demo remains current

These modules are intentionally replaceable behind stable interfaces.

### 3. State model

The public demo uses JSON fixtures. A production version should introduce repositories or adapters rather than letting the UI write directly to files.

Target logical stores:

```text
TaskRepository
ProjectRepository
DecisionRepository
MeetingRepository
AutomationRepository
```

Each stored object should have explicit scope and provenance.

Suggested common metadata:

```text
user_id
scope
project_id
source
created_at
updated_at
```

### 4. Approval model

Preparation and execution are different states.

Protected actions include:

- Strategic decisions
- Financial commitments
- Legal commitments
- Negotiation positions
- External promises
- Important external messages

Expected execution flow:

```text
User intent
  -> Draft / recommendation
  -> Policy evaluation
  -> Explicit approval when protected
  -> Connector write
  -> Audit record
```

A retrieved memory, email, webpage, file or model response cannot grant approval.

### 5. Context boundaries

The top-level scope is explicit:

```text
Work
Personal
```

Project analysis should remain inside the relevant scope. A combined view is allowed only where the workflow needs it, for example a daily schedule or brief.

Future retrieval should filter by scope before semantic ranking, not rely on the LLM to ignore unrelated personal context.

### 6. Quality and security layer

The repository includes:

- Pytest coverage for core workflows
- GitHub Actions CI
- Least-privilege workflow permissions
- Dependabot configuration
- `.env.example` without secrets
- `.gitignore` protection for local secrets
- `SECURITY.md`
- `docs/SECURITY_AND_PRIVACY.md`
- `AGENTS.md` for AI-assisted development rules

## Production direction

Add components in this order unless evidence suggests otherwise:

1. Validate v0.2 locally
2. Add LLM-backed structured extraction behind current interfaces
3. Add persistent repositories for tasks, projects and decisions
4. Add authentication and per-user isolation
5. Add connector adapters with separate read/write permissions
6. Add audit logging and retention controls
7. Add background jobs for briefs and follow-ups
8. Add production prompt-injection and connector-safety tests

## What should not be added yet

Do not introduce a vector database, orchestration framework, complex multi-agent runtime or public write-capable deployment solely to make the project look more advanced.

For the current stage, clarity, testability and a credible operating model are more valuable than architectural scale.
