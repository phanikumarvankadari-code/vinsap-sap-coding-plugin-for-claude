# Prerequisites

| Tool | Why VinSAP needs it | Check | Install |
|---|---|---|---|
| Node.js | Runs Claude Code, Playwright, doc-generation tooling | `node --version` (>=18) | https://nodejs.org |
| Claude Code CLI | Runs the plugin itself | `claude --version` | https://docs.claude.com/claude-code |
| Git CLI *(only if `git.enabled` is on)* | Tracks `inputs/`, `outputs/`, `.sdlc/` for this project in version control | `git --version` | macOS: `brew install git` (or already present via `xcode-select --install`) · Windows: https://git-scm.com/download/win (or `winget install --id Git.Git`) |
| Playwright | Fiori/UI5 e2e test generation and execution | `npx playwright --version` | Same command on both OSes: `npm install -D playwright && npx playwright install` — docs: https://playwright.dev/docs/intro (Windows: run from PowerShell/cmd; macOS: run from Terminal — no OS-specific install steps beyond Node.js being present) |
| draw.io (desktop app + CLI) | Architecture/process diagrams via the `illustrator` skill (default `diagram_tool`) — the desktop app ships a headless CLI mode used to export `.drawio` files to SVG/PNG | `drawio --version` | macOS: `brew install --cask drawio`, or direct download from https://www.drawio.com/ · Windows: installer (`.exe`) from https://github.com/jgraph/drawio-desktop/releases (the `drawio` CLI binary ships inside the desktop app install on both OSes) |
| Atlassian MCP | Jira/Confluence connector | check with `/mcp` inside Claude Code — should list `atlassian` as connected | Already declared in this plugin's `.mcp.json` (remote server, no separate package install) — first use triggers a browser OAuth prompt to authorize your Atlassian account. Claude Code MCP docs: https://code.claude.com/docs/en/mcp |
| antigravity CLI (optional) | Only needed if configured as the diagram/image-generation tool instead of draw.io/mermaid | project-specific | ask the user for their install source — this is not a standard public tool |

## Flow

1. Run each check command.
2. For anything missing, show the install command and ask the user to run it (or confirm you may run it — installs are not silent/automatic).
3. Re-check after the user confirms install.
4. draw.io is only required if `/vinsap:config`'s `diagram_tool` is `drawio` (the default) — if the user sets it to `mermaid` instead, skip this check.
5. antigravity CLI is only required if `/vinsap:config` sets it as the diagram tool — skip checking it otherwise.
6. Git CLI is only required if `/vinsap:config`'s `git.enabled` is `true` — skip this check when git tracking is off.
