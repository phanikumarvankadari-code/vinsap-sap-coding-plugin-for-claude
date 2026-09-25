---
description: Start a new ticket (or, on the very first run for a project, walk through initial setup). Alias: /vinsap:init.
---

Invoke the `onboarding-guide` skill.

1. Check prerequisites (Node.js, Claude Code CLI, Playwright, antigravity CLI if configured, draw.io, Git CLI, `uv`/`uvx`) per `references/prerequisites.md`; guide install for anything missing.
2. If `.sdlc/config.json` doesn't exist yet, this is the project's first run — run the walkthrough from `references/walkthrough.md` and point to `/vinsap:config` next, then stop (don't start a ticket yet).
3. Otherwise, this starts a **new ticket**: ask for the ticket ID, ask how inputs will arrive (pull via `mcp-atlassian`, or manual drop), create `tickets/<TICKET-ID>/inputs/{docs,emails,conversations,jira}/` and `outputs/`, fetch the Jira ticket into `inputs/jira/` if that source was chosen.
4. Synthesize `tickets/<TICKET-ID>/intent.md` from whatever inputs are available (Jira description/comments, or manually-dropped docs/emails/conversations) — a short human-readable capture of what's being asked for: the raw ask, who wants it, and any context already known. Show it to the user and let them correct it before moving on; this is the seed `/vinsap:spec` reads next, not the final scope.
5. Set `.sdlc/active_ticket.json` to this new ticket.
6. Create `tickets/<TICKET-ID>/state.json` and append a `tickets/<TICKET-ID>/timeline.jsonl` entry marking the `intent` stage complete.

This command is aliased as `/vinsap:init` — identical behavior. To resume an existing ticket instead of starting a new one, use `/vinsap:switch <TICKET-ID>`.
