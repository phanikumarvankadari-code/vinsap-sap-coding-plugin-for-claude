---
description: Save a status snapshot of the active ticket, then tell you it's safe to run Claude Code's native /compact.
---

Invoke the `session-recorder` skill's local-save path — same summary-building logic as `/vinsap:handoff` (read `tickets/<active>/timeline.jsonl` + `state.json`, format a narrative: what happened, key decisions, current milestone status, open items), but:

1. Resolve the active ticket (per `_shared/context-contract.md`) — if none is active, tell the user to run `/vinsap:intent` or `/vinsap:switch` first, don't guess.
2. Write the snapshot to `tickets/<active>/outputs/handoff/<timestamp>-precompact.md`. **Always local, skip the "publish to Jira/Confluence?" question entirely** — this is an internal continuity checkpoint, not a deliberate handoff.
3. Append a `tickets/<active>/timeline.jsonl` entry (`action: "precompact_snapshot"`).
4. Tell the user the snapshot's path, and that it's now safe to run `/compact` (Claude Code's own built-in command) to free up context.

**This command cannot trigger native `/compact` itself** — a plugin command runs as agent instructions inside the current turn, and compaction is a harness-level action the user invokes directly. `/vinsap:compact` only prepares for it; running `/compact` afterward is a separate, manual step.
