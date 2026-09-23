---
description: Read the active ticket's inputs/, analyze, ask clarifying questions, and finalize the scope. Alias of /vinsap:analyze and /vinsap:start.
---

Invoke the `scope-builder` skill.

1. Resolve the active ticket from `.sdlc/active_ticket.json` (per `_shared/context-contract.md`) — if none is active, tell the user to run `/vinsap:onboard` or `/vinsap:switch` first.
2. Read everything under `tickets/<active>/inputs/` (`docs/`, `emails/`, `conversations/`, `jira/`).
3. Produce a consolidated analysis summary: what's known, what's requested, any conflicts across sources.
4. List open questions/gaps found.
5. Ask the user those open questions directly, one at a time or grouped, to close the gaps.
6. Write the finalized scope to `tickets/<active>/outputs/scope.md`.
7. Append an entry to `tickets/<active>/timeline.jsonl` and update `tickets/<active>/state.json`.

This command is aliased as `/vinsap:analyze` and `/vinsap:start` — identical behavior.
