# Security Review

Review date: 2026-09-11

This review covers the public prototype repository only. It is not a penetration test and does not claim production readiness.

## Result

No intentional real user, company, counterparty or credential data is required by the current demo.

The repository is suitable to continue as a **synthetic public prototype**, subject to the known limitations documented below.

## Checks performed

### Sensitive project and identity leakage

Repository code search was checked for known private-context project/company identifiers and the connected personal email address used during development.

No matches were found for the reviewed private identifiers.

The public demo continues to use synthetic names such as:

- Project Atlas
- Client Portal

### Common credential patterns

Repository code search was checked for common credential fragments including:

- OpenAI-style `sk-` prefixes
- GitHub `ghp_` prefixes
- Google `AIza` prefixes
- Private-key header text

No matching committed credentials were found in the reviewed default branch.

`.env.example` contains an empty placeholder only.

### Git ignore rules

`.gitignore` excludes:

- `.env` and local environment variants
- Streamlit secrets
- Python virtual environments and caches
- Local database files
- Future `local_data/` and `private_data/` directories

### CI permissions

The test workflow explicitly requests only:

```yaml
permissions:
  contents: read
```

This reduces the default GitHub Actions token permissions for the current CI job.

### Dependency maintenance

Dependabot is configured for:

- Python dependencies
- GitHub Actions dependencies

This does not replace vulnerability review, but it reduces the chance that dependencies silently remain stale.

### Human approval gate

The application models protected external actions as draft-only until explicit human approval.

Protected categories include strategic, financial, legal, negotiation, promise and important-message actions.

The current public demo has no real write connector, so the approval rule cannot be bypassed into a real email/calendar/financial action inside this version.

### Work / Personal separation

The task model carries explicit scope. Product and security documentation require future storage and retrieval to filter by scope before model reasoning.

This is a design requirement, not yet a production access-control implementation.

## Security controls now present

- Synthetic public demo data
- No real connector writes
- `.env.example` without credentials
- Hardened `.gitignore`
- GitHub Actions tests
- Read-only CI token permissions
- Dependabot
- `SECURITY.md`
- Detailed security and privacy model
- AI-agent repository rules in `AGENTS.md`
- Human approval guard
- Official-message style guard
- Tests covering approval behavior

## GitHub settings to verify manually

Some protections are repository/account settings rather than source files and cannot be guaranteed by this code review.

Recommended GitHub settings:

1. Confirm **Secret scanning** is active for the public repository.
2. Confirm **Push protection** is enabled at the account or repository level where available.
3. Review Dependabot alerts when they appear.
4. Consider branch protection with required CI checks once the repository stops being edited rapidly during prototyping.
5. Enable private vulnerability reporting if available.

GitHub references:

- https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning
- https://docs.github.com/en/code-security/concepts/secret-security/push-protection
- https://docs.github.com/en/code-security/getting-started/quickstart-for-securing-your-repository

## Known limitations before real-data use

Do not connect real personal or business data to a publicly accessible deployment until at least the following exist:

- Authentication
- Per-user authorization
- Secure persistent storage
- Connector account binding
- Audit logs
- Retention and deletion rules
- Prompt-injection tests
- Connector write-policy tests
- Rate limiting
- Deployment secret management
- Production backup and recovery rules

## Architecture-specific risks to keep watching

### Memory poisoning

Future long-term memory must not be treated as trusted authorization. Retrieved context can be stale, incorrect or maliciously influenced.

### Prompt injection through connected sources

Email, webpages, documents and meeting notes are untrusted content. Their text must never be able to modify system approval rules or request additional permissions.

### Cross-scope retrieval

Work queries should not accidentally retrieve Personal records, and vice versa. Scope filtering should happen before semantic retrieval.

### Excessive connector permissions

Future integrations should start read-only when possible. Write permissions should be added only for workflows that need them.

## Licensing note

No open-source license has been selected. This is not a security issue, but it should be resolved before the repository is presented as an open-source project or external contributions are invited.

## Current recommendation

Proceed with local UX validation and LLM-backed extraction next. Do not add real email/calendar write connectors or real personal data until authentication, persistence boundaries and auditability are designed.
