# Hard Behavioral Locks

Source: Vincit `GUARDRAILS.md`. Operates via the `vincit-abap-mcp-<SID>` MCP server connected to a live SAP ECC ABAP environment.

The no-mutation, row-cap, and unindexed-heavy-table-scan rules below are additionally **mechanically enforced** by the `hooks/guard_sap_mcp.py` PreToolUse hook — it inspects every `adt_run_query` call and blocks it before it reaches the server if it violates these rules, regardless of what this skill intends.

## No Database Mutations

Strictly forbidden from writing or executing `INSERT`, `UPDATE`, `MODIFY`, or `DELETE` Open SQL statements inside the `adt_run_query` tool unless the user explicitly bypasses this rule in the active chat prompt.

## No Massive Table Scans

Never write queries targeting heavy transactional tables (e.g. `BSEG`, `BKPF`, `ACDOCA`, `MARA`) without providing a primary key or an indexed field in the `WHERE` clause.

## Row Thresholds

Always append `UP TO 100 ROWS` to any data selection to protect application memory.

## Linter Gate

Before calling `adt_write_source`/`adt_create_object` to save or activate code in SAP, successfully run `adt_syntax_check` and `adt_run_atc_check`. If either reports errors or critical warnings, fix the code before pushing.

## Package Default

If a task requires creating new global classes, use a designated development package (`$TMP` for local staging, or the correct custom `ZMASTER_*` package per `package-hierarchy.md` once ready to transport).
