---
name: scope-builder
description: Use for /vinsap:analyze, /vinsap:scope, /vinsap:start (aliases) — reads inputs/, produces an analysis summary, asks the user clarifying questions for gaps, and writes the finalized outputs/scope.md.
---

# Scope Builder

Follow `../_shared/context-contract.md` for read/write conventions.

## Steps

1. Read everything under `inputs/docs/`, `inputs/emails/`, `inputs/conversations/`, `inputs/jira/`.
2. Produce a consolidated analysis summary: what's known, what's being requested, and any conflicting information across sources.
3. Identify open questions/gaps — things unclear or missing that block a confident scope.
4. Ask the user those open questions directly (grouped, not one huge dump) and capture their answers.
5. Write the finalized scope to `outputs/scope.md`, including:
   - Summary of the request
   - What's in scope / out of scope
   - Answers captured from the clarifying round
   - Any remaining open risks (carried forward into `doc-generator`'s Functional Doc "Open Questions/Risks" section later)
6. Append a `.sdlc/timeline.jsonl` entry and update `.sdlc/state.json` (`stage: "scope"`).

## Notes

- If `inputs/` is empty, tell the user to run `/vinsap:onboard` first (or drop files in now) rather than guessing scope from nothing.
- Re-runnable — if new inputs are added later, running this again should re-analyze and merge, not discard the prior scope doc without asking.
