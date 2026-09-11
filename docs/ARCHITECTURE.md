# Architecture

Nurkhan OS v0.1 is intentionally small. The goal is to validate the operating model before adding external services.

## Layers

### 1. Interface

`app.py` contains the Streamlit interface and presents five views:

- Overview
- Inbox
- Meetings
- Morning Brief
- Projects

The interface does not contain business rules beyond presentation and basic orchestration.

### 2. Core logic

The `core/` package contains deterministic prototype logic:

- `inbox.py` turns free-form input into a task draft
- `meetings.py` extracts decisions, action items, owners, deadlines and open questions
- `brief.py` prioritizes demo tasks into a focused Morning Brief
- `projects.py` exposes compact project context and decision history
- `demo.py` resolves relative demo dates so the scenario remains current

These modules are intentionally replaceable. A future LLM service can sit behind the same interface without changing the product workflow.

### 3. Demo data

`data/` contains synthetic project and task scenarios. No real user data belongs in the public repository.

### 4. Quality layer

`tests/` covers the core flows. GitHub Actions runs the tests automatically on pushes and pull requests.

## Intended production direction

A production version would add these components gradually:

1. LLM service for natural-language parsing and summarization
2. Persistent task and project storage
3. Authentication and per-user data isolation
4. Integration adapters for calendar, email and task systems
5. Audit-friendly decision history
6. Background jobs for briefs and follow-ups

## Design principle

The system should reduce manual structuring. A user should be able to provide raw context in natural language and receive a small number of clear outputs:

- FYI
- ACTION
- DECISION REQUIRED

The product should preserve the reason behind important project decisions so rejected ideas are not repeatedly proposed without new evidence.
