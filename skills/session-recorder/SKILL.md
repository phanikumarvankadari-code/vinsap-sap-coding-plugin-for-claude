---
name: session-recorder
description: Use for /vinsap:handoff — reads the full session timeline, formats a narrative markdown summary, and saves it to Jira, Confluence, or a local file per user's choice.
---

# Session Recorder

Follow `../_shared/context-contract.md` for read/write conventions.

## Steps

1. Read `.sdlc/timeline.jsonl` in full and `.sdlc/state.json` for current status.
2. Format a narrative **markdown** summary, in chronological order:
   - What happened (grouped by stage: onboard, config, scope, milestones, develop, review, test, deep-review, docs)
   - Key decisions made (including any `guardrail_bypass` entries — call these out explicitly)
   - Code changes (objects created/modified, transports touched)
   - Current milestone status (pull from `.sdlc/state.json`)
   - Open items/blockers
   - Follow `doc-generator/references/writing-style.md` — simple English, bullets over paragraphs
3. Ask the user where it should go, offering `handoff.destination` from `.sdlc/config.json` as the default but always confirming/allowing override:
   - **Jira ticket comment** — via `mcp-atlassian` MCP, post to the linked ticket
   - **Standalone markdown file** — save to `outputs/handoff/<timestamp>-handoff.md`
   - **Confluence page** — via `mcp-atlassian` MCP, create new or update existing, if configured
4. Append a `.sdlc/timeline.jsonl` entry recording that a handoff was produced (`action: "handoff_created"`).

## Notes

- Always build from `timeline.jsonl`, never from chat scrollback or by guessing — this is what keeps the handoff accurate even when run mid-project.
- Output is always markdown (`.md`), regardless of destination — even when posted as a Jira comment, the source content is markdown-formatted text.
