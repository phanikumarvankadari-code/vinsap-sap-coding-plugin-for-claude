---
name: config-manager
description: Use for /vinsap:config — creates/updates .sdlc/config.json with connector setup, product scope, prerequisites, diagram tool, review model tiers, screenshot mode, and git usage.
---

# Config Manager

Follow `../_shared/context-contract.md` for read/write conventions.

## Fields to manage in `.sdlc/config.json`

`sap` is **top-level**, a sibling of `connectors` — not nested inside it. This is the authoritative shape: `hooks/guard_sap_mcp.py::find_system_mode()` reads `config["sap"]["systems"]` directly, so it must match exactly.

```json
{
  "connectors": {
    "mcp-atlassian": {
      "jira_username": "",
      "confluence_username": ""
    }
  },
  "sap": {
    "systems": {
      "DEV": { "mcp_server": "vincit-abap-mcp-S4H", "mode": "dev" }
    },
    "default_package": "$TMP",
    "deployment_mode": "mcp"
  },
  "products": ["FIN", "SLS", "SRC", "MFG", "SCM", "HCM", "AST", "SVC", "CORE"],
  "diagram_tool": "drawio",
  "review": { "quick_model": "haiku", "deep_model": "opus" },
  "documentation": { "screenshot_mode": "auto" },
  "handoff": { "destination": "file" },
  "git": { "enabled": false }
}
```

## Steps

1. Read the existing `.sdlc/config.json` if present; show the user what's already set vs. what's still missing.
2. Ask for missing values conversationally, grouped by section (connectors, products, prerequisites, deployment mode, diagram tool, model tiers, screenshot mode, git usage, handoff default) — don't ask everything as one giant form.
3. Re-run the prerequisite check from `onboarding-guide/references/prerequisites.md` if the user wants to change tooling.
4. Write the merged config back to `.sdlc/config.json`.
5. Append a `.sdlc/timeline.jsonl` entry summarizing what changed.

## Deployment mode

Ask the user to choose `sap.deployment_mode`:

- **`mcp`** (default) — `abap-developer` pushes code, creates/activates transports, and runs the linter directly through the `vincit-abap-mcp-<SID>` connector (the Vincit SAP MCP VS Code extension). Fully automated per `abap-developer/references/transport-guidelines.md`.
- **`manual`** — `abap-developer` still generates the code and runs it through the same guardrails/style checks locally, but does **not** push anything through the MCP connector. Instead it writes the finished object source to `outputs/develop/<milestone>/` with an instruction sheet (object name, package, transport request to use) for the user to apply themselves via ADT (Eclipse/VS Code ABAP Development Tools).

`sap.deployment_mode` is read by `abap-developer` on every `/vinsap:develop` run — surface which mode is active before generating code so the user isn't surprised by whether something landed in the system or just on disk.

`sap.default_package` here is only a **suggested default** — it does not silently decide the package or transport for a milestone. When `deployment_mode` is `mcp`, `abap-developer` asks the user for the package (defaulting to `sap.default_package`) and, via `adt_list_transports`, offers a selection of the currently open/modifiable transports on the target system to reuse — or lets the user choose to create a new one — rather than assuming. See `abap-developer/references/transport-guidelines.md` §2/§2a.

## Git usage

Ask the user whether this project should track its VinSAP artifacts (`inputs/`, `outputs/`, `.sdlc/`) in git — set `git.enabled` accordingly:

- **`true`** — every `.sdlc/timeline.jsonl` append gets a matching git commit, 1:1 (see `_shared/context-contract.md` → "Git tracking"). `git log` and the timeline become two views of the same history. Requires the Git CLI — see `onboarding-guide/references/prerequisites.md`.
- **`false`** (default) — no git activity from the plugin; `.sdlc/timeline.jsonl` remains the only history.

