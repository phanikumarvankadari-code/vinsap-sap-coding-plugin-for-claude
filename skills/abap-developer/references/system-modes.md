# System Modes

Every Vincit SAP MCP server enforces one of three modes **server-side** — `dev`, `quality`, `production` — as a rule of the server itself, not something this plugin grants or can override. `abap-developer` follows these rules by design, and they're additionally **mechanically enforced** by the `hooks/guard_sap_mcp.py` PreToolUse hook (see `../../../hooks/hooks.json`), which blocks any `mcp__vincit-abap-mcp-*` tool call that violates the target system's mode — independent of what the model decides to do. This is belt-and-suspenders: the skill shouldn't attempt a disallowed call, and the hook stops it even if it does.

Mode per connected system is recorded in `.sdlc/config.json` `sap.systems.<ROLE>.mode` during `/vinsap:config` discovery.

## `dev`

- Full access: create, update, read, run — all guardrails in `guardrails.md` apply as written, including the explicit-bypass exception for DB mutations.
- This is where `/vinsap:develop` normally targets.

## `quality`

- **No code creation.** `adt_write_source`/`adt_create_object` are not available here — don't attempt them.
- Allowed: view code (`adt_get_source`), compare code (`adt_compare_versions`), and run code remotely (`adt_run_unit_tests`, `adt_run_atc_check`, `adt_syntax_check`, `adt_run_query` — still row-capped, still no mutations).
- Writes only ever reach a `quality` system via transport promotion, never via this plugin creating/editing code directly on it.

## `production`

- **Cannot run anything.** Read-only at most — check/view code (`adt_get_source`, `adt_search_objects`) and general system state.
- **Never access or query production data.** Do not call `adt_run_query`, `adt_get_table_contents`, or any data-reading tool against a `production`-mode system, even read-only, even row-capped, even if asked — this is the reason the guardrails exist in the first place.
- No create, no write, no run, no data access. If a task seems to require touching production, stop and tell the user this has to happen outside the plugin.

## Applying this

Check the target system's mode from `.sdlc/config.json` before calling *any* SAP MCP tool, not just writes — a `quality`/`production` system picked by mistake should be caught at the very first call, since it usually means the wrong system was targeted. `test-runner` (for `adt_run_unit_tests`/`adt_run_query`) follows the same gating.
