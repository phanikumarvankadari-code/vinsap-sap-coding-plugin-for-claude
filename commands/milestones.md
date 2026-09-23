---
description: Break the active ticket's finalized scope into milestones, tagged ABAP/Fiori/mixed, checking for reuse in the SAP system.
---

Invoke the `milestone-planner` skill.

1. Read `tickets/<active>/outputs/scope.md`.
2. Query the SAP system via the `vincit-abap-mcp-<SID>` MCP connector to check for existing objects that can be reused before proposing new ones.
3. Break the scope into discrete milestones. Tag each milestone `abap`, `fiori`, or `mixed`.
4. Optionally produce a milestone flow/dependency diagram via the `illustrator` skill.
5. Write the milestone plan to `tickets/<active>/state.json` (as the source of truth for `/vinsap:status`) and summarize it to the user.
6. Append an entry to `tickets/<active>/timeline.jsonl`.
