# Nurkhan OS Product Operating Model

This document defines the operating logic behind the public prototype. It is intentionally written with generic project names and synthetic examples so the repository can stay public.

## Product goal

Nurkhan OS is an AI Chief of Staff system designed to reduce manual coordination work and move the user toward decisions, negotiations, strategy and management.

The system should not merely answer messages. It should infer when an input implies a task, decision, reminder, follow-up, project update, meeting preparation need, research need or external action.

## 1. Two operating contexts

All information belongs to one of two contexts:

- **Work**: business projects, meetings, documents, counterparties, strategy, metrics and execution.
- **Personal**: purchases, errands, calls, home tasks, personal meetings and family logistics.

The contexts may be combined for scheduling and daily briefs, but should not be mixed inside project-specific analysis.

## 2. Inbox first

The user should be able to write in natural language without filling a form.

Example:

```text
Позвонить юристу по договору Project Atlas в пятницу
```

The system should infer the task model:

```text
Task
Work / Personal
Project
Priority
Deadline
Context
Owner
Status
Next action
Category
```

Rules:

- Do not invent a deadline when none is stated or unambiguous.
- Detect dependencies and use `Waiting` when another person or event is blocking progress.
- Avoid duplicate tasks when a persistent task registry is connected.
- Update existing tasks when the user says a task is done, cancelled, moved or waiting.

Supported task statuses:

```text
Inbox
To do
In progress
Waiting
Done
Cancelled
```

## 3. Attention model

Every important item should be framed as one of:

- **FYI**: information the user only needs to know.
- **ACTION**: a concrete next action.
- **DECISION REQUIRED**: a question that requires the user's judgment or approval.

This keeps the product focused on attention, not task volume.

## 4. Project context

Each work project should preserve:

- Goal
- Current strategy
- Key metrics
- Economics when relevant
- Counterparties
- Important documents
- Decisions
- Reasons behind decisions
- Open questions
- Risks
- Current tasks
- Owners
- Deadlines
- Blockers
- Recent meetings
- Next actions

Decision history is a first-class object. A previously rejected option should not be proposed again unless circumstances or evidence changed.

## 5. Morning Brief

The Morning Brief should show only what deserves attention now.

Target structure:

1. Today's meetings
2. Main work priorities
3. DECISION REQUIRED
4. Overdue and stuck tasks
5. Important project changes
6. Personal tasks for today
7. What can wait

Future tasks should not be repeated every day unless preparation should already start, the deadline is close, the item is high priority or a blocker has appeared.

## 6. Leaving Work Brief

Before the end of the workday, unfinished tasks should be reorganized into practical groups:

- Before leaving work
- Buy
- Pick up / stop by
- On the way
- At home
- Do not forget
- Move to tomorrow

Completed and cancelled items should not appear.

## 7. Meeting workflow

### Before a meeting

A useful briefing should include:

- Participants
- Company or organization
- Interaction history
- Meeting objective
- Current position
- What may matter to the other side
- What matters to us
- Possible cooperation points
- Risks
- Sensitive topics
- 5 to 7 key questions
- Definition of a good outcome

### After a meeting

The system should extract:

- Decisions
- Action items
- Owners
- Deadlines
- Open questions
- What we promised
- What the other side promised
- Next action
- Follow-up requirement

The extracted result should update project context and the task registry when integrations are connected.

## 8. Research workflow

Research should not stop at summarization. The standard output should separate:

- Facts
- Conclusions
- Opportunities
- Risks
- Recommendations

The key question is: what does this mean for the user's projects, and what can be done with it?

## 9. External messages and commitments

The system may prepare drafts, but it must not independently make important external commitments on the user's behalf.

Explicit approval is required before:

- Strategic decisions
- Financial commitments
- Legal commitments
- Negotiation positions
- External promises
- Important external messages

The product should therefore separate `draft` from `execute` as different permission states.

## 10. Official writing style

External business text should be concise and natural.

Rules for the prototype:

- Avoid bureaucratic filler.
- Avoid generic AI-style phrases.
- Avoid decorative arrows.
- Avoid the long em dash character in official text unless explicitly requested.
- Prefer commas, colons, periods, parentheses or a simple hyphen where needed.
- Check repetitions, grammar and natural Russian before an external draft is considered ready.
- Use cautious wording for external obligations.

## 11. Persistent task registry

A production version should use one authoritative task registry rather than duplicating state across chats and modules.

The public prototype models this as a future `TaskRepository` adapter. Possible backends include a database, spreadsheet or task system.

Expected behavior:

```text
Incoming message
  -> detect task/update
  -> search for existing matching task
  -> create or update
  -> return project + status + next action
```

## 12. Automation principle

When a workflow repeats, the system should propose automation rather than asking the user to keep checking manually.

Examples:

- Daily brief generation
- End-of-day brief generation
- Follow-up after a waiting period
- Deadline checks
- Conditional monitoring

Automations should remain bounded by the same approval rules as interactive actions.

## 13. Product architecture direction

```text
Natural input
  -> Input Router
  -> Structured Task / Meeting / Project Event
  -> Context Store + Task Registry + Decision History
  -> Briefing / Research / Drafting Engines
  -> Action Guard
  -> Connectors
```

The LLM is an interpretation and reasoning layer, not the source of truth for permissions or irreversible actions.

## 14. v0.2 scope

The current public demo includes:

- Free-form Inbox routing
- Work / Personal classification
- Task statuses including Waiting
- FYI / ACTION / DECISION REQUIRED
- Morning Brief
- Leaving Work Brief
- Meeting extraction
- Project decision history
- External action approval gate
- Official-text style guard
- Synthetic demo data only

Not yet implemented:

- Authentication
- Real persistent storage
- Real email/calendar/task connectors
- LLM-backed extraction
- Multi-user access control
- Production audit logs
- Real message sending
