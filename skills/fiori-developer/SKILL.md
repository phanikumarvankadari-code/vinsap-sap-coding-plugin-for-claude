---
name: fiori-developer
description: Use for the Fiori/UI5 path of /vinsap:develop — generates Fiori/UI5 enhancement code, auto-generates QUnit unit tests and Playwright e2e tests.
---

# Fiori Developer

Follow `../_shared/context-contract.md` for read/write conventions.

## Steps

1. Read the target milestone from `tickets/<active>/state.json` and `tickets/<active>/outputs/scope.md`.
2. Generate the Fiori/UI5 enhancement code (view, controller, formatter, or standalone app extension) needed for the milestone.
3. Keep controller logic thin and testable — extract business/formatting logic into separate, injectable helper modules where practical, mirroring `abap-developer`'s "prefer testable units" principle.
4. Auto-generate a **QUnit** test for component/unit-level logic (controllers, formatters).
5. Auto-generate a **Playwright** e2e test for the user-facing flow; this runs later as a background subagent via `/vinsap:test` (see `test-runner/SKILL.md`), not inline here.
6. Update `tickets/<active>/state.json` milestone status; append a `tickets/<active>/timeline.jsonl` entry for each meaningful action.

## Notes

- If the milestone enhances a **standard Fiori app**, prefer an extension/adaptation project over modifying standard code directly.
- Coordinate naming with `abap-developer/references/package-hierarchy.md` if the UI milestone also touches OData/CDS projections in the `UI` layer.
