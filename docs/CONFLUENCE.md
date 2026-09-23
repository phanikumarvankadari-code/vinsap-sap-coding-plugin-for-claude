# VinSAP — ABAP/SAP SDLC Automation Plugin for Claude Code

*Source of truth: [GitHub repo](https://github.com/phanikumarvankadari-code/vinsap-sap-coding-plugin-for-claude). This page is a summary for the team — update it whenever the plugin changes meaningfully.*

## What it is

VinSAP is a Claude Code plugin that automates the SAP/ABAP development lifecycle end-to-end: gathering requirements, scoping, milestone planning, ABAP/Fiori development with auto-generated tests, code review, testing, and documentation — with a persistent audit trail so work can be handed off or resumed without losing context.

It connects to SAP through the **Vincit SAP MCP** (a VS Code extension, connected per system) and to Jira/Confluence through **mcp-atlassian** (run via `uvx`). A shipped hook mechanically enforces system-mode rules (dev/quality/production) and SQL guardrails on every SAP call, independent of what the AI model decides to do — this isn't just a written instruction, it's a script that blocks disallowed calls before they reach the server.

## Prerequisites

- **Claude Code CLI** — runs the plugin. [Quickstart](https://docs.claude.com/en/docs/claude-code/quickstart)
- **Node.js ≥ 18** — [Getting started](https://nodejs.org/en/learn/getting-started/introduction-to-nodejs)
- **Git CLI** *(optional — only if git tracking is turned on in config)* — [Pro Git book](https://git-scm.com/book/en/v2)
- **GitHub CLI (`gh`)** *(optional)* — [manual](https://cli.github.com/manual)
- **Playwright** — Fiori/UI5 e2e testing. [Writing tests](https://playwright.dev/docs/writing-tests)
- **Python 3** — runs the SAP MCP guardrail hook
- **draw.io** (desktop app + CLI) — default diagram tool
- **Vincit SAP MCP** (VS Code extension) — connect this *before* running `/vinsap:config`
- **uv/uvx** — launches the Jira/Confluence connector. [uv docs](https://docs.astral.sh/uv/)
- **mcp-atlassian** — Jira/Confluence connector, already declared in the plugin, launched via `uvx`. Site URLs, project/space filters, and read-only mode are hardcoded Vincit-wide constants in `.mcp.json`; only usernames come from `/vinsap:config`. **API tokens are set as environment variables on your machine, never stored in any config file.**
- **Atlassian API token** — there's no separate "MCP key"; `mcp-atlassian` authenticates as you with your personal Atlassian API token. Generate one at [id.atlassian.com → API tokens](https://id.atlassian.com/manage-profile/security/api-tokens), then set it as `JIRA_API_TOKEN` and `CONFLUENCE_API_TOKEN` in your shell profile (same token for both). Never share it or commit it anywhere.

## Installing

```
/plugin marketplace add phanikumarvankadari-code/vinsap-sap-coding-plugin-for-claude
/plugin install vinsap
```

You'll be asked to pick an install scope: **User** (every project, just you), **Project** (everyone in this repo), or **Local** (just you, this repo only).

## The pipeline

VinSAP works across **many tickets in one project**. Connectors/systems/preferences are set up **once**; everything else repeats **per ticket**.

**Once, project-level:**

1. **`/vinsap:onboard`** (alias `/vinsap:init`) — first run just checks prerequisites
2. **`/vinsap:config`** — connectors, SAP system modes, deployment mode, product scope, diagram tool, review model tiers, screenshot mode, git usage — shared by every ticket

**Per ticket, repeat for each one:**

3. **`/vinsap:onboard`** again — starts a new ticket: ticket ID, input source (Jira vs manual drop), creates `tickets/<TICKET-ID>/`, sets it active
4. **`/vinsap:analyze`** (aliases `/vinsap:scope`, `/vinsap:start`) — reads that ticket's inputs, asks clarifying questions, finalizes scope
5. **`/vinsap:milestones`** — breaks scope into milestones, tagged ABAP/Fiori/mixed
6. **`/vinsap:develop`** — generates code + tests per milestone, asks for package/transport selection
7. **`/vinsap:review`** — quick guideline check, runs in the background on a cheap model
8. **`/vinsap:test`** — runs tests, auto-fixes failures up to a retry cap
   *(steps 6–8 repeat per milestone until tests pass)*
9. **`/vinsap:deep-review`** — thorough, cross-milestone review, runs in the foreground on a stronger model, can ask clarifying questions
10. **`/vinsap:docs`** — generates Functional/Technical/Test documents from Vincit templates, optionally publishes to Confluence (new pages default into the [ADSD documentation folder](https://vincit.atlassian.net/wiki/spaces/ADSD/folder/10682105864))

Three commands work at any point, on the active ticket:

- **`/vinsap:status`** — plain progress view of the active ticket, or `/vinsap:status all` to list every ticket
- **`/vinsap:switch <TICKET-ID>`** — jump to a ticket already started, without re-onboarding it
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
      inputs/               - raw material: docs, emails, conversations, Jira exports
      outputs/              - generated scope, reviews, documents, handoff summaries
      state.json            - this ticket's current status
      timeline.jsonl          - this ticket's full history
    ADSD-1301/
      ...                    - a separate ticket in flight, same structure
```

## Status

Actively developed. Known open items: Vincit's real Functional/Technical Word templates still need to replace the placeholders, and the draw.io theme resources are still a placeholder waiting on Vincit's actual style guide.
