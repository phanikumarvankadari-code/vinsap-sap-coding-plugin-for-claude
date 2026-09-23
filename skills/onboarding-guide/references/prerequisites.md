# Prerequisites

| Tool | Why VinSAP needs it | Check | Install | Learn more |
|---|---|---|---|---|
| Node.js | Runs Claude Code, Playwright, doc-generation tooling | `node --version` (>=18) | https://nodejs.org | Getting-started guide: https://nodejs.org/en/learn/getting-started/introduction-to-nodejs |
| Claude Code CLI | Runs the plugin itself | `claude --version` | https://docs.claude.com/claude-code | Install + quickstart: https://docs.claude.com/en/docs/claude-code/quickstart · Full docs: https://docs.claude.com/en/docs/claude-code/overview |
| Git CLI *(only if `git.enabled` is on)* | Tracks `tickets/`, `.sdlc/` for this project in version control | `git --version` | macOS: `brew install git` (or already present via `xcode-select --install`) · Windows: https://git-scm.com/download/win (or `winget install --id Git.Git`) | Understanding git itself: https://git-scm.com/book/en/v2 (Pro Git, free) or https://docs.github.com/en/get-started/using-git/about-git |
| GitHub CLI (`gh`) *(optional)* | Handy if this project's VinSAP artifacts live in a GitHub repo (PRs, issues, gists) alongside plain `git` | `gh --version` | macOS: `brew install gh` · Windows: https://cli.github.com (installer) or `winget install --id GitHub.cli` | https://cli.github.com/manual |
| Playwright | Fiori/UI5 e2e test generation and execution | `npx playwright --version` | Same command on both OSes: `npm install -D playwright && npx playwright install` — docs: https://playwright.dev/docs/intro (Windows: run from PowerShell/cmd; macOS: run from Terminal — no OS-specific install steps beyond Node.js being present) | Writing/running tests: https://playwright.dev/docs/writing-tests · Test generator (`npx playwright codegen`): https://playwright.dev/docs/codegen |
| draw.io (desktop app + CLI) | Architecture/process diagrams via the `illustrator` skill (default `diagram_tool`) — the desktop app ships a headless CLI mode used to export `.drawio` files to SVG/PNG | `drawio --version` | macOS: `brew install --cask drawio`, or direct download from https://www.drawio.com/ · Windows: installer (`.exe`) from https://github.com/jgraph/drawio-desktop/releases (the `drawio` CLI binary ships inside the desktop app install on both OSes) | |
| `uv`/`uvx` | Runs `mcp-atlassian` (the Jira/Confluence MCP server, launched via `uvx mcp-atlassian`) | `uvx --version` | macOS: `brew install uv` · Windows: https://docs.astral.sh/uv/getting-started/installation/ (installer script or `winget install --id astral-sh.uv`) | https://docs.astral.sh/uv/ |
| `mcp-atlassian` connector | Jira/Confluence access | check with `/mcp` inside Claude Code — should list `mcp-atlassian` as connected | Already declared in this plugin's `.mcp.json`, launched via `uvx` — no separate package install. Non-secret settings come from `/vinsap:config`; **`JIRA_API_TOKEN`/`CONFLUENCE_API_TOKEN` must be set as real environment variables by the user, never stored in any config file.** Project: https://github.com/sooperset/mcp-atlassian | |
| Atlassian API token *(the actual secret behind `JIRA_API_TOKEN`/`CONFLUENCE_API_TOKEN`)* | There is no separate "MCP key" — `mcp-atlassian` authenticates as you, using your personal Atlassian API token (username + token, basic auth) | check it's set: `echo $JIRA_API_TOKEN` (or `$CONFLUENCE_API_TOKEN` — same token works for both, generated once) | Generate one at https://id.atlassian.com/manage-profile/security/api-tokens → "Create API token" → copy it immediately (shown once) → `export JIRA_API_TOKEN="<token>"` and `export CONFLUENCE_API_TOKEN="<token>"` in your shell profile (`~/.zshrc`/`~/.bashrc`) — never paste it into chat, a config file, or anything committed | https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/ |
| antigravity CLI (optional) | Only needed if configured as the diagram/image-generation tool instead of draw.io/mermaid | project-specific | ask the user for their install source — this is not a standard public tool | |

## Flow

1. Run each check command.
2. For anything missing, show the install command and ask the user to run it (or confirm you may run it — installs are not silent/automatic).
3. Re-check after the user confirms install.
4. draw.io is only required if `/vinsap:config`'s `diagram_tool` is `drawio` (the default) — if the user sets it to `mermaid` instead, skip this check.
5. antigravity CLI is only required if `/vinsap:config` sets it as the diagram tool — skip checking it otherwise.
6. Git CLI is only required if `/vinsap:config`'s `git.enabled` is `true` — skip this check when git tracking is off.
7. GitHub CLI is always optional — never block onboarding on it, just mention it's available if the user's remote is GitHub.
