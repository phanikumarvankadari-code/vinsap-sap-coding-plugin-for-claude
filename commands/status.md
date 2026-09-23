---
description: Show progress for the active ticket, or list all tickets, as a plain CLI kanban-style view.
---

No dedicated skill — format directly. Two modes:

- **No argument** (or the active ticket's ID): resolve the active ticket from `.sdlc/active_ticket.json` (per `_shared/context-contract.md`), read `tickets/<active>/state.json`, show its detailed kanban view (below). If no ticket is active, say so and point to `/vinsap:onboard`/`/vinsap:switch` rather than guessing.
- **`all`** (or any unrecognized argument): list every folder under `tickets/`, read each one's `state.json`, and show a one-line summary per ticket (ID, stage, milestones done/total), marking which one is currently active.

Also report the Atlassian connection: check whether `mcp-atlassian` tools (`mcp__mcp-atlassian__*`) are available in the current session — if so, read `.mcp.json`'s `mcpServers.mcp-atlassian.env` for `JIRA_PROJECTS_FILTER` and `CONFLUENCE_SPACES_FILTER` (both hardcoded Vincit constants, currently `ADSD`) and show them. If the tools aren't available, say "not connected" rather than guessing.

Output format (active-ticket mode):

```
VinSAP — <TICKET-ID> Status  [active]

Atlassian: ✅ connected — Jira project ADSD · Confluence space ADSD
           (or: ❌ not connected — check /mcp)

Stage Progress
✅ onboard
✅ config
✅ analyze/scope
⏳ milestones

Milestones
✅ M1: <title>   [develop ✓] [test ✓]
⏳ M2: <title>   [develop ✓] [test ⏳]
⬜ M3: <title>   [pending]

Progress: <block-bar> NN% (X/Y complete)

Last updated: <timestamp>
```

Output format (`all` mode):

```
VinSAP — All Tickets

▶ ADSD-1204   develop    2/3 milestones done   (active)
  ADSD-1301   scope      0/0 milestones
  ADSD-0892   docs       4/4 milestones done
```

Icons: ✅ done, ⏳ in progress, ⬜ pending, ❌ failed/blocked. Compute the progress bar from milestones done/total. If `tickets/` doesn't exist yet, tell the user to run `/vinsap:onboard` first.
