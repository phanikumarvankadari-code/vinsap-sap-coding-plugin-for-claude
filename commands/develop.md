---
description: Generate code for the next (or specified) milestone, ABAP or Fiori path, with auto-generated tests.
---

Pick the target milestone (next `pending` one in `.sdlc/state.json`, or one the user names).

- If tagged `abap` (or `mixed`, ABAP part): invoke the `abap-developer` skill.
- If tagged `fiori` (or `mixed`, UI part): invoke the `fiori-developer` skill.

Each skill:
1. Generates the code for the milestone, following its guardrails/standards in `references/`.
2. Prefers class-based ABAP over reports/includes for testability.
3. If `sap.deployment_mode` is `mcp` (ABAP path): asks the user for the target package (default `sap.default_package`) and, via `adt_list_transports`, offers the open/modifiable transports for selection — or offers to create a new one — rather than assuming. See `abap-developer/references/transport-guidelines.md`.
4. Auto-generates the matching test (ABAP Unit for ABAP, QUnit for Fiori/UI5 unit-level logic).
5. Updates `.sdlc/state.json` milestone status to `developing` then `developed`.
6. Appends an entry to `.sdlc/timeline.jsonl` for every meaningful action (object created/changed, transport touched, test generated) — not just at the end.

After development, suggest the user run `/vinsap:review` and then `/vinsap:test`.
