# Release Management & Transport Guidelines

Source: Vincit `GUIDELINES_RELEASE.md`. Folded into `abap-developer` (no separate `/vinsap:transport` command for MVP). Access via `adt_create_transport` and `adt_list_transports` over the `vincit-abap-mcp-<SID>` MCP connector, handled defensively:

1. **Transport Naming Convention** — all Transport Requests must strictly use this pattern (max 60 characters):
   `[AI-VSP] <MODULE> | <TICKET_ID> | <Short Description>`
   Example: `[AI-VSP] FI | TICKET-1204 | Add customer name to layout`

2. **Check Before Creating** — before invoking `adt_create_transport`, always call `adt_list_transports` to verify whether an open, eligible transport matching the `[AI-VSP]` signature already exists for this task. If it does, reuse it.

3. **Stage Locally First** — develop new logic inside local objects (`$TMP`) using local scratchpads first. Only transfer code to a transportable package (`adt_create_object` / `adt_write_source`) after verifying it compiles cleanly (`adt_syntax_check`).

4. **Release Block** — authorized to save, lock, and activate objects into a Transport Request. **No release-transport tool is exposed by this MCP server at all** — there is nothing to call even if asked; treat any request to release as out of scope and tell the user it must be done manually (e.g. via ADT/Eclipse or the transport management UI) if they truly need it.

5. **Transport scope per package** — one transport touches one application's layers (the leaves under a single `ZMASTER_<AREA>_<APP>` namespace — see `package-hierarchy.md`). Cross-application transports require the user's explicit approval and must be named per §1 with `<MODULE>` set to `<AREA>-<APP>`, e.g. `[AI-VSP] SLS-OSOSTK | TICKET-… | …`.
