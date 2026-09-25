---
name: session-recorder
description: Use for /vinsap:handoff — reads the active ticket's full timeline, formats a narrative markdown summary, always saves a copy into the ticket's outputs/handoff/, and optionally also publishes to Jira or Confluence.
---

# Session Recorder

Follow `../_shared/context-contract.md` for read/write conventions.

## Steps

1. Read `tickets/<active>/timeline.jsonl` in full and `tickets/<active>/state.json` for current status.
2. Format a narrative **markdown** summary, in chronological order:
   - What happened (grouped by stage: config, intent, spec, plan, build, review, test, deep-review, ship, docs)
   - Key decisions made (including any `guardrail_bypass` entries — call these out explicitly)
   - Code changes (objects created/modified, transports touched)
   - Current milestone status (pull from `tickets/<active>/state.json`)
   - Open items/blockers
   - Follow `doc-generator/references/writing-style.md` — simple English, bullets over paragraphs
3. **Always** save the markdown to `tickets/<active>/outputs/handoff/<timestamp>-handoff.md` — this is unconditional, not a destination choice. This is what keeps the ticket's own record of what happened, independent of anything published externally.
4. Then ask the user whether to **also** publish it externally, offering `handoff.destination` from `.sdlc/config.json` as the default but always confirming/allowing override or skipping:
   - **Jira ticket comment** — via `mcp-atlassian` MCP, post to the linked ticket
   - **Confluence page** — via `mcp-atlassian` MCP, create new or update existing, if configured
   - **None** — the local file in `tickets/<active>/outputs/handoff/` is enough this time
5. Append a `tickets/<active>/timeline.jsonl` entry recording that a handoff was produced (`action: "handoff_created"`), noting whether it was also published externally and where.

## Notes

- Always build from `timeline.jsonl`, never from chat scrollback or by guessing — this is what keeps the handoff accurate even when run mid-project.
- Output is always markdown (`.md`), regardless of destination — even when posted as a Jira comment, the source content is markdown-formatted text.
