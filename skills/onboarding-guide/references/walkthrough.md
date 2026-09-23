# VinSAP Walkthrough

Run through this with the user at the end of the project's very first `/vinsap:onboard` run, briefly — this is an orientation, not a full manual.

**One-time, project-level setup:**

1. **`/vinsap:onboard`** (you're here — alias `/vinsap:init`) — on this very first run, just sets up prerequisites; doesn't start a ticket yet.
2. **`/vinsap:config`** — set up connectors (Jira/Confluence via `mcp-atlassian`, SAP MCP systems/modes), product scope, diagram tool, model tiers, screenshot mode, git usage. Shared across every ticket you'll work on in this project.

**Per ticket, repeat this whole flow for each one:**

3. **`/vinsap:onboard`** again — this time starts a new ticket: ticket ID, input source, creates `tickets/<TICKET-ID>/`, sets it active.
4. **`/vinsap:analyze`** (aka `/vinsap:scope`, `/vinsap:start`) — reads that ticket's `inputs/`, asks clarifying questions, writes `outputs/scope.md` (both under `tickets/<TICKET-ID>/`).
5. **`/vinsap:milestones`** — breaks the scope into milestones, tagged ABAP/Fiori/mixed.
6. **`/vinsap:develop`** — generates code + tests per milestone.
7. **`/vinsap:review`** — quick guideline check (background, cheap model).
8. **`/vinsap:test`** — runs tests, auto-fixes failures, repeats `develop`↔`test` per milestone until passing.
9. **`/vinsap:deep-review`** — thorough, cross-milestone review (foreground, smarter model) before documentation.
10. **`/vinsap:docs`** — generates Functional/Technical/Test documents, optionally publishes to Confluence.

**Anytime:**
- **`/vinsap:status`** — quick CLI view of the active ticket (or all tickets).
- **`/vinsap:switch <TICKET-ID>`** — change which ticket is active, without starting a new one.
- **`/vinsap:handoff`** — save a narrative summary of what happened on the active ticket, for continuation or sharing.

Tell the user: "Run `/vinsap:config` next." (Only on this first-ever run — subsequent `/vinsap:onboard` calls start new tickets directly.)
