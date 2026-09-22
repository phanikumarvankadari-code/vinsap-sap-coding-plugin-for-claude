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
- `.sdlc/timeline.jsonl` — **append** (never overwrite) an entry after every meaningful action, not only at stage completion

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
