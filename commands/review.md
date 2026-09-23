---
description: Quick guideline-compliance check for the current milestone's code, run as a background subagent on a cheap/fast model.
---

Invoke the `code-reviewer` skill in **quick mode**.

1. Read `review.quick_model` from `.sdlc/config.json` (fallback: a cheap/fast model such as Haiku).
2. Dispatch as a subagent (via the Agent tool, `model` override set to the quick model) to check the current milestone's generated code against `abap-developer/references/` (guardrails, Clean ABAP style, package/naming conventions) or `fiori-developer` conventions as applicable.
3. Fire-and-forget — do not block on it; report findings back when the subagent completes.
4. Write findings to `tickets/<active>/outputs/reviews/<milestone>-review.md` and summarize in chat.
5. Append an entry to `tickets/<active>/timeline.jsonl`.

For a thorough, cross-milestone, foreground review that can ask clarifying questions, use `/vinsap:deep-review` instead.
