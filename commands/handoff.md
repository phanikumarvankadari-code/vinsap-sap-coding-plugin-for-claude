---
description: Summarize the active ticket's timeline into a markdown handoff, always saved into the ticket, and optionally also published to Jira or Confluence.
---

Invoke the `session-recorder` skill.

1. Read `tickets/<active>/timeline.jsonl` in full (append-only history) and `tickets/<active>/state.json` for current status.
2. Format a narrative markdown (`.md`) summary: what happened in order, key decisions made, code changes, current milestone status, open items/blockers.
3. **Always** save it to `tickets/<active>/outputs/handoff/<timestamp>-handoff.md` — unconditional, this is the ticket's own record of what happened.
4. Then ask whether to **also** publish it externally, defaulting to `handoff.destination` set in `.sdlc/config.json` but always confirming/allowing override or skipping:
   - Update the linked **Jira ticket** as a comment (via `mcp-atlassian` MCP)
   - Publish to Confluence
   - Skip — the local file is enough this time
5. Append an entry to `tickets/<active>/timeline.jsonl` recording that a handoff was produced, and where (if anywhere) it was also published.

Callable at any point on the active ticket, not just at the end — always builds from the full timeline, so it stays accurate mid-ticket.
