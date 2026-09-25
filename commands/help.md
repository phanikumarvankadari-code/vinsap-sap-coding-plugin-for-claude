---
description: Explain every VinSAP command — what it does, an example, and the choices it asks you to make.
---

No dedicated skill — print the reference below directly (don't re-derive it from the individual command files each time; keep this file itself in sync when a command changes).

If the user names a specific command (e.g. `/vinsap:help build`), show only that command's entry, expanded with a bit more detail from its own `commands/<name>.md`. Otherwise show the full list below.

---

## VinSAP Command Reference

**Once per project:**

### `/vinsap:config`
Sets up connectors, SAP systems, deployment mode, and preferences — shared by every ticket.
- Example: `/vinsap:config`
- Choices you make: which SAP systems map to `dev`/`quality`/`production` mode; `deployment_mode` (`mcp` push-directly vs `manual` generate-and-apply-yourself); diagram tool (`draw.io` vs `mermaid`); review model tiers (cheap model for `/vinsap:review`, stronger one for `/vinsap:deep-review`); screenshot mode (`auto` vs `manual`); handoff default destination; whether to track `tickets/`/`.sdlc/` in git; your Jira/Atlassian login email.

### `/vinsap:intent` (alias `/vinsap:init`, legacy alias `/vinsap:onboard`)
First run: checks prerequisites. Every run after: starts a new ticket and captures the ask into `intent.md`.
- Example: `/vinsap:intent ADSD-1204`
- Choices you make: the ticket ID; input source (pull from Jira via `mcp-atlassian`, or manually drop files into `inputs/`); corrections to the drafted `intent.md` before moving on.

**Per ticket:**

### `/vinsap:spec` (aliases `/vinsap:analyze`, `/vinsap:start`, legacy alias `/vinsap:scope`)
Reads `intent.md` + inputs, asks clarifying questions, writes the finalized `outputs/spec.md`.
- Example: `/vinsap:spec`
- Choices you make: answers to whatever gaps/open questions it surfaces; which functional/solution area(s) this ticket falls under (`FI`/`SD`/`MM`/`PP`/`LE`/`HR`/`AA`/`CS`/`CORE`); whether to start the Functional Document now or later.

### `/vinsap:plan` (legacy alias `/vinsap:milestones`)
Breaks the spec into milestones (tagged `abap`/`fiori`/`mixed`), previews anticipated objects, writes `outputs/plan.md`.
- Example: `/vinsap:plan`
- Choices you make: whether to reuse an object it flags instead of building new; **review code locally before it ships?** — `Always`/`Ask each time`/`Skip` (asked once per ticket, remembered for every milestone).

### `/vinsap:build` (legacy alias `/vinsap:develop`)
Generates code + tests for the next (or a named) milestone.
- Example: `/vinsap:build M2`
- Choices you make: if your `local_review` preference is `always`/`ask`, whether to accept the generated code or request changes before it continues; the `Z*` package to target (searched and listed, never defaulted); which transport to reuse or whether to create a new one.

### `/vinsap:review`
Quick guideline check on the current milestone's code, runs in the background on a cheap model. No choices — fire-and-forget.
- Example: `/vinsap:review`

### `/vinsap:test`
Runs ABAP Unit/QUnit/Playwright tests, auto-fixes failures up to a retry cap.
- Example: `/vinsap:test`
- Choices you make: only if it exhausts the retry cap and asks you how to proceed on a stubborn failure.

### `/vinsap:deep-review` *(optional)*
Thorough, cross-milestone review in the foreground on a stronger model — can ask you clarifying questions mid-review.
- Example: `/vinsap:deep-review`
- Choices you make: answers to any clarifying questions it raises. Whether this runs at all is controlled by `/vinsap:ship`'s deep-review preference, not required directly.

### `/vinsap:ship`
Deploy-readiness checklist. ABAP/mixed milestones ship one at a time; Fiori/UI5 ships once, after the whole track is built and tested.
- Example: `/vinsap:ship`
- Choices you make: the first time per ticket, **require deep-review before shipping?** — `Always`/`Ask each time`/`Skip` (remembered after that).

### `/vinsap:docs`
Interactively generates a Functional, Technical, or Test document, optionally publishes to Confluence.
- Example: `/vinsap:docs`
- Choices you make: which document type; which sections to include (checkbox list, all on by default, can add custom ones); anything it can't derive from `spec.md`/`plan.md`/code/tests; whether to publish to Confluence (new page or update existing) — publishing auto-comments the page link on the linked Jira issue.

**Anytime, on the active ticket:**

### `/vinsap:status`
Plain-text progress view. `/vinsap:status all` lists every ticket. No choices.
- Example: `/vinsap:status` or `/vinsap:status all`

### `/vinsap:switch <TICKET-ID>`
Jumps to a ticket you already started, without re-running `/vinsap:intent`.
- Example: `/vinsap:switch ADSD-1301`
- Choices you make: which ticket, if you don't name one — it lists what's available.

### `/vinsap:handoff`
Narrative summary of everything that happened on the active ticket. Always saved locally; optionally also published.
- Example: `/vinsap:handoff`
- Choices you make: publish externally as a Jira comment, a Confluence page, or skip (local file is always saved either way).
