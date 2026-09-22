# Prerequisites

| Tool | Why VinSAP needs it | Check | Install |
|---|---|---|---|
| Node.js | Runs Claude Code, Playwright, doc-generation tooling | `node --version` (>=18) | https://nodejs.org |
| Claude Code CLI | Runs the plugin itself | `claude --version` | https://docs.claude.com/claude-code |
| Playwright | Fiori/UI5 e2e test generation and execution | `npx playwright --version` | `npm install -D playwright && npx playwright install` |
| antigravity CLI (optional) | Only needed if configured as the diagram/image-generation tool instead of draw.io/mermaid | project-specific | ask the user for their install source — this is not a standard public tool |

## Flow

1. Run each check command.
2. For anything missing, show the install command and ask the user to run it (or confirm you may run it — installs are not silent/automatic).
3. Re-check after the user confirms install.
4. antigravity CLI is only required if `/vinsap:config` sets it as the diagram tool — skip checking it otherwise.
