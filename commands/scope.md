---
description: Read inputs/, analyze, ask clarifying questions, and finalize the scope. Alias of /vinsap:analyze and /vinsap:start.
---

Invoke the `scope-builder` skill.

1. Read everything under `inputs/` (`docs/`, `emails/`, `conversations/`, `jira/`).
2. Produce a consolidated analysis summary: what's known, what's requested, any conflicts across sources.
3. List open questions/gaps found.
4. Ask the user those open questions directly, one at a time or grouped, to close the gaps.
5. Write the finalized scope to `outputs/scope.md`.
6. Append an entry to `.sdlc/timeline.jsonl` and update `.sdlc/state.json`.

This command is aliased as `/vinsap:analyze` and `/vinsap:start` — identical behavior.
