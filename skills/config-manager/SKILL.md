---
name: config-manager
description: Use for /vinsap:config — creates/updates .sdlc/config.json with connector setup, product scope, prerequisites, diagram tool, review model tiers, and screenshot mode.
---

# Config Manager

Follow `../_shared/context-contract.md` for read/write conventions.

## Fields to manage in `.sdlc/config.json`

```json
{
  "connectors": {
    "atlassian": { "site": "", "jira_project_keys": [], "confluence_space": "" },
    "sap": {
      "systems": {
        "DEV": { "mcp_server": "vincit-abap-mcp-S4H", "mode": "dev" }
      },
      "default_package": "$TMP",
      "deployment_mode": "mcp"
    }
  },
  "products": ["FIN", "SLS", "SRC", "MFG", "SCM", "HCM", "AST", "SVC", "CORE"],
  "diagram_tool": "drawio",
  "review": { "quick_model": "haiku", "deep_model": "opus" },
  "documentation": { "screenshot_mode": "auto" },
  "handoff": { "destination": "file" }
}
```

## Steps

1. Read the existing `.sdlc/config.json` if present; show the user what's already set vs. what's still missing.
2. Ask for missing values conversationally, grouped by section (connectors, products, prerequisites, deployment mode, diagram tool, model tiers, screenshot mode, handoff default) — don't ask everything as one giant form.
3. Re-run the prerequisite check from `onboarding-guide/references/prerequisites.md` if the user wants to change tooling.
4. Write the merged config back to `.sdlc/config.json`.
5. Append a `.sdlc/timeline.jsonl` entry summarizing what changed.

## Deployment mode

Ask the user to choose `sap.deployment_mode`:

- **`mcp`** (default) — `abap-developer` pushes code, creates/activates transports, and runs the linter directly through the `vincit-abap-mcp-<SID>` connector (the Vincit SAP MCP VS Code extension). Fully automated per `abap-developer/references/transport-guidelines.md`.
- **`manual`** — `abap-developer` still generates the code and runs it through the same guardrails/style checks locally, but does **not** push anything through the MCP connector. Instead it writes the finished object source to `outputs/develop/<milestone>/` with an instruction sheet (object name, package, transport request to use) for the user to apply themselves via ADT (Eclipse/VS Code ABAP Development Tools).

`sap.deployment_mode` is read by `abap-developer` on every `/vinsap:develop` run — surface which mode is active before generating code so the user isn't surprised by whether something landed in the system or just on disk.

## SAP system discovery (not static)

The Vincit SAP MCP is **not** declared in this plugin's `.mcp.json` — each system's server (`vincit-abap-mcp-<SID>`) is connected globally, per system, outside the plugin (VS Code extension), before `/vinsap:config` even runs. Don't hardcode server names.

1. List currently-connected MCP servers matching the `vincit-abap-mcp-*` naming pattern (e.g. via the environment's MCP server listing).
2. For each one found, ask the user: which landscape role does it play (`DEV`/`QA`/`PRD` or a custom label) and which **mode** — `dev`, `quality`, or `production`? See `abap-developer/references/system-modes.md` for how mode gates behavior.
3. Record the mapping in `sap.systems`: `{"<ROLE>": {"mcp_server": "<actual connected server name>", "mode": "dev"|"quality"|"production"}}`.
4. If a system role's server isn't connected yet, tell the user to connect it (via the VS Code extension) and re-run `/vinsap:config` — don't invent a placeholder command to launch it.
5. Re-run this discovery whenever the user adds a new system, rather than assuming the mapping is static forever.
- `review.quick_model` / `review.deep_model` power `/vinsap:review` and `/vinsap:deep-review` respectively — see `code-reviewer/SKILL.md`.
- `handoff.destination` is only ever a *default*; `/vinsap:handoff` always confirms or lets the user override at runtime.
