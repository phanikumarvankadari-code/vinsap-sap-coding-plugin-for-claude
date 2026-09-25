# VinSAP Walkthrough

Run through this with the user at the end of the project's very first `/vinsap:intent` run, briefly — this is an orientation, not a full manual.

**One-time, project-level setup:**

1. **`/vinsap:config`** — set up connectors (Jira/Confluence via `mcp-atlassian`, SAP MCP systems/modes), diagram tool, model tiers, screenshot mode, git usage. Shared across every ticket you'll work on in this project.
2. **`/vinsap:intent`** (you're here — alias `/vinsap:init`) — on this very first run, just sets up prerequisites; doesn't start a ticket yet.

**Per ticket, repeat this whole flow for each one:**

3. **`/vinsap:intent`** again — this time starts a new ticket: ticket ID, input source, creates `tickets/<TICKET-ID>/`, writes `intent.md`, sets it active.
4. **`/vinsap:spec`** (aka `/vinsap:analyze`, `/vinsap:scope`, `/vinsap:start`) — reads intent + that ticket's `inputs/`, asks clarifying questions plus the ticket's functional/solution area(s), writes `outputs/spec.md` (both under `tickets/<TICKET-ID>/`).
5. **`/vinsap:plan`** — breaks the spec into milestones, tagged ABAP/Fiori/mixed, previews anticipated objects, writes `outputs/plan.md`.
6. **`/vinsap:build`** — generates code + tests per milestone.
7. **`/vinsap:review`** — quick guideline check (background, cheap model).
8. **`/vinsap:test`** — runs tests, auto-fixes failures, repeats `build`↔`test` per milestone until passing.
9. **`/vinsap:deep-review`** *(optional)* — thorough, cross-milestone review (foreground, smarter model). `/vinsap:ship` decides whether it's required.
10. **`/vinsap:ship`** — deploy-readiness checklist. ABAP/mixed milestones ship one at a time; Fiori/UI5 milestones ship once, after the whole Fiori track is built and tested.
11. **`/vinsap:docs`** — generates Functional/Technical/Test documents, optionally publishes to Confluence (and comments the link on the linked Jira issue).

**Anytime:**
- **`/vinsap:status`** — quick CLI view of the active ticket (or all tickets).
- **`/vinsap:switch <TICKET-ID>`** — change which ticket is active, without starting a new one.
- **`/vinsap:handoff`** — save a narrative summary of what happened on the active ticket, for continuation or sharing.

Tell the user: "Run `/vinsap:config` next." (Only on this first-ever run — subsequent `/vinsap:intent` calls start new tickets directly.)
