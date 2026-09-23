---
name: onboarding-guide
description: Use for /vinsap:onboard (alias /vinsap:init) — checks prerequisites, guides installs, and starts a new ticket (input source, tickets/<TICKET-ID>/ folder, sets it active). First-touch skill for a new VinSAP engagement, and re-run per new ticket.
---

# Onboarding Guide

Follow `../_shared/context-contract.md` for read/write conventions — in particular "Project structure" and "Resolving the active ticket."

## Steps

1. **Prerequisite check** — see `references/prerequisites.md`. Check Node.js, Claude Code CLI, Playwright, and (if the project will use it) antigravity CLI, draw.io, Git CLI, `uv`/`uvx`. Report what's present/missing; offer install guidance for anything missing rather than failing silently. Skip if already checked recently and nothing's changed.
2. **First run vs. new ticket** — if `.sdlc/config.json` doesn't exist yet, this is the very first run for this project: run through `references/walkthrough.md`, then point the user to `/vinsap:config` before starting any ticket. If `.sdlc/config.json` already exists, this run is starting a **new ticket** on top of an already-configured project — skip straight to step 3.
3. **Ticket ID** — ask for the Jira ticket ID this work is for (e.g. `ADSD-1204`). If pulling from Jira, this can come from the ticket the user names; if manual, ask the user to supply one (any short unique identifier works, doesn't strictly need to be a real Jira key, but should be if one exists).
4. **Input source** — ask the user: pull the ticket via `mcp-atlassian` (fetches description, comments, attachments into `tickets/<TICKET-ID>/inputs/jira/`), or manually drop files into `tickets/<TICKET-ID>/inputs/docs/`, `inputs/emails/`, `inputs/conversations/`.
5. **Create the ticket folder**: `tickets/<TICKET-ID>/inputs/docs/`, `inputs/emails/`, `inputs/conversations/`, `inputs/jira/`, `outputs/`. Don't touch `.sdlc/config.json` (shared, untouched here).
6. **Set active**: write `.sdlc/active_ticket.json` with `{"active_ticket": "<TICKET-ID>", "last_switched": "<now>"}`.
7. If this was the very first run for the project, run the walkthrough and point to `/vinsap:config` next. Otherwise, confirm the new ticket is active and point to `/vinsap:analyze` (or `/vinsap:scope`/`/vinsap:start`) next.
8. Create `tickets/<TICKET-ID>/state.json` (`stage: "onboard"`) and append a `tickets/<TICKET-ID>/timeline.jsonl` entry.

## Notes

- Don't block on prerequisites the current task doesn't need (e.g. antigravity CLI only matters if diagram generation uses it — draw.io/mermaid don't need it).
- This skill only sets up structure and input source; it does not read or analyze the input content — that's `scope-builder`'s job.
- To resume work on an existing ticket rather than start a new one, use `/vinsap:switch <TICKET-ID>` instead of re-running onboarding.
