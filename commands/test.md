---
description: Run all tests for the current/all milestones (ABAP Unit, QUnit, Playwright), auto-fixing failures up to a retry cap.
---

Invoke the `test-runner` skill.

1. Run ABAP Unit tests (via `vincit-abap-mcp-<SID>` MCP) and QUnit tests for the target milestone(s).
2. Run Playwright e2e tests as a **background subagent** (fire-and-forget, does not block the main session).
3. On failure: analyze the assertion/trace, attempt a fix in the source or test, re-run. Repeat up to a configured retry cap (default 3) before flagging the milestone as blocked and asking the user.
4. Update `.sdlc/state.json` milestone status (`testing` → `tested`/`blocked`).
5. Append an entry to `.sdlc/timeline.jsonl` per test run, including auto-fix attempts.
6. Report a pass/fail summary to the user.
