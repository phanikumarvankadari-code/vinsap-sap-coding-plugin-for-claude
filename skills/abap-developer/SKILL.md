---
name: abap-developer
description: Use for the ABAP path of /vinsap:build — generates ABAP code (classes preferred) via the target system's Vincit SAP MCP server, enforcing Clean ABAP style, ZMASTER package hierarchy, hard guardrails, system-mode gating, transport handling, and auto-generated ABAP Unit tests. Also handles the ABAP path of /vinsap:ship.
---

# ABAP Developer

Follow `../_shared/context-contract.md` for read/write conventions. This skill operates via whichever `vincit-abap-mcp-*` MCP server is mapped to the target system in `.sdlc/config.json` `sap.systems` (see `config-manager/SKILL.md` — server names are discovered, not hardcoded).

## System mode — check first, see `references/system-modes.md`

Each Vincit SAP MCP server enforces its mode (`dev`/`quality`/`production`) server-side — this plugin mirrors it defensively, it doesn't grant or override it. Before calling any SAP MCP tool, confirm the target system's mode from `.sdlc/config.json`. `/vinsap:build` normally targets a `dev`-mode system only: `quality` allows view/compare/run but never create; `production` allows checking code only and **never touches data at all** — no `adt_run_query`, no table reads, nothing — regardless of `deployment_mode` or any user bypass.

## Hard guardrails — non-negotiable, see `references/guardrails.md` for full detail

- **No DB mutations** (`INSERT`/`UPDATE`/`MODIFY`/`DELETE` Open SQL) via `adt_run_query` unless the user explicitly bypasses in the active prompt.
- **No unindexed scans** on heavy transactional tables (`BSEG`, `BKPF`, `ACDOCA`, `MARA`, …) — require a key/indexed `WHERE` field.
- **Row cap** — always append `UP TO 100 ROWS` to selections.
- **Linter gate** — must pass `adt_syntax_check` and `adt_run_atc_check` before any `adt_write_source`/`adt_create_object` call.
- **No release** — `adt_create_transport`/`adt_list_transports` are available, but no release-transport tool is exposed by this MCP server; never attempt to release a transport through it.

## Coding standard — see `references/coding-standards.md`

Clean ABAP per the official SAP style guide: expressions over statements, small methods (20–30 lines), descriptive names, no obsolete statements, fail-fast with class exceptions. **Prefer class-based ABAP over reports/includes** — easier to unit test, keeps logic modular. See `references/coding-standards.md` § "Class granularity" for how many classes a milestone actually needs — don't over-split.

## Package hierarchy — see `references/package-hierarchy.md`

All transportable objects live under `ZMASTER_<AREA>_<APP><LAYER>`. Follow the fixed area codes (classical ECC module codes — `FI`/`SD`/`MM`/`PP`/`LE`/`HR`/`AA`/`CS`/`CORE`), layer codes (`DDIC/DB/APP/UI`), strict layer-dependency direction (`UI→APP→DB→DDIC`), 30-char cap, and bottom-up creation order. Never create a top-level `Z*` package.

## Transport handling — see `references/transport-guidelines.md`

Folded into this skill (no separate `/vinsap:transport` command). Stage new logic locally (`$TMP`) first. Before creating a transport, check for an existing open one matching the `[AI-VSP] <MODULE> | <TICKET_ID> | <desc>` naming signature and reuse it. Create/save/activate are allowed. **No release-transport tool is exposed by the MCP server at all** — there's nothing to call even with a bypass; release happens outside this plugin.

## Testing — see `references/unittest-guidelines.md`

Auto-generate an ABAP Unit test class alongside every class/method generated, following the AAA pattern and naming convention. No real DB dependency in tests — inject/mock instead.

## Deployment mode

Read `sap.deployment_mode` from `.sdlc/config.json` before generating code, and tell the user which mode is active:

- **`mcp`** (default) — push, save, activate, and manage the transport directly through the `vincit-abap-mcp-<SID>` connector, per the steps below.
- **`manual`** — generate the code and run it through the same guardrails/lint/style checks locally, but do not push through the MCP connector. Instead write the finished object source to `tickets/<active>/outputs/build/<milestone>/`, plus an instruction sheet (object name, target package, transport request name/number to use) for the user to apply themselves via ADT.

## Build steps (`/vinsap:build`)

1. Read the target milestone from `tickets/<active>/state.json` and `tickets/<active>/outputs/spec.md` (plus its object preview in `outputs/plan.md`, if present).
2. Design the class(es)/objects needed, checking `references/package-hierarchy.md` for correct placement. Use `adt_search_objects`/`adt_get_source` to check for reuse and inspect existing structures.
3. Generate code, respecting all guardrails above. In `mcp` mode, create/write via `adt_create_object`/`adt_write_source`; in `manual` mode, generate locally without calling those.
4. Run `adt_syntax_check` and `adt_run_atc_check`; fix issues before saving/activating (or before handing off, in `manual` mode).
5. Generate the matching ABAP Unit test class per `references/unittest-guidelines.md`.
6. **Local-review checkpoint**: check `tickets/<active>/state.json` → `preferences.local_review`. On `always`, or on `ask` (asking now), pause and show the generated code/object summary in chat — wait for the user's go-ahead or change requests before continuing to step 7. On `skip`, continue straight through.
7. Package and transport, per `references/transport-guidelines.md` §2a — never auto-select either:
   - **Package**: ask for a `Z*` prefix to search — pre-fill from the ticket's `functional_areas` using `ZMASTER_<AREA>*` (e.g. `SD` → `ZMASTER_SD*`) if set. Search via `adt_search_objects` (type `DEVC`), present up to 100 matches for the user to pick, or create a new one (confirmed name) if none fit.
   - **Transport**: call `adt_list_transports`, present the open/modifiable transports found (flagging any matching the `[AI-VSP]` signature) for the user to pick from, or offer to create a new one via `adt_create_transport` if none fit.
   Stage in `$TMP` first, then activate into the chosen package/transport. In `manual` mode, note the package/transport name to use in the instruction sheet instead of calling `adt_create_transport` directly.
8. Update `tickets/<active>/state.json` milestone status (`build: "building"` then `"built"`); append a `tickets/<active>/timeline.jsonl` entry for each meaningful action (object created, transport touched, test generated) — not just once at the end.

## Ship steps (`/vinsap:ship`, ABAP/mixed milestones)

Runs **per milestone**, right after `/vinsap:test` passes for it — transport is staged incrementally, not deferred:

1. If this is the first `/vinsap:ship` run for the ticket, ask whether `/vinsap:deep-review` should be required before shipping — `Always`/`Ask each time`/`Skip` — store as `preferences.deep_review` in `state.json`.
2. Confirm `test: "done"` for this milestone; refuse to ship if not.
3. Apply the `deep_review` preference from step 1 (require it, ask now, or skip, per the stored value).
4. List the transport(s) touched by this milestone (from the timeline).
5. Write/append `tickets/<active>/outputs/ship.md` with this milestone's entry; update `state.json` (`ship: "done"`).
6. Append a `tickets/<active>/timeline.jsonl` entry.

Doesn't release or deploy anything itself — release stays a manual, outside-the-plugin step.

## Guardrail exceptions

If the user explicitly bypasses a guardrail (mutation, release), record it clearly in the timeline entry (`action: "guardrail_bypass"`) — this feeds the Technical Doc's Authorization/Security section later.
