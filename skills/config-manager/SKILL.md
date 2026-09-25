---
name: config-manager
description: Use for /vinsap:config — creates/updates .sdlc/config.json with connector setup, SAP systems, prerequisites, diagram tool, review model tiers, screenshot mode, and git usage.
---

# Config Manager

Follow `../_shared/context-contract.md` for read/write conventions.

## Fields to manage in `.sdlc/config.json`

`sap` is **top-level**. This is the authoritative shape: `hooks/guard_sap_mcp.py::find_system_mode()` reads `config["sap"]["systems"]` directly, so it must match exactly. `mcp-atlassian`'s own auth needs zero fields in `.sdlc/config.json` (OAuth BYOT, see below) — but `connectors.mcp-atlassian.atlassian_login` still exists, for a different reason: see "Atlassian connector" below.

```json
{
  "connectors": {
    "mcp-atlassian": {
      "atlassian_login": ""
    }
  },
  "sap": {
    "systems": {
      "DEV": { "mcp_server": "vincit-abap-mcp-S4H", "mode": "dev" }
    },
    "default_package": "ZSD",
    "deployment_mode": "mcp"
  },
  "diagram_tool": "drawio",
  "review": { "quick_model": "haiku", "deep_model": "opus" },
  "documentation": { "screenshot_mode": "auto", "confluence_parent_id": "10682105864" },
  "handoff": { "destination": "file" },
  "git": { "enabled": false }
}
```

## Steps

1. Read the existing `.sdlc/config.json` if present; show the user what's already set vs. what's still missing.
2. Ask for missing values conversationally, grouped by section (Jira/Atlassian login, prerequisites, deployment mode, diagram tool, model tiers, screenshot mode, git usage, handoff default) — don't ask everything as one giant form. There's no project-wide "products in scope" field here anymore — that turned out unused in practice; functional/solution area is now asked **per ticket** in `scope-builder` instead (see its `functional_areas` step), since it varies ticket to ticket and actually feeds into something: pre-filling the `Z*` package-search prefix in `abap-developer`.
3. Re-run the prerequisite check from `onboarding-guide/references/prerequisites.md` if the user wants to change tooling.
4. Write the merged config back to `.sdlc/config.json` — shared across every ticket, not ticket-scoped.
5. If a ticket is currently active (`.sdlc/active_ticket.json`), append an entry summarizing what changed to that ticket's `timeline.jsonl`. If no ticket is active yet (e.g. this is the project's first-ever `/vinsap:config` run before any `/vinsap:onboard`), skip this — there's no ticket-scoped file to write to yet.

## Deployment mode

Ask the user to choose `sap.deployment_mode`:

- **`mcp`** (default) — `abap-developer` pushes code, creates/activates transports, and runs the linter directly through the `vincit-abap-mcp-<SID>` connector (the Vincit SAP MCP VS Code extension). Fully automated per `abap-developer/references/transport-guidelines.md`.
- **`manual`** — `abap-developer` still generates the code and runs it through the same guardrails/style checks locally, but does **not** push anything through the MCP connector. Instead it writes the finished object source to `tickets/<active>/outputs/develop/<milestone>/` with an instruction sheet (object name, package, transport request to use) for the user to apply themselves via ADT (Eclipse/VS Code ABAP Development Tools).

`sap.deployment_mode` is read by `abap-developer` on every `/vinsap:develop` run — surface which mode is active before generating code so the user isn't surprised by whether something landed in the system or just on disk.

`sap.default_package` is only an optional **search-prefix hint** — never auto-selected as the target. When `deployment_mode` is `mcp`, `abap-developer` asks the user for a `Z*` package prefix to search (e.g. `ZSD*`), searches existing packages via `adt_search_objects`, and presents up to 100 matches for the user to pick from (or create a new one) — never silently picks `sap.default_package`, `$TMP`, or `ZMASTER` on its own. Transport works the same way: `adt_list_transports` offers a selection of the currently open/modifiable transports on the target system to reuse, or lets the user choose to create a new one. See `abap-developer/references/transport-guidelines.md` §2/§2a.

## Git usage

Ask the user whether this project should track its VinSAP artifacts (`tickets/`, `.sdlc/`) in git — set `git.enabled` accordingly:

- **`true`** — every ticket's `timeline.jsonl` append gets a matching git commit, 1:1 (see `_shared/context-contract.md` → "Git tracking"). `git log` and the timeline become two views of the same history, legible across multiple tickets. Requires the Git CLI — see `onboarding-guide/references/prerequisites.md`.
- **`false`** (default) — no git activity from the plugin; each ticket's `timeline.jsonl` remains the only history.

This is about **local project tracking** of VinSAP's own working files, not the SAP-side ABAP transport/`$TMP` workflow (already handled in `abap-developer/references/transport-guidelines.md`) and not gCTS/git-enabled ABAP repos (the `adt_*_git_repo` tools) — those are separate concerns this plugin doesn't currently manage.

## Atlassian connector (mcp-atlassian)

