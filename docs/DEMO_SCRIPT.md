# Demo walkthrough

This is a short walkthrough for showing Nurkhan OS to another person in about three minutes.

## 1. Overview

Open the app on **Overview**.

Explain the product in one sentence:

> Nurkhan OS is an AI Chief of Staff prototype that turns raw tasks, meeting notes and project context into structured actions, decisions and daily focus.

Point out the operating principles:

- Work / Personal separation
- FYI / ACTION / DECISION REQUIRED
- Waiting-state tracking
- Decision history with reasons
- Human approval before important external actions

All visible data is synthetic.

## 2. Inbox

Open **Inbox** and use the pre-filled example.

Click **Structure task**.

Show that a natural-language note becomes:

- scope
- project
- priority
- deadline
- status
- owner
- category
- attention type
- next action

Mention that the parser does not invent a deadline when one is not stated.

Then try a waiting example:

```text
Ждем ответ от клиента по договору Project Atlas
```

Show that the status becomes `Waiting`.

## 3. Meetings

Open **Meetings** and process the sample notes.

Show how the notes are split into:

- decisions
- action items
- owners
- deadlines
- open questions
- what we promised
- what the other side promised
- next action
- follow-up requirement

Explain that the current parser is deterministic and will later be replaced by an LLM-backed extractor behind the same interface.

## 4. Morning Brief

Open **Morning Brief**.

Show that the system separates:

- main work priorities
- decisions required
- overdue or stuck items
- personal tasks for today
- work that can wait

The point is not to show every task. It is to reduce attention load.

## 5. Leaving Work Brief

Open **Leaving Work**.

Show that the same unfinished tasks are reorganized around execution before the user leaves work:

- before leaving work
- buy
- pick up / stop by
- on the way
- at home
- do not forget
- move to tomorrow

This demonstrates that one task registry can produce different operational views without duplicating tasks.

## 6. Projects

Open **Projects** and select Project Atlas.

Show goal, strategy, metrics, blockers, risks and next actions.

Finish with **Decision history**. The system keeps not only what was decided, but why it was decided.

## 7. Action Guard

Open **Action Guard**.

Keep **Important external message** enabled and leave approval unchecked.

Show that the system remains in **draft only** mode.

Then enable explicit approval and show the policy change.

Paste a draft containing a long em dash or decorative arrow to demonstrate the official-text style check.

Clarify that the public demo never actually sends a message.

## Closing line

> v0.2 validates the operating model, attention routing and approval boundaries. The next step is to add LLM-backed extraction and persistent storage without weakening those boundaries.
