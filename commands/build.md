---
description: Generate code for the next (or specified) milestone, ABAP or Fiori path, with auto-generated tests.
---

Pick the target milestone (next `pending` one in `tickets/<active>/state.json`, or one the user names).

- If tagged `abap` (or `mixed`, ABAP part): invoke the `abap-developer` skill.
- If tagged `fiori` (or `mixed`, UI part): invoke the `fiori-developer` skill.

Each skill:
1. Generates the code for the milestone, following its guardrails/standards in `references/`.
2. Prefers class-based ABAP over reports/includes for testability — see `abap-developer/references/coding-standards.md` § "Class granularity" for how many classes a milestone should actually need.
3. Syntax/ATC checks, generates the matching test (ABAP Unit for ABAP, QUnit for Fiori/UI5 unit-level logic).
4. Checks `tickets/<active>/state.json` → `preferences.local_review`: on `always`, or on `ask` (asking now), pauses and shows the generated code/object summary in chat, waiting for the user's go-ahead or change requests before continuing. On `skip`, continues straight through.
5. If `sap.deployment_mode` is `mcp` (ABAP path): asks the user for a `Z*` package prefix to search (pre-filled from the ticket's `functional_areas` as `ZMASTER_<AREA>*`), searches via `adt_search_objects`, and presents matches to pick from (or create new) — never defaults or auto-selects. Then, via `adt_list_transports`, offers the open/modifiable transports for selection — or offers to create a new one. See `abap-developer/references/transport-guidelines.md`.
6. Updates `tickets/<active>/state.json` milestone status to `building` then `built`.
7. Appends an entry to `tickets/<active>/timeline.jsonl` for every meaningful action (object created/changed, transport touched, test generated) — not just at the end.

After building, suggest the user run `/vinsap:review` and then `/vinsap:test`. Once tests pass, `/vinsap:ship` runs the deploy-readiness checklist (deep-review preference, transport consolidation) — see `commands/ship.md`.
