---
description: Break the active ticket's finalized spec into milestones, tagged ABAP/Fiori/mixed, checking for reuse in the SAP system.
---

Invoke the `milestone-planner` skill.

1. Read `tickets/<active>/outputs/spec.md`.
2. Query the SAP system via the `vincit-abap-mcp-<SID>` MCP connector to check for existing objects that can be reused before proposing new ones.
3. Break the spec into discrete milestones. Tag each milestone `abap`, `fiori`, or `mixed`.
4. For ABAP/mixed milestones, add a best-guess **object preview** — anticipated object names/types/target layer (see `abap-developer/references/package-hierarchy.md`) — informational only, `/vinsap:build` can still deviate from it.
5. Optionally produce a milestone flow/dependency diagram via the `illustrator` skill.
6. Ask once, for this ticket: **review code locally before it ships?** — `Always` / `Ask each time` / `Skip`. Store as `preferences.local_review` in `tickets/<active>/state.json`. `/vinsap:build` consults this before moving code out of local staging.
7. Write the milestone plan to both `tickets/<active>/outputs/plan.md` (human-readable: milestone list, object previews, dependencies) and `tickets/<active>/state.json` (machine-tracked status, the source of truth for `/vinsap:status`). Summarize it to the user.
8. Append an entry to `tickets/<active>/timeline.jsonl`.
