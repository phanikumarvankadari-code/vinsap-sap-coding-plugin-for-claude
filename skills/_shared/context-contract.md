# Shared Context Contract

Every VinSAP skill follows this contract for where it reads and writes, so the pipeline stays coherent across commands and across sessions.

## Read from

- `inputs/docs/`, `inputs/emails/`, `inputs/conversations/`, `inputs/jira/` — raw project inputs (read-only source material)
- `.sdlc/config.json` — connectors, product scope, model tiers, screenshot mode, diagram tool, handoff destination
- `.sdlc/state.json` — current stage + per-milestone status
- `outputs/scope.md` — finalized scope, once it exists

## Write to

- `outputs/<stage>/` — this skill's own output (e.g. `outputs/reviews/`, `outputs/docs/`, `outputs/handoff/`)
- `.sdlc/state.json` — update stage/milestone status whenever it changes
- `.sdlc/timeline.jsonl` — **append** (never overwrite) an entry after every meaningful action, not only at stage completion. If `git.enabled` is `true`, each append is immediately followed by a commit — see "Git tracking" below.

## `.sdlc/timeline.jsonl` entry shape

One JSON object per line:

```json
{"timestamp": "2026-09-23T10:42:00Z", "stage": "develop", "skill": "abap-developer", "milestone": "M2", "action": "code_generated", "summary": "Created ZCL_SLS_OSOSTK_DISCOUNT with rate calculation logic", "files_touched": ["ZCL_SLS_OSOSTK_DISCOUNT"]}
```

`action` is a short snake_case tag (`code_generated`, `test_generated`, `test_run`, `test_fixed`, `review_finding`, `milestone_completed`, `decision_made`, `doc_published`, `handoff_created`, …).

## `.sdlc/state.json` shape

```json
{
  "stage": "develop",
  "milestones": [
    {"id": "M1", "title": "...", "type": "abap", "develop": "done", "test": "done"},
    {"id": "M2", "title": "...", "type": "fiori", "develop": "done", "test": "in_progress"}
  ],
  "last_updated": "2026-09-23T10:42:00Z"
}
```

`/vinsap:status` reads this directly. `/vinsap:handoff` reads `timeline.jsonl` directly. Neither should need to reconstruct history from git or from chat scrollback.

## First-write behavior

If `.sdlc/` does not exist yet when a skill runs, create it (this normally happens on `/vinsap:onboard`, but any skill run standalone should still be resilient to a missing folder rather than erroring).

## Git tracking (optional, per `.sdlc/config.json` → `git.enabled`)

If `git.enabled` is `true`, **every `.sdlc/timeline.jsonl` append gets a matching git commit** — 1:1, not a separate judgment call about what counts as "meaningful." Immediately after appending the timeline entry:

1. `git add -A` (or scope it to `inputs/`, `outputs/`, `.sdlc/`, whatever the action actually touched)
2. `git commit -m "vinsap(<stage>): <summary>"` — reuse the timeline entry's own `summary` field as the commit message body, prefixed with the stage (e.g. `vinsap(develop): Created ZCL_SLS_OSOSTK_DISCOUNT with rate calculation logic`)

This keeps `timeline.jsonl` and `git log` as two views of the exact same history — `git log` gives diffs per step, `timeline.jsonl` gives the structured/queryable record `/vinsap:status` and `/vinsap:handoff` read.

If `git.enabled` is `false` or unset, skip this entirely — don't touch git. Never push, never force anything, never touch branches other than the current one — this is local commit-as-you-go only, not a release/deploy action. If a commit fails (e.g. nothing staged, or a hook rejects it), don't retry destructively — surface it and move on, the timeline entry itself already recorded the action.
