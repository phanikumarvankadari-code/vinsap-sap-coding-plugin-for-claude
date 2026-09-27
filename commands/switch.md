---
description: Switch which ticket subsequent commands operate on. Does not create a new ticket — use /vinsap:intent for that.
---

Invoke the `ticket-switcher` skill.

1. Take `$ARGUMENTS` as the target ticket ID. If empty, list tickets under `tickets/` and ask the user to pick.
2. Verify `tickets/<TICKET-ID>/` exists — if not, tell the user to run `/vinsap:intent` to start it as a new ticket instead.
3. Update `.sdlc/active_ticket.json` to point at it.
4. Show a quick summary of that ticket's current stage/milestone status (same style as `/vinsap:status`).
5. Check `tickets/<TICKET-ID>/outputs/handoff/` for saved context (handoff summaries, `/vinsap:compact` precompact snapshots). If any exist, read the **most recent** one (by its timestamp filename) and fold its contents into the current conversation — so the session picks up with that ticket's prior state already loaded, not just the raw `state.json` numbers. Mention to the user which snapshot you loaded and when it was saved. If none exist, say so plainly rather than guessing at history.
