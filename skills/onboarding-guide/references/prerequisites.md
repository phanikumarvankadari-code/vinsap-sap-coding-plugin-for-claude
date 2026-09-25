# Prerequisites

| Tool | Why VinSAP needs it | Check | Install | Learn more |
|---|---|---|---|---|
| Node.js | Runs Claude Code, Playwright, doc-generation tooling | `node --version` (>=18) | https://nodejs.org/en/download | Getting-started guide: https://nodejs.org/en/learn/getting-started/introduction-to-nodejs |
| Claude Code CLI | Runs the plugin itself | `claude --version` | https://docs.claude.com/claude-code | Install + quickstart: https://docs.claude.com/en/docs/claude-code/quickstart · Full docs: https://docs.claude.com/en/docs/claude-code/overview |
| Git CLI *(only if `git.enabled` is on)* | Tracks `tickets/`, `.sdlc/` for this project in version control | `git --version` | macOS: `brew install git` (or already present via `xcode-select --install`) · Windows: https://git-scm.com/download/win (or `winget install --id Git.Git`) | Understanding git itself: https://git-scm.com/book/en/v2 (Pro Git, free) or https://docs.github.com/en/get-started/using-git/about-git |
| GitHub CLI (`gh`) *(optional)* | Handy if this project's VinSAP artifacts live in a GitHub repo (PRs, issues, gists) alongside plain `git` | `gh --version` | macOS: `brew install gh` · Windows: https://cli.github.com (installer) or `winget install --id GitHub.cli` | https://cli.github.com/manual |
| Playwright | Fiori/UI5 e2e test generation and execution | `npx playwright --version` | Same command on both OSes: `npm install -D playwright && npx playwright install` — docs: https://playwright.dev/docs/intro (Windows: run from PowerShell/cmd; macOS: run from Terminal — no OS-specific install steps beyond Node.js being present) | Writing/running tests: https://playwright.dev/docs/writing-tests · Test generator (`npx playwright codegen`): https://playwright.dev/docs/codegen |
| draw.io (desktop app + CLI) | Architecture/process diagrams via the `illustrator` skill (default `diagram_tool`) — the desktop app ships a headless CLI mode used to export `.drawio` files to SVG/PNG | `drawio --version` | macOS: `brew install --cask drawio`, or direct download from https://www.drawio.com/ · Windows: installer (`.exe`) from https://github.com/jgraph/drawio-desktop/releases (the `drawio` CLI binary ships inside the desktop app install on both OSes) | |
| `uv`/`uvx` | Runs `mcp-atlassian` (the Jira/Confluence MCP server, launched via `uvx mcp-atlassian`) | `uvx --version` | macOS: `brew install uv` · Windows: https://docs.astral.sh/uv/getting-started/installation/ (installer script or `winget install --id astral-sh.uv`) | https://docs.astral.sh/uv/ |
| `mcp-atlassian` connector | Jira/Confluence access | check with `/mcp` inside Claude Code — should list `mcp-atlassian` as connected | Already declared in this plugin's `.mcp.json`, launched via `uvx` — no separate package install. Uses OAuth 2.0 BYOT auth (Cloud-compatible); non-secret settings (cloud ID, project/space filters, read-only mode) are hardcoded in `.mcp.json`, nothing to set via `/vinsap:config`. Project: https://github.com/sooperset/mcp-atlassian | |
| Atlassian Service Account bearer token *(the actual secret behind `ATLASSIAN_OAUTH_ACCESS_TOKEN`)* | There is no separate "MCP key" — `mcp-atlassian` authenticates using a bearer token issued to an **Atlassian Service Account** (`accountType: "app"`, org-admin-managed via Atlassian Administration → Service Accounts). This is **not** the same as a personal Atlassian API token (basic auth) and **not** a personal OAuth 3LO user token — it's a service-account-scoped access token | check it's set: `echo $ATLASSIAN_OAUTH_ACCESS_TOKEN`; verify it's live: `curl -H "Authorization: Bearer $ATLASSIAN_OAUTH_ACCESS_TOKEN" "https://api.atlassian.com/ex/jira/<cloud_id>/rest/api/3/myself"` (expect `"accountType":"app"` in the response) | Obtain it from Vincit's shared 1Password vault — not something you self-generate. See "Configuring the token" below for OS-specific setup. **Never** paste it into chat, a config file, or anything committed. **Token refresh is your responsibility** — BYOT tokens are not auto-refreshed; re-export when it expires or is rotated | https://support.atlassian.com/organization-administration/docs/manage-service-accounts/ |
| antigravity CLI (optional) | Only needed if configured as the diagram/image-generation tool instead of draw.io/mermaid | project-specific | ask the user for their install source — this is not a standard public tool | |

## Configuring the Atlassian Service Account token

`ATLASSIAN_OAUTH_ACCESS_TOKEN` must exist in the environment **before** Claude Code (this session) launches — setting it in a different terminal window after the fact won't be picked up. Set it permanently in your shell profile, then start a fresh Claude Code session.

**macOS / Linux (zsh, the default shell):**
```bash
echo 'export ATLASSIAN_OAUTH_ACCESS_TOKEN="<your token>"' >> ~/.zshrc
source ~/.zshrc
```
(If using bash instead of zsh, use `~/.bashrc` or `~/.bash_profile` instead of `~/.zshrc`.)

**Windows (PowerShell):**
```powershell
[System.Environment]::SetEnvironmentVariable('ATLASSIAN_OAUTH_ACCESS_TOKEN', '<your token>', 'User')
```
This persists it for your user account across sessions (equivalent to editing System Properties → Environment Variables by hand). Close and reopen PowerShell/Claude Code afterward for it to take effect. Alternatively, add it to your PowerShell `$PROFILE` script with `$env:ATLASSIAN_OAUTH_ACCESS_TOKEN = "<your token>"` if you only want it set for PowerShell sessions specifically, not system-wide.

**Windows (Command Prompt):**
```cmd
setx ATLASSIAN_OAUTH_ACCESS_TOKEN "<your token>"
```
Same persistence as the PowerShell method above; also requires a new terminal window to take effect.

In every case: verify with the `echo`/check command in the table above, then confirm `/mcp` inside Claude Code lists `mcp-atlassian` as connected.

## Flow

1. Run each check command.
2. For anything missing, show the install command and ask the user to run it (or confirm you may run it — installs are not silent/automatic).
3. Re-check after the user confirms install.
4. draw.io is only required if `/vinsap:config`'s `diagram_tool` is `drawio` (the default) — if the user sets it to `mermaid` instead, skip this check.
5. antigravity CLI is only required if `/vinsap:config` sets it as the diagram tool — skip checking it otherwise.
6. Git CLI is only required if `/vinsap:config`'s `git.enabled` is `true` — skip this check when git tracking is off.
7. GitHub CLI is always optional — never block onboarding on it, just mention it's available if the user's remote is GitHub.
