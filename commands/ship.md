---
description: Deploy-readiness checklist for a milestone (or the Fiori track), cadence depends on milestone type.
---

Invoke `abap-developer` (for the milestone just built, if `abap`/`mixed`) or `fiori-developer` (if `fiori`) — ship logic lives in each developer skill's "Ship" section, not a separate skill.

1. First time this runs for the ticket: ask whether `/vinsap:deep-review` should be required before shipping — **Always** / **Ask each time** / **Skip** — store as `preferences.deep_review` in `tickets/<active>/state.json`, reused for later milestones without re-asking.
2. Confirm the milestone's tests are green (`test: "done"` in `state.json`); refuse to ship if not.
3. Apply the `deep_review` preference: on `always`, or `ask` (asking now), require `/vinsap:deep-review` to have run for this milestone/ticket before continuing; on `skip`, proceed without it.
4. **Cadence depends on milestone type:**
   - **ABAP/mixed** — ships this milestone now: list the transport(s) touched by it.
   - **Fiori/UI5** — check whether *every* Fiori milestone in this ticket has reached `test: "done"`. If not, tell the user shipping is deferred until the whole Fiori track is built/tested, and stop here (don't write `ship.md` yet). If yes, ship the whole track now.
5. Doesn't release or deploy anything itself — release stays a manual, outside-the-plugin step. Write/append `tickets/<active>/outputs/ship.md` (per-milestone entry for ABAP, one entry for the whole Fiori track) and update `state.json` (`ship: "done"` on the relevant milestone(s)).
6. Append an entry to `tickets/<active>/timeline.jsonl`.

Once all milestones for the ticket have shipped, suggest `/vinsap:docs`.
