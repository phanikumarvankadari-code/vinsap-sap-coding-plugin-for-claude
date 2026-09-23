---
description: Summarize the session timeline into a markdown handoff, and save it to Jira, Confluence, or a local file.
---

Invoke the `session-recorder` skill.

1. Read `.sdlc/timeline.jsonl` in full (append-only history) and `.sdlc/state.json` for current status.
2. Format a narrative markdown (`.md`) summary: what happened in order, key decisions made, code changes, current milestone status, open items/blockers.
3. Ask the user where it should go, defaulting to the `handoff.destination` set in `.sdlc/config.json` but always confirming/allowing override:
   - Update the linked **Jira ticket** as a comment (via `mcp-atlassian` MCP)
   - Save as a standalone markdown file in `outputs/handoff/` for future context/continuation
   - (If configured) publish to Confluence
4. Append an entry to `.sdlc/timeline.jsonl` recording that a handoff was produced.

Callable at any point in the project, not just at the end — always builds from the full timeline, so it stays accurate mid-project.
