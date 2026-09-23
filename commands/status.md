---
description: Show current stage and per-milestone progress as a plain CLI kanban-style view.
---

Read `.sdlc/state.json`. No dedicated skill — format directly.

Also report the Atlassian connection: check whether `mcp-atlassian` tools (`mcp__mcp-atlassian__*`) are available in the current session — if so, read `.mcp.json`'s `mcpServers.mcp-atlassian.env` for `JIRA_PROJECTS_FILTER` and `CONFLUENCE_SPACES_FILTER` (both hardcoded Vincit constants, currently `ADSD`) and show them. If the tools aren't available, say "not connected" rather than guessing.

Output format:

```
VinSAP — <ticket/project id> Status

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

Icons: ✅ done, ⏳ in progress, ⬜ pending, ❌ failed/blocked. Compute the progress bar from milestones done/total. If `.sdlc/state.json` does not exist yet, tell the user to run `/vinsap:onboard` first.
