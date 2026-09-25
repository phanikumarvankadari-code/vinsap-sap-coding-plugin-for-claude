---
name: scope-builder
description: Use for /vinsap:spec (aliases /vinsap:analyze, /vinsap:scope, /vinsap:start) — reads the active ticket's intent.md + inputs/, produces an analysis summary, asks the user clarifying questions for gaps, and writes the finalized outputs/spec.md.
---

# Scope Builder

Follow `../_shared/context-contract.md` for read/write conventions and how the active ticket resolves.

## Steps

1. Read `tickets/<active>/intent.md` plus everything under `tickets/<active>/inputs/docs/`, `inputs/emails/`, `inputs/conversations/`, `inputs/jira/`.
2. Produce a consolidated analysis summary: what's known, what's being requested, and any conflicting information across sources.
3. Identify open questions/gaps — things unclear or missing that block a confident spec.
4. Ask the user those open questions directly (grouped, not one huge dump) and capture their answers.
5. Ask which **functional/solution area(s)** this ticket falls under — classical ECC module codes, the same fixed set `abap-developer/references/package-hierarchy.md` uses: `FI`, `SD`, `MM`, `PP`, `LE`, `HR`, `AA`, `CS`, `CORE`. Store as `functional_areas` in `tickets/<active>/state.json`. This isn't a package assignment — it's just used later to pre-fill (never auto-select) the `Z*` package-search prefix in `abap-developer` (e.g. `SD` → suggest starting the search at `ZMASTER_SD*`).
6. Write the finalized spec to `tickets/<active>/outputs/spec.md`, including:
   - Summary of the request
   - What's in scope / out of scope
   - Answers captured from the clarifying round
   - Any remaining open risks (carried forward into `doc-generator`'s Functional Doc "Open Questions/Risks" section later)
7. Offer to start the Functional Document now via `/vinsap:docs` (optional — the user picks sections via a checkbox list, see `doc-generator/SKILL.md`); either way, point to `/vinsap:plan` next.
8. Append a `tickets/<active>/timeline.jsonl` entry and update `tickets/<active>/state.json` (`stage: "spec"`).

## Notes

- If `tickets/<active>/inputs/` is empty, tell the user to drop files in now (or run `/vinsap:intent` if no ticket is active yet) rather than guessing the spec from nothing.
- Re-runnable — if new inputs are added later, running this again should re-analyze and merge, not discard the prior spec without asking.
- Always operates on the **active** ticket — use `/vinsap:switch` first if the user means a different one.
