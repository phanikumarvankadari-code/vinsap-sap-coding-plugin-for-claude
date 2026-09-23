---
name: code-reviewer
description: Use for /vinsap:review (quick mode, background subagent, cheap model) and /vinsap:deep-review (foreground, smarter model, can ask clarifying questions). Checks generated code against abap-developer and fiori-developer standards.
---

# Code Reviewer

Follow `../_shared/context-contract.md` for read/write conventions. Two modes, chosen by which command invoked this skill.

## Quick mode (`/vinsap:review`)

1. Read `review.quick_model` from `.sdlc/config.json`.
2. Dispatch as a **subagent** via the Agent tool with a `model` override set to the quick model — fire-and-forget, does not block the main session.
3. Scope: the current milestone's code only. Checklist-style: naming/package conventions (`abap-developer/references/package-hierarchy.md`), Clean ABAP style compliance, guardrail compliance (no mutations found in generated code, row caps present, no unindexed heavy-table scans), or the equivalent UI5/QUnit conventions for Fiori milestones.
4. Write findings to `tickets/<active>/outputs/reviews/<milestone>-review.md`, severity-tagged, no scope creep beyond the checklist.
5. Summarize in chat when the subagent completes. Append a `tickets/<active>/timeline.jsonl` entry.

## Deep mode (`/vinsap:deep-review`)

1. Read `review.deep_model` from `.sdlc/config.json`.
2. Run **in the foreground** (main session, not a subagent) — this is required so it can ask the user clarifying questions directly if it hits a gap in understanding, rather than needing to route questions through a parent session.
3. Scope: all developed milestones together. Beyond the quick checklist: cross-milestone consistency, `ZMASTER` layer-dependency compliance (`UI→APP→DB→DDIC`), security review (SQL injection risk, any guardrail bypasses taken — check `tickets/<active>/timeline.jsonl` for `guardrail_bypass` entries), performance red flags (missing indexes, N+1 patterns), full ATC-equivalent static check.
4. If a gap is found (ambiguous requirement, unclear edge case), ask the user directly before finishing that portion of the review.
5. Write findings to `outputs/reviews/<milestone-or-project>-deep-review.md`. Append a `tickets/<active>/timeline.jsonl` entry.

## Finding format (both modes)

`file: severity: problem. fix.` — one line per finding, no praise, no scope creep beyond what each mode's checklist covers.
