---
name: milestone-planner
description: Use for /vinsap:milestones — breaks the finalized scope into milestones tagged ABAP/Fiori/mixed, checking SAP system for reuse before proposing new objects.
---

# Milestone Planner

Follow `../_shared/context-contract.md` for read/write conventions.

## Steps

1. Read `outputs/scope.md`.
2. Query the SAP system via the `vincit-abap-mcp-<SID>` MCP connector (object search/source read) to check whether any part of the scope can reuse existing objects instead of building new ones.
3. Break the scope into discrete, independently developable/testable milestones. For each milestone, decide:
   - `type`: `abap`, `fiori`, or `mixed`
   - short title and a one-paragraph description
   - dependencies on other milestones, if any
4. Prefer smaller milestones that map to a single class/app/capability — easier to develop, test, and review independently (ties to `abap-developer`'s "class-based ABAP" preference).
5. Optionally produce a milestone dependency/flow diagram via the `illustrator` skill.
6. Write the milestone list into `.sdlc/state.json` (`milestones: [...]`, each starting at `develop: "pending"`).
7. Summarize the plan to the user before moving on.
8. Append a `.sdlc/timeline.jsonl` entry.

## Notes

- If the SAP MCP query surfaces a reusable object, flag it to the user rather than silently reusing or silently ignoring it.
