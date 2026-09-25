# Release Management & Transport Guidelines

Source: Vincit `GUIDELINES_RELEASE.md`. Folded into `abap-developer` (no separate `/vinsap:transport` command for MVP). Access via `adt_create_transport` and `adt_list_transports` over the `vincit-abap-mcp-<SID>` MCP connector, handled defensively:

1. **Transport Naming Convention** — all Transport Requests must strictly use this pattern (max 60 characters):
   `[AI-VSP] <MODULE> | <TICKET_ID> | <Short Description>`
   Example: `[AI-VSP] FI | TICKET-1204 | Add customer name to layout`

2. **Ask, don't assume** — before invoking `adt_create_transport`, always call `adt_list_transports` for the target system and package. Present the user with the open, modifiable transports found (highlighting any already matching the `[AI-VSP]` signature for this ticket) and let them choose: reuse one of the listed transports, or create a new one. Never silently auto-select a transport on the user's behalf.

2a. **Package** — never assume or silently default a package, including `$TMP` and `sap.default_package`. Once the object is ready to leave local staging:
   - Ask the user for a `Z*` package name prefix to search. Pre-fill a suggested prefix from the ticket's `functional_areas` (set by `scope-builder`, see its "Steps" §5) if set, using the `ZMASTER_<AREA>` convention from `package-hierarchy.md` (e.g. `SLS` → suggest `ZMASTER_SLS*`); `sap.default_package` in `.sdlc/config.json` is a fallback hint if `functional_areas` isn't set. Either way it's only a starting suggestion, never auto-selected as the target.
   - Search existing packages matching that prefix via `adt_search_objects` (object type `DEVC`), and present up to 100 matches for the user to pick from.
   - If none fit, or the user wants a new package, fall back to creating one per `abap-developer/references/package-hierarchy.md` naming rules — still asking the user to confirm the generated name before creation.
   - The only exception is local staging itself (`$TMP`) per §3 below — that's not a "target package" choice, it's always the first stop regardless.

3. **Stage Locally First** — develop new logic inside local objects (`$TMP`) using local scratchpads first. Only transfer code to a transportable package (`adt_create_object` / `adt_write_source`) after verifying it compiles cleanly (`adt_syntax_check`).

4. **Release Block** — authorized to save, lock, and activate objects into a Transport Request. **No release-transport tool is exposed by this MCP server at all** — there is nothing to call even if asked; treat any request to release as out of scope and tell the user it must be done manually (e.g. via ADT/Eclipse or the transport management UI) if they truly need it.

5. **Transport scope per package** — one transport touches one application's layers (the leaves under a single `ZMASTER_<AREA>_<APP>` namespace — see `package-hierarchy.md`). Cross-application transports require the user's explicit approval and must be named per §1 with `<MODULE>` set to `<AREA>-<APP>`, e.g. `[AI-VSP] SLS-OSOSTK | TICKET-… | …`.
