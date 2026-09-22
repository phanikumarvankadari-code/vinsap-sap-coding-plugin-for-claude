---
description: Choose input source (Jira ticket vs manual drop) and set up the inputs/ folder for this SDLC engagement.
---

Invoke the `onboarding-guide` skill.

1. Check prerequisites (Node.js, Claude Code CLI, Playwright, antigravity CLI if configured) per `references/prerequisites.md`; guide install for anything missing.
2. Ask the user how inputs will arrive: pull a Jira ticket (via the `atlassian` MCP connector) or manually drop files.
3. Create the `inputs/` folder structure if it does not already exist: `inputs/docs/`, `inputs/emails/`, `inputs/conversations/`, `inputs/jira/`. If pulling from Jira, fetch the ticket (description, comments, attachments) into `inputs/jira/`.
4. Run the walkthrough tutorial from `references/walkthrough.md`, pointing the user to `/vinsap:config` next.
5. Append an entry to `.sdlc/timeline.jsonl` and update `.sdlc/state.json` (create if absent) marking the `onboard` stage complete.
