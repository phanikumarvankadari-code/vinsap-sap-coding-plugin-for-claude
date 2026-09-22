---
name: onboarding-guide
description: Use for /vinsap:onboard — checks prerequisites, guides installs, sets the input source (Jira vs manual), and creates the inputs/ folder structure. First-touch skill for a new VinSAP engagement.
---

# Onboarding Guide

Follow `../_shared/context-contract.md` for read/write conventions.

## Steps

1. **Prerequisite check** — see `references/prerequisites.md`. Check Node.js, Claude Code CLI, Playwright, and (if the project will use it) antigravity CLI. Report what's present/missing; offer install guidance for anything missing rather than failing silently.
2. **Input source** — ask the user: pull the linked Jira ticket via the `atlassian` MCP connector, or manually drop files into `inputs/`.
   - If Jira: fetch the ticket's description, comments, and attachments into `inputs/jira/<TICKET-ID>/`.
   - If manual: tell the user exactly where to drop files (`inputs/docs/`, `inputs/emails/`, `inputs/conversations/`).
3. **Create folder structure** if not already present:
   ```
   inputs/docs/ inputs/emails/ inputs/conversations/ inputs/jira/
   outputs/
   .sdlc/
   ```
4. **Walkthrough** — run through `references/walkthrough.md` with the user, then point them to `/vinsap:config` as the next step.
5. Update `.sdlc/state.json` (`stage: "onboard"`, create the file if absent) and append a `.sdlc/timeline.jsonl` entry.

## Notes

- Don't block on prerequisites the current task doesn't need (e.g. antigravity CLI only matters if diagram generation uses it — draw.io/mermaid don't need it).
- This skill only sets up structure and input source; it does not read or analyze the input content — that's `scope-builder`'s job.
