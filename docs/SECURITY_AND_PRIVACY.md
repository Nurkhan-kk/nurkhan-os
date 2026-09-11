# Security and Privacy Model

Nurkhan OS is currently a public demonstration project, not a production assistant. The security model below defines the rules that should remain true as the prototype evolves.

## Security goals

1. Keep real personal and business data out of the public repository.
2. Keep credentials and API keys out of Git history.
3. Prevent retrieved context, model output or external content from authorizing sensitive actions by itself.
4. Require explicit human approval for important external commitments.
5. Keep Work and Personal context separated except where a combined schedule or daily brief explicitly needs both.
6. Make future connectors use the minimum permissions required.

## Current public-demo boundary

The repository contains synthetic data only. It must not contain:

- Real business records
- Client or counterparty correspondence
- Contracts
- Financial data
- Medical data
- Personal schedules
- Real meeting transcripts
- Real task lists
- Passwords, API keys, tokens or private keys

The current app does not send email, change calendars, create financial obligations or execute external commitments.

## Secrets

Secrets must live outside source control.

Allowed patterns include:

- Environment variables
- A local `.env` file that is ignored by Git
- Streamlit secrets stored outside the repository
- A deployment platform's secret manager

The repository includes `.env.example` only as a placeholder. Real values must never be committed.

For a public GitHub repository, secret scanning is an important additional defense. Push protection should also remain enabled where available.

References:

- https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning
- https://docs.github.com/en/code-security/concepts/secret-security/push-protection
- https://docs.streamlit.io/deploy/concepts/secrets

## Data separation

The product treats data scope as an explicit field rather than relying on the model to remember boundaries.

Primary scopes:

```text
Work
Personal
```

Future storage should additionally scope records by project, user and source.

Example:

```text
user_id
scope
project_id
record_type
source
created_at
updated_at
```

A Work project query should not retrieve Personal context unless the workflow explicitly requires a combined schedule or brief.

## Memory is a trust boundary

Long-term memory improves continuity but can also propagate stale, incorrect or malicious instructions.

Therefore:

- Retrieved memory is context, not authorization.
- Memory must not override current explicit user intent.
- An old instruction must not silently authorize a new protected action.
- External content must not be allowed to modify approval rules.
- High-impact actions should re-check current permission immediately before execution.
- Project decisions should record source and reason so later reasoning can distinguish fact from interpretation.

This direction is consistent with current research that treats personal-agent memory as a security boundary rather than only a retrieval feature.

Reference:

- https://arxiv.org/abs/2606.06054

## External action approval

The `Action Guard` separates preparation from execution.

The following categories require explicit human approval before execution:

- Strategic decision
- Financial commitment
- Legal commitment
- Negotiation position
- External promise
- Important external message

A model may draft, summarize or recommend. It may not treat its own recommendation as approval.

Expected flow:

```text
Intent
  -> Draft / Recommendation
  -> Policy check
  -> Human approval when required
  -> Connector execution
  -> Audit record
```

## Connector security

Future Gmail, Calendar, Drive or task-system connectors should follow least privilege.

Rules:

- Request only permissions needed for the workflow.
- Prefer read-only access when a write is not needed.
- Separate read tools from write tools.
- Re-check approval immediately before protected writes.
- Do not pass unnecessary context to external services.
- Log the type of action and result, but redact secrets and sensitive payloads.

## Prompt injection and untrusted content

Email, webpages, files and meeting transcripts may contain instructions that were not written by the user.

Treat these sources as untrusted data.

An external document must not be able to:

- Change system approval rules
- Request secrets
- Trigger connector writes on its own
- Expand connector permissions
- Move data between Work and Personal scopes without a legitimate workflow reason

## Logging

Production logs should avoid storing full sensitive payloads by default.

Prefer structured metadata such as:

```text
action_type
connector
approval_state
record_id
status
timestamp
```

If message bodies or documents are needed for debugging, use explicit debug controls, short retention and access restrictions.

## Authentication and multi-user use

The current demo has no authentication and must not be exposed with real personal data.

Before production use, add:

- User authentication
- Authorization checks
- Per-user storage boundaries
- Session security
- Connector-account binding
- Audit logging
- Secure deletion and retention controls

## Dependency and CI security

The repository runs tests in GitHub Actions with read-only repository-content permission. Dependabot is configured for Python and GitHub Actions dependency updates.

Further hardening should add a deliberate vulnerability-review or blocking policy once the project begins using real data or more dependencies.

Do not add a dependency merely because it is convenient. Prefer a small dependency surface for a personal assistant with access to sensitive data.

## Deployment

A public demo deployment must continue to use synthetic data only.

A private personal deployment should:

- Require authentication before exposing any real data
- Use HTTPS
- Store secrets in a secret manager
- Avoid publicly reachable administrative interfaces
- Keep backups encrypted when sensitive state is persisted
- Define retention and deletion behavior

## Known gaps in v0.2

The current repository intentionally does not claim production readiness. It currently lacks:

- Authentication
- Encryption-at-rest design
- Production database
- Connector permission model
- Full audit log
- Data deletion workflow
- Prompt-injection test suite
- Dedicated dependency vulnerability enforcement beyond automated update checks
- Rate limiting

These are roadmap items, not hidden assumptions.
