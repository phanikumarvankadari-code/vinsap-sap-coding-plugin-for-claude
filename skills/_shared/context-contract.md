# Shared Context Contract

Every VinSAP skill follows this contract for where it reads and writes, so the pipeline stays coherent across commands, across tickets, and across sessions.

## Project structure — shared config, per-ticket everything else

```
project-root/
  .sdlc/
    config.json            # shared across ALL tickets: connectors, SAP systems, model tiers, diagram tool, git usage
    active_ticket.json      # {"active_ticket": "TICKET-1204"} — which ticket commands target right now
  tickets/
    <TICKET-ID>/
      inputs/docs/ emails/ conversations/ jira/
      outputs/scope.md, reviews/, docs/, handoff/, develop/
      state.json             # this ticket's stage + per-milestone status
      timeline.jsonl          # this ticket's append-only history
```

`config.json` does **not** change per ticket — connectors, SAP system/mode mappings, model tiers, diagram tool, screenshot mode, handoff default, git usage are engagement-wide settings, set once via `/vinsap:config`. Everything else — inputs, outputs, scope, milestones, state, timeline — is scoped to one ticket at a time under `tickets/<TICKET-ID>/`.

## Resolving the active ticket

1. Read `.sdlc/active_ticket.json`. If it doesn't exist or names a ticket whose `tickets/<ID>/` folder is missing, stop and tell the user to run `/vinsap:onboard` (new ticket) or `/vinsap:switch <TICKET-ID>` (existing ticket) — don't guess or silently create one.
2. Every path below that says `<ticket>/...` means `tickets/<active_ticket>/...`, where `<active_ticket>` is that resolved ID.
3. `/vinsap:onboard` creates a new ticket folder and sets it active. `/vinsap:switch <TICKET-ID>` changes which ticket is active without creating anything new (errors if that ticket folder doesn't exist).

## Read from

- `<ticket>/inputs/docs/`, `<ticket>/inputs/emails/`, `<ticket>/inputs/conversations/`, `<ticket>/inputs/jira/` — raw ticket inputs (read-only source material)
- `.sdlc/config.json` — connectors, product scope, model tiers, screenshot mode, diagram tool, handoff destination (shared, not ticket-scoped)
- `.sdlc/active_ticket.json` — which ticket is active
- `<ticket>/state.json` — current stage + per-milestone status for this ticket
- `<ticket>/outputs/scope.md` — this ticket's finalized scope, once it exists

## Write to

- `<ticket>/outputs/<stage>/` — this skill's own output for this ticket (e.g. `<ticket>/outputs/reviews/`, `<ticket>/outputs/docs/`, `<ticket>/outputs/handoff/`)
- `<ticket>/state.json` — update stage/milestone status whenever it changes
- `<ticket>/timeline.jsonl` — **append** (never overwrite) an entry after every meaningful action, not only at stage completion. If `git.enabled` is `true`, each append is immediately followed by a commit — see "Git tracking" below.

Never write ticket-scoped output to `.sdlc/` or to another ticket's folder. Never write shared config (`.sdlc/config.json`) from a ticket-scoped skill — that's `config-manager`'s job alone.

## `<ticket>/timeline.jsonl` entry shape

One JSON object per line:

```json
{"timestamp": "2026-09-23T10:42:00Z", "stage": "develop", "skill": "abap-developer", "milestone": "M2", "action": "code_generated", "summary": "Created ZCL_SLS_OSOSTK_DISCOUNT with rate calculation logic", "files_touched": ["ZCL_SLS_OSOSTK_DISCOUNT"]}
```

`action` is a short snake_case tag (`code_generated`, `test_generated`, `test_run`, `test_fixed`, `review_finding`, `milestone_completed`, `decision_made`, `doc_published`, `handoff_created`, `guardrail_bypass`, …). No `ticket` field needed inside the entry — the file's location under `tickets/<TICKET-ID>/` already scopes it.

## `<ticket>/state.json` shape

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

`/vinsap:status` reads this (for the active ticket, or a named one) directly. `/vinsap:handoff` reads `<ticket>/timeline.jsonl` directly. Neither should need to reconstruct history from git or from chat scrollback.

## `.sdlc/active_ticket.json` shape

```json
{"active_ticket": "ADSD-1204", "last_switched": "2026-09-23T10:42:00Z"}
```

## First-write behavior

If `.sdlc/` does not exist yet when a skill runs, create it (this normally happens on the very first `/vinsap:onboard`). If `tickets/<ID>/` doesn't exist for the active ticket, that's an error state, not something to silently create — see "Resolving the active ticket" above.

## Git tracking (optional, per `.sdlc/config.json` → `git.enabled`)

If `git.enabled` is `true`, **every `<ticket>/timeline.jsonl` append gets a matching git commit** — 1:1, not a separate judgment call about what counts as "meaningful." Immediately after appending the timeline entry:

1. `git add -A` (or scope it to `tickets/<ID>/`, `.sdlc/`, whatever the action actually touched)
2. `git commit -m "vinsap(<ticket>/<stage>): <summary>"` — reuse the timeline entry's own `summary` field as the commit message body, prefixed with the ticket and stage (e.g. `vinsap(ADSD-1204/develop): Created ZCL_SLS_OSOSTK_DISCOUNT with rate calculation logic`)

This keeps `timeline.jsonl` and `git log` as two views of the exact same history, now legible across multiple tickets in the same repo.

If `git.enabled` is `false` or unset, skip this entirely — don't touch git. Never push, never force anything, never touch branches other than the current one — this is local commit-as-you-go only, not a release/deploy action. If a commit fails (e.g. nothing staged, or a hook rejects it), don't retry destructively — surface it and move on, the timeline entry itself already recorded the action.
