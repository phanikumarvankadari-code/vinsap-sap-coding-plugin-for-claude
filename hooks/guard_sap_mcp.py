#!/usr/bin/env python3
"""
VinSAP PreToolUse guard for Vincit SAP MCP (vincit-abap-mcp-*) tool calls.

Mechanically enforces, independent of model behavior:
  - system mode (dev/quality/production), mapped from .sdlc/config.json
  - the SQL guardrails (no mutation, row cap, no unindexed heavy-table scans)

Contract: reads the PreToolUse hook JSON payload from stdin
({"tool_name": ..., "tool_input": {...}, "cwd": ...}). Exit 0 to allow the
call through; exit 2 and print the reason to stderr to block it.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Tools that only read metadata/source/structure — never touch table data,
# never mutate, never execute business logic. Allowed even on production,
# and allowed even if the system's mode can't be determined yet.
READ_ONLY_SAFE_TOOLS = {
    "adt_get_source",
    "adt_search_objects",
    "adt_get_object_structure",
    "adt_get_type_hierarchy",
    "adt_get_callers",
    "adt_get_callees",
    "adt_pretty_print",
    "adt_get_text_elements",
    "adt_get_revisions",
    "adt_list_transports",
    "adt_list_git_repos",
    "adt_get_atc_customizing",
    "adt_check_git_repo",
    "adt_get_git_repo_branches",
    "adt_compare_versions",
    "adt_list_traces",
    "adt_list_trace_requests",
    "adt_get_trace_hitlist",
    "adt_get_trace_statements",
    "adt_get_trace_dbaccess",
    "adt_get_cds_element_info",
    "knowledge_query_rules",
}

# Tools that create/modify/delete objects, transports, or repo state.
WRITE_TOOLS = {
    "adt_write_source",
    "adt_create_object",
    "adt_delete_object",
    "adt_create_transport",
    "adt_set_text_elements",
    "adt_create_git_repo",
    "adt_push_git_repo",
    "adt_stage_git_repo",
    "adt_switch_git_repo_branch",
    "adt_unlink_git_repo",
    "adt_pull_git_repo",
    "adt_delete_trace",
    "adt_delete_trace_config",
    "adt_create_trace",
    "adt_debugger_attach",
    "adt_debugger_set_breakpoints",
    "adt_debugger_set_variable_value",
    "adt_debugger_delete_listener",
}

# Tools that execute code or read live data — allowed on dev/quality (with
# the query guardrails below on adt_run_query), never on production.
DATA_OR_EXEC_TOOLS = {
    "adt_run_query",
    "adt_get_table_contents",
    "adt_run_unit_tests",
    "adt_run_atc_check",
    "adt_syntax_check",
    "adt_analyze_call_graph",
    "adt_compare_call_graphs",
    "adt_debugger_listen",
    "adt_debugger_step",
    "adt_debugger_stack",
    "adt_debugger_variables",
}

HEAVY_TABLES = {"BSEG", "BKPF", "ACDOCA", "MARA"}
MUTATION_KEYWORDS = re.compile(r"\b(INSERT|UPDATE|MODIFY|DELETE)\b", re.IGNORECASE)
ROW_CAP_PATTERN = re.compile(r"\bUP\s+TO\s+\d+\s+ROWS\b", re.IGNORECASE)
WHERE_PATTERN = re.compile(r"\bWHERE\b", re.IGNORECASE)


def block(reason: str) -> None:
    sys.stderr.write(reason + "\n")
    sys.exit(2)


def find_project_config(start: Path) -> dict | None:
    for candidate in [start, *start.parents]:
        cfg_path = candidate / ".sdlc" / "config.json"
        if cfg_path.is_file():
            try:
                return json.loads(cfg_path.read_text())
            except (json.JSONDecodeError, OSError):
                return None
    return None


def find_system_mode(config: dict | None, server_name: str) -> str | None:
    if not config:
        return None
    systems = (config.get("sap") or {}).get("systems") or {}
    for _role, sysinfo in systems.items():
        if isinstance(sysinfo, dict) and sysinfo.get("mcp_server") == server_name:
            return sysinfo.get("mode")
    return None


def collect_strings(value, acc: list[str]) -> None:
    if isinstance(value, str):
        acc.append(value)
    elif isinstance(value, dict):
        for v in value.values():
            collect_strings(v, acc)
    elif isinstance(value, list):
        for v in value:
            collect_strings(v, acc)


def check_query_guardrails(tool_input: dict) -> str | None:
    """Returns a block reason, or None if the query passes the guardrails."""
    strings: list[str] = []
    collect_strings(tool_input, strings)
    blob = "\n".join(strings)

    if MUTATION_KEYWORDS.search(blob):
        return (
            "Blocked: adt_run_query appears to contain a mutating statement "
            "(INSERT/UPDATE/MODIFY/DELETE). Data mutations are not permitted "
            "through VinSAP. See abap-developer/references/guardrails.md."
        )

    touched_heavy = [t for t in HEAVY_TABLES if re.search(rf"\b{t}\b", blob, re.IGNORECASE)]
    if touched_heavy and not WHERE_PATTERN.search(blob):
        return (
            f"Blocked: query touches heavy table(s) {', '.join(touched_heavy)} "
            "without a WHERE clause on a key/indexed field. See "
            "abap-developer/references/guardrails.md."
        )

    if not ROW_CAP_PATTERN.search(blob):
        return (
            "Blocked: query is missing a row cap (e.g. 'UP TO 100 ROWS'). "
            "See abap-developer/references/guardrails.md."
        )

    return None


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Can't parse the hook payload — fail open rather than break the session.
        sys.exit(0)

    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {}) or {}
    cwd = Path(payload.get("cwd") or ".")

    match = re.match(r"^mcp__(vincit-abap-mcp-[^_]+(?:-[^_]+)*)__(.+)$", tool_name)
    if not match:
        sys.exit(0)  # not a Vincit SAP MCP tool call, nothing to guard

    server_name, adt_tool = match.group(1), match.group(2)

    if adt_tool in READ_ONLY_SAFE_TOOLS:
        sys.exit(0)

    config = find_project_config(cwd)
    mode = find_system_mode(config, server_name)

    if mode is None:
        block(
            f"Blocked: system mode for '{server_name}' is not configured in "
            ".sdlc/config.json (sap.systems.*.mode). Run /vinsap:config to map "
            "this connected MCP server to a system and mode (dev/quality/production) "
            "before using it beyond read-only lookups."
        )
        return

    if mode == "production":
        block(
            f"Blocked: '{server_name}' is a production system. VinSAP never runs, "
            "writes, or reads data against production — read-only code inspection "
            "only. See abap-developer/references/system-modes.md."
        )
        return

    if mode == "quality":
        if adt_tool in WRITE_TOOLS:
            block(
                f"Blocked: '{server_name}' is a quality system. Code creation is "
                "not permitted there — view, compare, and run are allowed, but "
                "writes only ever reach quality via transport promotion. See "
                "abap-developer/references/system-modes.md."
            )
            return
        if adt_tool == "adt_run_query":
            reason = check_query_guardrails(tool_input)
            if reason:
                block(reason)
                return
        sys.exit(0)

    if mode == "dev":
        if adt_tool == "adt_run_query":
            reason = check_query_guardrails(tool_input)
            if reason:
                block(reason)
                return
        sys.exit(0)

    block(f"Blocked: unrecognized system mode '{mode}' for '{server_name}'.")


if __name__ == "__main__":
    main()
