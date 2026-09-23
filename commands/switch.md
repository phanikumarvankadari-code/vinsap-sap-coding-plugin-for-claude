---
description: Switch which ticket subsequent commands operate on. Does not create a new ticket — use /vinsap:onboard for that.
---

Invoke the `ticket-switcher` skill.

1. Take `$ARGUMENTS` as the target ticket ID. If empty, list tickets under `tickets/` and ask the user to pick.
2. Verify `tickets/<TICKET-ID>/` exists — if not, tell the user to run `/vinsap:onboard` to start it as a new ticket instead.
3. Update `.sdlc/active_ticket.json` to point at it.
4. Show a quick summary of that ticket's current stage/milestone status (same style as `/vinsap:status`).
