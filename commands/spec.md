---
description: Read the active ticket's intent + inputs/, ask clarifying questions, and finalize the spec. Alias of /vinsap:analyze and /vinsap:start.
---

Invoke the `scope-builder` skill.

1. Resolve the active ticket from `.sdlc/active_ticket.json` (per `_shared/context-contract.md`) — if none is active, tell the user to run `/vinsap:intent` or `/vinsap:switch` first.
2. Read `tickets/<active>/intent.md` plus everything under `tickets/<active>/inputs/` (`docs/`, `emails/`, `conversations/`, `jira/`).
3. Produce a consolidated analysis summary: what's known, what's requested, any conflicts across sources.
4. List open questions/gaps found.
5. Ask the user those open questions directly, one at a time or grouped, to close the gaps.
6. Ask which functional/solution area(s) this ticket falls under — classical ECC module codes (`FI`/`SD`/`MM`/`PP`/`LE`/`HR`/`AA`/`CS`/`CORE`) — stored as `functional_areas` in `state.json`, used later to pre-fill the `Z*` package search in `abap-developer`/`fiori-developer`.
7. Write the finalized spec to `tickets/<active>/outputs/spec.md`.
8. Offer to start the **Functional Document** now via `/vinsap:docs` (checkbox section picker) — optional, the user can decline and run it later; point to `/vinsap:plan` as the next required step either way.
9. Append an entry to `tickets/<active>/timeline.jsonl` and update `tickets/<active>/state.json`.

This command is aliased as `/vinsap:analyze` and `/vinsap:start` — identical behavior.
