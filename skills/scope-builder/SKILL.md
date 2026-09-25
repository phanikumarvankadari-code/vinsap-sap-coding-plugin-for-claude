---
name: scope-builder
description: Use for /vinsap:analyze, /vinsap:scope, /vinsap:start (aliases) — reads the active ticket's inputs/, produces an analysis summary, asks the user clarifying questions for gaps, and writes the finalized outputs/scope.md.
---

# Scope Builder

Follow `../_shared/context-contract.md` for read/write conventions and how the active ticket resolves.

## Steps

1. Read everything under `tickets/<active>/inputs/docs/`, `inputs/emails/`, `inputs/conversations/`, `inputs/jira/`.
2. Produce a consolidated analysis summary: what's known, what's being requested, and any conflicting information across sources.
3. Identify open questions/gaps — things unclear or missing that block a confident scope.
4. Ask the user those open questions directly (grouped, not one huge dump) and capture their answers.
5. Ask which **functional/solution area(s)** this ticket falls under — the same fixed codes `abap-developer/references/package-hierarchy.md` uses: `FIN`, `SLS`, `SRC`, `MFG`, `SCM`, `HCM`, `AST`, `SVC`, `CORE`. Store as `functional_areas` in `tickets/<active>/state.json`. This isn't a package assignment — it's just used later to pre-fill (never auto-select) the `Z*` package-search prefix in `abap-developer` (e.g. `SLS` → suggest starting the search at `ZSD*`/`ZMASTER_SLS*`).
6. Write the finalized scope to `tickets/<active>/outputs/scope.md`, including:
   - Summary of the request
   - What's in scope / out of scope
   - Answers captured from the clarifying round
   - Any remaining open risks (carried forward into `doc-generator`'s Functional Doc "Open Questions/Risks" section later)
7. Append a `tickets/<active>/timeline.jsonl` entry and update `tickets/<active>/state.json` (`stage: "scope"`).

## Notes

- If `tickets/<active>/inputs/` is empty, tell the user to drop files in now (or run `/vinsap:onboard` if no ticket is active yet) rather than guessing scope from nothing.
- Re-runnable — if new inputs are added later, running this again should re-analyze and merge, not discard the prior scope doc without asking.
- Always operates on the **active** ticket — use `/vinsap:switch` first if the user means a different one.
