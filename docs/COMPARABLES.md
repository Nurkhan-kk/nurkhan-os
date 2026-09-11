# Comparable Projects and Design Takeaways

Nurkhan OS is not intended to copy an existing assistant. This note records patterns from adjacent open-source projects that are useful for shaping a credible public repository and a safer product architecture.

## Khoj

Repository: https://github.com/khoj-ai/khoj

Khoj positions itself as a personal AI assistant that can work with documents, agents, search and automations, with a strong self-hosting story.

Useful patterns observed:

- Clear README focused on what the product does
- Self-hosting and privacy are prominent concepts
- Dedicated documentation
- Explicit environment/configuration handling
- License file
- CI and developer tooling
- Separation between product code and deployment configuration

Takeaway for Nurkhan OS:

Keep the public value proposition simple, make privacy boundaries explicit, and document setup before adding many integrations.

## Leon

Repository: https://github.com/leon-ai/leon

Leon describes itself as an open-source personal assistant built around tools, context, memory and agentic execution. Its current architecture distinguishes more controlled deterministic execution from more agentic behavior.

Useful patterns observed:

- Architecture documentation is treated as a first-class artifact
- AI/developer-agent instructions are stored in repository files such as `AGENTS.md`
- Environment samples are separated from real credentials
- Tools, skills, context and execution layers are modular
- The project explicitly documents its development state instead of pretending unfinished areas are production-ready

Takeaway for Nurkhan OS:

The distinction between deterministic controlled workflows and model-driven reasoning is especially relevant. Human approval and connector execution should remain deterministic policy layers even after an LLM is introduced.

## Mem0

Repository: https://github.com/mem0ai/mem0

Mem0 focuses on persistent memory for AI applications and documents memory processing, retrieval and scoping as separate architectural concerns.

Useful patterns observed:

- Memory has explicit lifecycle and scope
- Retrieval is separated from generation
- Long-lived user context is treated differently from short-lived session context
- Memory is designed as infrastructure rather than hidden prompt text

Takeaway for Nurkhan OS:

Project context, decision history and personal preferences should become explicit stored records with scope and provenance. They should not exist only inside a large prompt.

## What Nurkhan OS should emphasize

The strongest differentiation is not a generic chat interface. It is the operating model:

- Natural-language Inbox instead of mandatory forms
- Work / Personal separation
- Persistent project context and decision reasons
- FYI / ACTION / DECISION REQUIRED attention routing
- Morning Brief focused on attention rather than task volume
- Leaving Work Brief organized around real-world execution
- Meeting preparation and post-meeting extraction
- Waiting-state and follow-up management
- Human approval for important external actions
- Official-message style checks

## Repository quality checklist

Based on the patterns above, a credible public prototype should have:

- README with a clear product statement
- Quick start instructions
- Architecture or product-spec documentation
- Synthetic demo data
- Tests and CI
- `.env.example`, never real secrets
- `.gitignore` for local secrets and generated files
- Security policy
- Privacy and threat-model notes
- AI-agent development instructions
- Clear statement of prototype limitations
- License decision before inviting reuse or external contributions

## Deliberate choices for this repository

Nurkhan OS remains intentionally small. It should not add Docker, a vector database, authentication providers or a full agent framework merely to resemble larger projects.

The next technical additions should be driven by validated product needs:

1. Local UX validation
2. LLM-backed structured extraction
3. Persistent task and project storage
4. Connector interfaces
5. Authentication and auditability before real personal data is used

This keeps the repository understandable to a reviewer and reduces the security surface while the product concept is still being validated.
