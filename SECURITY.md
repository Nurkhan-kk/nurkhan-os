# Security Policy

Nurkhan OS is currently a public prototype and is not production-ready.

## Supported versions

Security fixes currently apply to the latest `main` branch only.

## Reporting a vulnerability

Please do not open a public issue containing secrets, credentials, personal data or exploit details.

If GitHub private vulnerability reporting is available for this repository, use the repository's private security advisory flow. Otherwise, contact the repository owner through the GitHub profile and share only the minimum information needed to establish a private reporting channel.

Include:

- A short description of the issue
- Affected file or workflow
- Reproduction steps that do not expose real secrets
- Potential impact
- Suggested mitigation if known

## Scope

Especially relevant findings include:

- Secret exposure
- Approval-gate bypass
- Cross-scope Work / Personal data leakage
- Prompt-injection paths that can trigger actions
- Connector permission escalation
- Authentication or authorization failures once those features exist
- Sensitive information written to logs

## Public demo warning

Do not put real personal, business, financial, contractual, medical or communication data into a publicly deployed version of this prototype.

The current repository has no authentication and does not claim production security.

See `docs/SECURITY_AND_PRIVACY.md` for the project threat model and security roadmap.