This plugin ships `mcp-atlassian` (sooperset/mcp-atlassian, run via `uvx`) in `.mcp.json`, using **OAuth 2.0 BYOT (bring-your-own-token)** auth — the right mode for Atlassian Cloud, as opposed to `JIRA_PERSONAL_TOKEN`/`CONFLUENCE_PERSONAL_TOKEN` (Server/Data Center only, not usable against `*.atlassian.net`).

**Hardcoded Vincit-wide constants** (in `.mcp.json` directly, committed, not asked in `/vinsap:config`): `ATLASSIAN_OAUTH_CLOUD_ID` (`b09660f1-0129-41e7-90fc-442d84f44c00` — Vincit's Atlassian Cloud ID, found via `curl https://vincit.atlassian.net/_edge/tenant_info`, not a secret), `JIRA_PROJECTS_FILTER` (`ADSD`), `CONFLUENCE_SPACES_FILTER` (`ADSD`), `READ_ONLY_MODE` (`false`). Same for every engagement using this plugin. **`READ_ONLY_MODE: false` means write access to Jira/Confluence is enabled by default** — worth surfacing to the user the first time `/vinsap:config` runs. If a future engagement needs a different Atlassian site/project/space, update `.mcp.json` directly.

**Only `ATLASSIAN_OAUTH_ACCESS_TOKEN` is environment-variable-driven** — the actual secret, resolved from the *actual process environment* at launch, not from `.sdlc/config.json`:

1. Tell the user to set `ATLASSIAN_OAUTH_ACCESS_TOKEN` in their own shell profile (or a local `.env` the project's `.gitignore` excludes).
2. **Token refresh is the user's responsibility** — BYOT tokens aren't auto-refreshed by `mcp-atlassian`. If Jira/Confluence calls start failing with auth errors, the first thing to check is whether this token has expired and needs re-exporting, not a config bug.
3. **Never write `ATLASSIAN_OAUTH_ACCESS_TOKEN` into `.sdlc/config.json`, any ticket's `timeline.jsonl`, any output file, or anything this skill controls.** If the user pastes it into chat, don't echo it back or persist it anywhere — just confirm they've set it as an environment variable and move on. The *consuming* project may not already gitignore `.sdlc/`, unlike the plugin's own repo — add it if missing (belt-and-suspenders, even though no secret is meant to land there).

### Why `connectors.mcp-atlassian.atlassian_login` still exists

The bearer token authenticates as an **Atlassian Service Account** (`accountType: "app"`), not as the human running this session — confirmed live: `curl .../rest/api/3/myself` with this token returns `accountType: "app"`, a service identity, not a personal one. That means Jira's `assignee = currentUser()` / Confluence's `creator = currentUser()` resolve to the **service account**, not to the person actually using VinSAP — those queries would silently return nothing useful for "my tickets."

So: ask the user for their own Jira/Atlassian login (their email address, e.g. `firstname.lastname@vincit.fi`) and store it as `connectors.mcp-atlassian.atlassian_login` — not a secret, just an email, fine to persist. Every skill that needs to query "tickets assigned to me" or similar (`onboarding-guide`'s Jira-ticket pull, `scope-builder`, etc.) should use `assignee = "<atlassian_login>"` explicitly in JQL/CQL instead of `currentUser()`. If this field is unset when such a query is needed, ask for it then rather than guessing or silently using `currentUser()` (which would be wrong).

## SAP system discovery (not static)

The Vincit SAP MCP is **not** declared in this plugin's `.mcp.json` — each system's server (`vincit-abap-mcp-<SID>`) is connected globally, per system, outside the plugin (VS Code extension), before `/vinsap:config` even runs. Don't hardcode server names.

1. List currently-connected MCP servers matching the `vincit-abap-mcp-*` naming pattern (e.g. via the environment's MCP server listing).
2. For each one found, ask the user: which landscape role does it play (`DEV`/`QA`/`PRD` or a custom label) and which **mode** — `dev`, `quality`, or `production`? See `abap-developer/references/system-modes.md` for how mode gates behavior.
3. Record the mapping in `sap.systems`: `{"<ROLE>": {"mcp_server": "<actual connected server name>", "mode": "dev"|"quality"|"production"}}`.
4. If a system role's server isn't connected yet, tell the user to connect it (via the VS Code extension) and re-run `/vinsap:config` — don't invent a placeholder command to launch it.
5. Re-run this discovery whenever the user adds a new system, rather than assuming the mapping is static forever.
- `review.quick_model` / `review.deep_model` power `/vinsap:review` and `/vinsap:deep-review` respectively — see `code-reviewer/SKILL.md`.
- `handoff.destination` is only ever a *default*; `/vinsap:handoff` always confirms or lets the user override at runtime.
- `documentation.confluence_parent_id` defaults to `10682105864` — the Vincit ADSD space's documentation folder (`https://vincit.atlassian.net/wiki/spaces/ADSD/folder/10682105864`). `doc-generator` (and `session-recorder` for handoff) use this as the `parentId` when creating a new Confluence page, so published docs land in that folder by default rather than at the space root. Ask the user only if they want a different default; it's still overridable per publish.
