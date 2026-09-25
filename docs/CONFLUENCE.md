# VinSAP — ABAP/SAP SDLC Automation Plugin for Claude Code

*Source of truth: [GitHub repo](https://github.com/phanikumarvankadari-code/vinsap-sap-coding-plugin-for-claude). This page is a summary for the team — update it whenever the plugin changes meaningfully.*

## What it is

VinSAP is a Claude Code plugin that automates the SAP/ABAP development lifecycle end-to-end: gathering requirements, scoping, milestone planning, ABAP/Fiori development with auto-generated tests, code review, testing, and documentation — with a persistent audit trail so work can be handed off or resumed without losing context.

It connects to SAP through the **Vincit SAP MCP** (a VS Code extension, connected per system) and to Jira/Confluence through **mcp-atlassian** (run via `uvx`). A shipped hook mechanically enforces system-mode rules (dev/quality/production) and SQL guardrails on every SAP call, independent of what the AI model decides to do — this isn't just a written instruction, it's a script that blocks disallowed calls before they reach the server.

## Prerequisites

- **Claude Code CLI** — runs the plugin. [Quickstart](https://docs.claude.com/en/docs/claude-code/quickstart)
- **Node.js ≥ 18** — [Download](https://nodejs.org/en/download) · [Getting started](https://nodejs.org/en/learn/getting-started/introduction-to-nodejs)
- **Git CLI** *(optional — only if git tracking is turned on in config)* — [Pro Git book](https://git-scm.com/book/en/v2)
- **GitHub CLI (`gh`)** *(optional)* — [manual](https://cli.github.com/manual)
- **Playwright** — Fiori/UI5 e2e testing. [Writing tests](https://playwright.dev/docs/writing-tests)
- **Python 3** — runs the SAP MCP guardrail hook
- **draw.io** (desktop app + CLI) — default diagram tool
- **Vincit SAP MCP** (VS Code extension) — connect this *before* running `/vinsap:config`
- **uv/uvx** — launches the Jira/Confluence connector. [uv docs](https://docs.astral.sh/uv/)
- **mcp-atlassian** — Jira/Confluence connector, already declared in the plugin, launched via `uvx`. Site URLs, project/space filters, and read-only mode are hardcoded Vincit-wide constants in `.mcp.json`; `/vinsap:config` only asks for your Jira/Atlassian login email (`atlassian_login`), needed because the bearer token authenticates as a shared service account, not you — "assigned to me" queries use this explicitly instead of `currentUser()`. **The bearer token itself is set as an environment variable on your machine, never stored in any config file.**
- **Atlassian Service Account bearer token** — there's no separate "MCP key"; `mcp-atlassian` authenticates via `ATLASSIAN_OAUTH_ACCESS_TOKEN`, a bearer token issued to an org-managed Atlassian Service Account (not a personal API token, not a personal OAuth login). Get it from 1Password: vault "AI driven SAP development", item "ai-driven-sap-RW API token", then set it as an env var per-OS (macOS: `~/.zshrc`; Windows: PowerShell `SetEnvironmentVariable` or `setx`) before launching Claude Code. Never share it or commit it anywhere.

## Installing

```
/plugin marketplace add phanikumarvankadari-code/vinsap-sap-coding-plugin-for-claude
/plugin install vinsap
```

You'll be asked to pick an install scope: **User** (every project, just you), **Project** (everyone in this repo), or **Local** (just you, this repo only).

## The pipeline

VinSAP works across **many tickets in one project**. Connectors/systems/preferences are set up **once**; everything else repeats **per ticket**.

**Once, project-level:**

1. **`/vinsap:config`** — connectors, SAP system modes, deployment mode, product scope, diagram tool, review model tiers, screenshot mode, git usage — shared by every ticket
2. **`/vinsap:intent`** (alias `/vinsap:init`) — first run just checks prerequisites

**Per ticket, repeat for each one:**

3. **`/vinsap:intent`** again — starts a new ticket: ticket ID, input source (Jira vs manual drop), creates `tickets/<TICKET-ID>/`, writes `intent.md`, sets it active
4. **`/vinsap:spec`** (aliases `/vinsap:scope`, `/vinsap:start`) — reads intent + that ticket's inputs, asks clarifying questions plus the ticket's functional/solution area(s) (used later to pre-fill package search), finalizes `outputs/spec.md`
5. **`/vinsap:plan`** — breaks the spec into milestones, tagged ABAP/Fiori/mixed, writes `outputs/plan.md`
6. **`/vinsap:build`** — generates code + tests per milestone, asks for package/transport selection
7. **`/vinsap:review`** — quick guideline check, runs in the background on a cheap model
8. **`/vinsap:test`** — runs tests, auto-fixes failures up to a retry cap
   *(steps 6–8 repeat per milestone until tests pass)*
9. **`/vinsap:deep-review`** *(optional)* — thorough, cross-milestone review, runs in the foreground on a stronger model, can ask clarifying questions. Not a hard gate — `/vinsap:ship` decides whether it's required, asked once per ticket (Always/Ask each time/Skip)
10. **`/vinsap:ship`** — deploy-readiness checklist, applies the deep-review preference, writes `outputs/ship.md`. Doesn't release/deploy anything itself. Cadence depends on milestone type: **ABAP/mixed** — per milestone, right after `test` passes, transport staged incrementally. **Fiori/UI5** — once, after every Fiori milestone in the ticket is built/tested, since app deployment isn't incremental
11. **`/vinsap:docs`** — generates Functional/Technical/Test documents from Vincit templates, optionally publishes to Confluence (new pages default into the [ADSD documentation folder](https://vincit.atlassian.net/wiki/spaces/ADSD/folder/10682105864)); every publish/update also comments the page URL on the ticket's Jira issue

Three commands work at any point, on the active ticket:

- **`/vinsap:status`** — plain progress view of the active ticket, or `/vinsap:status all` to list every ticket
- **`/vinsap:switch <TICKET-ID>`** — jump to a ticket already started, without re-running `/vinsap:intent`

Pre-rename names still work as legacy aliases: `/vinsap:onboard` → `/vinsap:intent`, `/vinsap:scope` → `/vinsap:spec`, `/vinsap:milestones` → `/vinsap:plan`, `/vinsap:develop` → `/vinsap:build`. Run `/vinsap:help` any time for the full command reference with examples, in-session.
- **`/vinsap:handoff`** — narrative summary of everything that happened on the active ticket, always saved into that ticket's `outputs/handoff/`, and optionally also published to Jira or Confluence

## System modes and guardrails

Every connected SAP system is tagged with a mode, enforced both by the server itself and by a hook in the plugin:

| Mode | Allowed |
|---|---|
| **dev** | Full: create, update, read, run |
| **quality** | View, compare, run tests — no code creation |
| **production** | Read-only code inspection only — no run, no write, no data access, ever |

Additional guardrails baked in: no DB mutations without explicit bypass, no unindexed scans on heavy tables, a row cap on selections, a syntax/ATC check before any save, and no way to release a transport through the plugin at all — that stays a manual, outside-the-plugin step.

## Where things live

Shared config once at the project root; everything else per ticket:

```
your-project/
  .sdlc/
    config.json           - shared across all tickets: connectors, systems/modes, model tiers
    active_ticket.json     - which ticket is currently active
  tickets/
    ADSD-1204/
      intent.md             - captured by /vinsap:intent
      inputs/               - raw material: docs, emails, conversations, Jira exports
      outputs/              - spec.md, plan.md, build/, reviews, ship.md, docs, handoff summaries
      state.json            - this ticket's current status
      timeline.jsonl          - this ticket's full history
    ADSD-1301/
      ...                    - a separate ticket in flight, same structure
```

## Status

Actively developed. Known open items: Vincit's real Functional/Technical Word templates still need to replace the placeholders, and the draw.io theme resources are still a placeholder waiting on Vincit's actual style guide.
