# VinSAP Walkthrough

Run through this with the user at the end of `/vinsap:onboard`, briefly — this is an orientation, not a full manual.

1. **`/vinsap:onboard`** (you're here — alias `/vinsap:init`) — set input source, create `inputs/` structure.
2. **`/vinsap:config`** — set up connectors (Jira/Confluence, SAP MCP), product scope, diagram tool, model tiers, screenshot mode.
3. **`/vinsap:analyze`** (aka `/vinsap:scope`, `/vinsap:start`) — reads `inputs/`, asks clarifying questions, writes `outputs/scope.md`.
4. **`/vinsap:milestones`** — breaks the scope into milestones, tagged ABAP/Fiori/mixed.
5. **`/vinsap:develop`** — generates code + tests per milestone.
6. **`/vinsap:review`** — quick guideline check (background, cheap model).
7. **`/vinsap:test`** — runs tests, auto-fixes failures, repeats `develop`↔`test` per milestone until passing.
8. **`/vinsap:deep-review`** — thorough, cross-milestone review (foreground, smarter model) before documentation.
9. **`/vinsap:docs`** — generates Functional/Technical/Test documents, optionally publishes to Confluence.

Anytime:
- **`/vinsap:status`** — quick CLI view of where things stand.
- **`/vinsap:handoff`** — save a narrative summary of what happened, for continuation or sharing.

Tell the user: "Run `/vinsap:config` next."
