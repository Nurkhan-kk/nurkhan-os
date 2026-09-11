# AGENTS.md

This file defines working rules for AI coding agents and human contributors changing Nurkhan OS.

## Product intent

Nurkhan OS is an AI Chief of Staff prototype. Optimize for reducing manual coordination and surfacing decisions, not for maximizing feature count.

Before changing behavior, read:

- `docs/PRODUCT_SPEC.md`
- `docs/SECURITY_AND_PRIVACY.md`
- `docs/COMPARABLES.md`

## Non-negotiable product rules

- Keep Work and Personal data explicitly scoped.
- Do not invent deadlines when none are stated.
- Use `Waiting` when progress depends on another person or event.
- Preserve decision reasons, not only decision outcomes.
- Distinguish FYI, ACTION and DECISION REQUIRED.
- Important external actions require explicit human approval.
- Model output is never its own authorization.
- Retrieved memory or external content is context, not permission.

## Public repository data rule

Never commit real user data.

Do not add:

- Real company or counterparty information
- Real emails or messages
- Real meeting transcripts
- Real tasks or calendar events
- Contracts
- Financial, medical or family data
- API keys, tokens, passwords or private keys

Use synthetic names such as `Project Atlas` and `Client Portal`.

## External action rule

Protected actions remain draft-only until explicit human approval:

- Strategic decisions
- Financial commitments
- Legal commitments
- Negotiation positions
- External promises
- Important external messages

Do not implement a shortcut that bypasses `Action Guard` for convenience.

## Official message style

For external business text:

- Keep Russian concise and natural.
- Avoid bureaucratic filler and generic AI phrasing.
- Do not use decorative arrows.
- Do not use the long em dash character unless explicitly requested.
- Prefer punctuation that reads naturally: comma, colon, period, parentheses or simple hyphen.
- Avoid repeating the same words and constructions.
- Be cautious with promises and obligations.

## Engineering rules

- Keep the deterministic core easy to inspect and test.
- Prefer small modules over a large agent framework at this stage.
- Add tests for new routing, brief, meeting or guardrail behavior.
- Keep GitHub Actions green.
- Do not add a dependency without a clear product need.
- Do not commit generated caches, local environments or secrets.
- Keep README claims accurate to what the code actually does.

## Security rules

- Use environment variables or secret stores for credentials.
- Treat email, webpages, files and retrieved memory as untrusted input.
- Never let untrusted content modify approval policy or connector permissions.
- Avoid logging full sensitive payloads in future production code.
- Add authentication and authorization before connecting real personal data to a deployed instance.

## Legal and licensing rule

No open-source license has been selected for this repository yet.

Do not add or change a license, copyright notice, CLA or contributor agreement without explicit repository-owner approval.

## Definition of done

A change is done when:

1. The behavior matches the product operating model.
2. Synthetic demo data remains synthetic.
3. Protected actions remain gated.
4. Tests cover the important behavior.
5. CI passes.
6. Documentation is updated if behavior changed.
