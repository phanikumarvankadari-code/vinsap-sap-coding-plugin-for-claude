---
name: test-runner
description: Use for /vinsap:test — runs ABAP Unit, QUnit, and Playwright tests for milestone(s), auto-fixing failures up to a retry cap before flagging a milestone blocked.
---

# Test Runner

Follow `../_shared/context-contract.md` for read/write conventions.

## Steps

1. Identify the target milestone(s) from `tickets/<active>/state.json` (default: all milestones in `develop: "done"` state not yet `test: "done"`).
2. Run **ABAP Unit** tests via `vincit-abap-mcp-<SID>` MCP for ABAP milestones.
3. Run **QUnit** tests for Fiori/UI5 milestones.
4. Run **Playwright** e2e tests as a **background subagent** (fire-and-forget) — do not block the main session waiting on browser tests.
5. On any failure:
   a. Read the assertion/stack trace and locate the failing code.
   b. Attempt a fix (in source code or in the test, whichever is actually wrong).
   c. Re-run the specific failing test.
   d. Repeat up to a retry cap (default 3 attempts) per failure.
   e. If still failing after the cap, mark the milestone `test: "blocked"` in `tickets/<active>/state.json` and flag it to the user with the failure detail — do not keep retrying silently.
6. Update `tickets/<active>/state.json` (`test: "done"` on full pass).
7. Append a `tickets/<active>/timeline.jsonl` entry for every test run and every auto-fix attempt (not just the final outcome).
8. Report a pass/fail summary per milestone to the user.

## Notes

- Auto-fix must re-run the specific test it fixed, not just assume the fix worked.
- Never weaken a test's assertions to force a pass — a failing test must be fixed by fixing the code, or escalated to the user; test-gaming is not an auto-fix.
