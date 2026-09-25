---
name: milestone-planner
description: Use for /vinsap:plan — breaks the finalized spec into milestones tagged ABAP/Fiori/mixed, checking SAP system for reuse before proposing new objects, and writes a human-readable outputs/plan.md.
---

# Milestone Planner

Follow `../_shared/context-contract.md` for read/write conventions.

## Steps

1. Read `tickets/<active>/outputs/spec.md`.
2. Query the SAP system via the `vincit-abap-mcp-<SID>` MCP connector (object search/source read) to check whether any part of the spec can reuse existing objects instead of building new ones.
3. Break the spec into discrete, independently developable/testable milestones. For each milestone, decide:
   - `type`: `abap`, `fiori`, or `mixed`
   - short title and a one-paragraph description
   - dependencies on other milestones, if any
4. Prefer smaller milestones that map to a single class/app/capability — easier to develop, test, and review independently (ties to `abap-developer`'s class-granularity guidance).
5. For ABAP/mixed milestones, add a best-guess **object preview**: anticipated object names/types/target layer (per `abap-developer/references/package-hierarchy.md`) — informational only, so the user can see how objects are planned before `/vinsap:build` runs. `/vinsap:build` can still deviate from it.
6. Optionally produce a milestone dependency/flow diagram via the `illustrator` skill.
7. Ask once, for this ticket: **review code locally before it ships?** — `Always` / `Ask each time` / `Skip`. Store as `preferences.local_review` in `tickets/<active>/state.json`. `/vinsap:build` consults this before moving code out of local staging into a package/transport.
8. Write the milestone list to **both**:
   - `tickets/<active>/outputs/plan.md` — human-readable: milestones, descriptions, dependencies, object previews.
   - `tickets/<active>/state.json` (`milestones: [...]`, each starting at `build: "pending"`) — machine-tracked, source of truth for `/vinsap:status`.
9. Summarize the plan to the user before moving on.
10. Append a `tickets/<active>/timeline.jsonl` entry.

## Notes

- If the SAP MCP query surfaces a reusable object, flag it to the user rather than silently reusing or silently ignoring it.
- The object preview is a planning aid, not a commitment — `/vinsap:build` always re-checks reuse and asks for the real package at build time.
