---
description: Thorough, cross-milestone review run in the foreground on a smarter model — can ask clarifying questions before finishing.
---

Invoke the `code-reviewer` skill in **deep mode**.

1. Read `review.deep_model` from `.sdlc/config.json` (fallback: the strongest available model).
2. Run **in the foreground** (not a subagent) so it can ask the user clarifying questions directly if it finds gaps in understanding (ambiguous requirement, unclear edge case) before finishing the review.
3. Analyze across all developed milestones together: consistency, `ZMASTER` package/layer-dependency compliance, security (SQL injection risk, guardrail exceptions taken), performance red flags, full ATC-equivalent static check.
4. Write findings to `tickets/<active>/outputs/reviews/<milestone-or-project>-deep-review.md` and summarize in chat.
5. Append an entry to `tickets/<active>/timeline.jsonl`.

Treat this as the gate before `/vinsap:docs`. For a fast, single-milestone, background check, use `/vinsap:review` instead.
