---
description: Generate code for the next (or specified) milestone, ABAP or Fiori path, with auto-generated tests.
---

Pick the target milestone (next `pending` one in `.sdlc/state.json`, or one the user names).

- If tagged `abap` (or `mixed`, ABAP part): invoke the `abap-developer` skill.
- If tagged `fiori` (or `mixed`, UI part): invoke the `fiori-developer` skill.

Each skill:
1. Generates the code for the milestone, following its guardrails/standards in `references/`.
2. Prefers class-based ABAP over reports/includes for testability.
3. Auto-generates the matching test (ABAP Unit for ABAP, QUnit for Fiori/UI5 unit-level logic).
4. Updates `.sdlc/state.json` milestone status to `developing` then `developed`.
5. Appends an entry to `.sdlc/timeline.jsonl` for every meaningful action (object created/changed, transport touched, test generated) — not just at the end.

After development, suggest the user run `/vinsap:review` and then `/vinsap:test`.
