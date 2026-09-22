---
description: Set up connectors, product/module scope, prerequisites, and preferences for this engagement.
---

Invoke the `config-manager` skill to create or update `.sdlc/config.json`:

- **Connectors** — Atlassian MCP (Jira project key(s), Confluence space), Vincit SAP MCP `vincit-abap-mcp-<SID>` (a VS Code extension hosting the MCP server — system landscape DEV/QA/PRD, client, package defaults).
- **Deployment mode** — `mcp` (push/activate/transport directly through the SAP MCP connector) or `manual` (generate code + instructions, user applies via ADT themselves).
- **Products/modules** — solution-area codes in scope: `FIN`, `SLS`, `SRC`, `MFG`, `SCM`, `HCM`, `AST`, `SVC`, `CORE`.
- **Prerequisites** — confirm/re-check Node.js, Claude Code CLI, Playwright, antigravity CLI; offer install guidance for anything missing.
- **Diagram tool** — default `draw.io`, mermaid as lightweight fallback.
- **Review model tiers** — `review.quick_model` (cheap/fast, e.g. haiku) and `review.deep_model` (smarter, e.g. opus/sonnet).
- **Screenshot mode** — `documentation.screenshot_mode`: `auto` (Playwright captures in background) or `manual` (user supplies screenshots).
- **Handoff destination default** — `confluence`, `jira-comment`, or `file` (user is still asked to confirm/override each time `/vinsap:handoff` runs).
- **Git usage** — `git.enabled`: whether this project's VinSAP artifacts (`inputs/`, `outputs/`, `.sdlc/`) get tracked/committed in git as the pipeline progresses. Requires the Git CLI if enabled.

Show the user what is already configured vs. still missing before asking for new input. Append an entry to `.sdlc/timeline.jsonl` on any change.
