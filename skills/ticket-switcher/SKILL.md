---
name: ticket-switcher
description: Use for /vinsap:switch — changes which ticket subsequent VinSAP commands operate on, without creating a new one. Use /vinsap:intent instead to start a brand new ticket.
---

# Ticket Switcher

Follow `../_shared/context-contract.md` for read/write conventions.

## Steps

1. Take the ticket ID argument. If none given, list the tickets currently under `tickets/` (folder names) and ask the user to pick one.
2. Verify `tickets/<TICKET-ID>/` exists. If it doesn't, **don't create it** — tell the user to run `/vinsap:intent` instead to start it as a new ticket, or check for a typo.
3. Write `.sdlc/active_ticket.json`: `{"active_ticket": "<TICKET-ID>", "last_switched": "<now>"}`.
4. Read `tickets/<TICKET-ID>/state.json` if it exists and summarize where that ticket currently stands (stage, milestone progress) — same shape `/vinsap:status` prints — so the user immediately sees what they're switching into.
5. No timeline entry needed for the switch itself in the *target* ticket (switching isn't a development action on that ticket) — but do log it lightly if useful for audit, at the caller's discretion.

## Notes

- This is the only command that changes `.sdlc/active_ticket.json` outside of `/vinsap:intent` setting it for a brand-new ticket.
- Never touches `.sdlc/config.json` — that stays shared across every ticket, untouched by switching.
