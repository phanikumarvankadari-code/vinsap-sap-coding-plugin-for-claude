---
name: fiori-developer
description: Use for the Fiori/UI5 path of /vinsap:build — generates Fiori/UI5 enhancement code, auto-generates QUnit unit tests and Playwright e2e tests. Also handles the Fiori path of /vinsap:ship.
---

# Fiori Developer

Follow `../_shared/context-contract.md` for read/write conventions.

## Build steps (`/vinsap:build`)

1. Read the target milestone from `tickets/<active>/state.json` and `tickets/<active>/outputs/spec.md`.
2. Generate the Fiori/UI5 enhancement code (view, controller, formatter, or standalone app extension) needed for the milestone.
3. Keep controller logic thin and testable — extract business/formatting logic into separate, injectable helper modules where practical, mirroring `abap-developer`'s "prefer testable units" principle.
4. Auto-generate a **QUnit** test for component/unit-level logic (controllers, formatters).
5. Auto-generate a **Playwright** e2e test for the user-facing flow; this runs later as a background subagent via `/vinsap:test` (see `test-runner/SKILL.md`), not inline here.
6. **Local-review checkpoint**: check `tickets/<active>/state.json` → `preferences.local_review` (set by `/vinsap:plan`). On `always`, or on `ask` (asking now), pause and show the generated code in chat — wait for the user's go-ahead or change requests. On `skip`, continue straight through.
7. Update `tickets/<active>/state.json` milestone status (`build: "building"` then `"built"`); append a `tickets/<active>/timeline.jsonl` entry for each meaningful action.

## Ship steps (`/vinsap:ship`, Fiori/UI5 milestones)

Unlike ABAP, Fiori ships **once for the whole track**, not per milestone — app-level deployment isn't incremental:

1. If this is the first `/vinsap:ship` run for the ticket, ask whether `/vinsap:deep-review` should be required before shipping — `Always`/`Ask each time`/`Skip` — store as `preferences.deep_review` in `state.json` (shared with the ABAP path, asked only once).
2. Check whether *every* Fiori milestone in this ticket has reached `test: "done"`. If not, tell the user shipping is deferred until the whole Fiori track is built and tested, and stop — don't write `ship.md` yet.
3. If yes: apply the `deep_review` preference, then write one `ship.md` entry summarizing the whole Fiori track (apps/views touched, OData/CDS `UI`-layer packages if any per `abap-developer/references/package-hierarchy.md`). Update `state.json` (`ship: "done"` on each Fiori milestone).
4. Append a `tickets/<active>/timeline.jsonl` entry.

Doesn't release or deploy anything itself — release stays a manual, outside-the-plugin step.

## Notes

- If the milestone enhances a **standard Fiori app**, prefer an extension/adaptation project over modifying standard code directly.
- Coordinate naming with `abap-developer/references/package-hierarchy.md` if the UI milestone also touches OData/CDS projections in the `UI` layer.