This is about **local project tracking** of VinSAP's own working files, not the SAP-side ABAP transport/`$TMP` workflow (already handled in `abap-developer/references/transport-guidelines.md`) and not gCTS/git-enabled ABAP repos (the `adt_*_git_repo` tools) — those are separate concerns this plugin doesn't currently manage.

## Atlassian connector (mcp-atlassian)

This plugin ships `mcp-atlassian` (sooperset/mcp-atlassian, run via `uvx`) in `.mcp.json`.

**Hardcoded Vincit-wide constants** (in `.mcp.json` directly, committed, not asked in `/vinsap:config`): `JIRA_URL` (`https://vincit.atlassian.net`), `JIRA_PROJECTS_FILTER` (`ADSD`), `CONFLUENCE_URL` (`https://vincit.atlassian.net/wiki`), `CONFLUENCE_SPACES_FILTER` (`ADSD`), `READ_ONLY_MODE` (`false`). These are the same for every engagement using this plugin — not secrets, safe to commit. **`READ_ONLY_MODE: false` means write access to Jira/Confluence is enabled by default for everyone using this plugin** — worth surfacing to the user the first time `/vinsap:config` runs, since it's a real capability, not just bookkeeping. If a future engagement needs a different Jira project, Atlassian site, or read-only posture, update `.mcp.json` directly rather than trying to make these configurable per-project.

**Only the two usernames stay environment-variable-driven**, resolved from the *actual process environment* at launch, not from `.sdlc/config.json`:

1. Ask the user for the remaining **non-secret** fields — Jira username, Confluence username — and write those into `connectors.mcp-atlassian` in `.sdlc/config.json` as shown above.
2. Tell the user to set the matching environment variables in their own shell profile (or a local `.env` the project's `.gitignore` excludes) so `.mcp.json`'s `${VAR}` placeholders resolve at launch:
   - `VINSAP_JIRA_USERNAME`, `VINSAP_CONFLUENCE_USERNAME`
   - `JIRA_API_TOKEN`, `CONFLUENCE_API_TOKEN` — **the two actual secrets**
3. **Never write `JIRA_API_TOKEN` or `CONFLUENCE_API_TOKEN` into `.sdlc/config.json`, `.sdlc/timeline.jsonl`, any output file, or anything this skill controls.** If the user pastes a token into chat, don't echo it back or persist it anywhere — just confirm they've set it as an environment variable and move on. This applies even though `.sdlc/` is already gitignored in the plugin's own repo — the *consuming* project may not have that protection unless `/vinsap:onboard`/`/vinsap:config` also adds it (see step 4).
4. If the consuming project doesn't already gitignore `.sdlc/`, add it — belt-and-suspenders against accidentally committing anything sensitive that ends up there.

## SAP system discovery (not static)

The Vincit SAP MCP is **not** declared in this plugin's `.mcp.json` — each system's server (`vincit-abap-mcp-<SID>`) is connected globally, per system, outside the plugin (VS Code extension), before `/vinsap:config` even runs. Don't hardcode server names.

1. List currently-connected MCP servers matching the `vincit-abap-mcp-*` naming pattern (e.g. via the environment's MCP server listing).
2. For each one found, ask the user: which landscape role does it play (`DEV`/`QA`/`PRD` or a custom label) and which **mode** — `dev`, `quality`, or `production`? See `abap-developer/references/system-modes.md` for how mode gates behavior.
3. Record the mapping in `sap.systems`: `{"<ROLE>": {"mcp_server": "<actual connected server name>", "mode": "dev"|"quality"|"production"}}`.
4. If a system role's server isn't connected yet, tell the user to connect it (via the VS Code extension) and re-run `/vinsap:config` — don't invent a placeholder command to launch it.
5. Re-run this discovery whenever the user adds a new system, rather than assuming the mapping is static forever.
- `review.quick_model` / `review.deep_model` power `/vinsap:review` and `/vinsap:deep-review` respectively — see `code-reviewer/SKILL.md`.
- `handoff.destination` is only ever a *default*; `/vinsap:handoff` always confirms or lets the user override at runtime.
