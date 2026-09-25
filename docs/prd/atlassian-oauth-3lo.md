# PRD (future) — Atlassian OAuth 2.0 3LO for mcp-atlassian

Status: **not started**. Captured from discussion on 2026-09-25. Current auth (live): OAuth 2.0 BYOT with a bearer token belonging to an Atlassian Service Account — see `skills/config-manager/SKILL.md` § "Atlassian connector (mcp-atlassian)".

## Problem with current setup (BYOT)

- Token authenticates as an **Atlassian Service Account** (`accountType: "app"`, confirmed live via `/rest/api/3/myself`), not the individual VinSAP user.
- `currentUser()` in JQL/CQL resolves to the service account, not the person using VinSAP — worked around today via `connectors.mcp-atlassian.atlassian_login` (user's own email, used explicitly in `assignee = "<atlassian_login>"` queries instead of `currentUser()`).
- Shared credential across the whole team — no per-user audit trail on who did what.

## Proposal: switch to full OAuth 2.0 (3LO)

Interactive browser login flow, run once per user via `uvx mcp-atlassian --oauth-setup`. User logs in as themselves at the real Atlassian login screen, consents, token + refresh token cached in the OS keychain (via `mcp-atlassian`'s `keyring` dependency — Keychain on macOS, Credential Manager on Windows, Secret Service on Linux). Auto-refreshed after that, no manual re-export like BYOT needs today.

Benefits:
- `currentUser()` works correctly — drops the `atlassian_login` workaround entirely.
- Each dev authenticates as themselves — real audit trail, real permission boundary (can't act beyond what that person's own Jira/Confluence account can do).
- No shared static bearer token to rotate/leak.

## What it requires

1. **Register an Atlassian OAuth 2.0 (3LO) app** — one-time, needs an org admin. developer.atlassian.com/console/myapps → OAuth 2.0 (3LO) → scopes (`read:jira-work`, `write:jira-work`, `read:jira-user`, `read:confluence-content.all`, `write:confluence-content`, `offline_access`) → callback URL `http://localhost:8080/callback`. Produces a Client ID + Client Secret — Vincit-wide, not personal, but still a secret.
2. **`.mcp.json` changes** — replace `ATLASSIAN_OAUTH_ACCESS_TOKEN` with `ATLASSIAN_OAUTH_CLIENT_ID`, `ATLASSIAN_OAUTH_CLIENT_SECRET`, `ATLASSIAN_OAUTH_REDIRECT_URI`, `ATLASSIAN_OAUTH_SCOPE`. `ATLASSIAN_OAUTH_CLOUD_ID`, `JIRA_PROJECTS_FILTER`, `CONFLUENCE_SPACES_FILTER`, `READ_ONLY_MODE` stay unchanged — project/space scoping is orthogonal to auth mode.

   ```json
   {
     "mcpServers": {
       "mcp-atlassian": {
         "command": "uvx",
         "args": ["mcp-atlassian"],
         "env": {
           "ATLASSIAN_OAUTH_CLIENT_ID": "${ATLASSIAN_OAUTH_CLIENT_ID}",
           "ATLASSIAN_OAUTH_CLIENT_SECRET": "${ATLASSIAN_OAUTH_CLIENT_SECRET}",
           "ATLASSIAN_OAUTH_REDIRECT_URI": "http://localhost:8080/callback",
           "ATLASSIAN_OAUTH_SCOPE": "read:jira-work write:jira-work read:jira-user read:confluence-content.all write:confluence-content offline_access",
           "ATLASSIAN_OAUTH_CLOUD_ID": "b09660f1-0129-41e7-90fc-442d84f44c00",
           "JIRA_PROJECTS_FILTER": "ADSD",
           "CONFLUENCE_SPACES_FILTER": "ADSD",
           "READ_ONLY_MODE": "false"
         }
       }
     }
   }
   ```

3. **Drop** `connectors.mcp-atlassian.atlassian_login` from `.sdlc/config.json` and the corresponding logic in `config-manager`/`onboarding-guide` skills — no longer needed once `currentUser()` works.
4. **Docs rewrite** — `config-manager/SKILL.md`, `onboarding-guide/references/prerequisites.md`, README, `docs/CONFLUENCE.md`: replace "get bearer token from 1Password, export it" with "run `uvx mcp-atlassian --oauth-setup` once, log in with your own Vincit Atlassian account."

## Cross-tenant access — why OAuth (BYOT or 3LO) is safer than the old classic API token

The prior config (basic auth, personal API token) was tied to the **account**, not a site — if that account also has access to a client's separate Jira Cloud instance, the same token authenticates there too; `mcp-atlassian`'s `JIRA_URL` was just convention, not an enforced boundary.

OAuth (BYOT today, 3LO in this proposal) is scoped to a specific **cloud/site** — `ATLASSIAN_OAUTH_CLOUD_ID` targets Vincit's site explicitly; 3LO's consent flow (`getAccessibleResources`) only authorizes sites the app was granted against. This closed a real hole, not just a BYOT-vs-3LO identity nuance — worth stating explicitly in `config-manager/SKILL.md` when this ships.

## Secret storage for Client ID/Secret (new requirement this introduces)

Unlike the access/refresh token (which `keyring` stores automatically, no config needed), the **Client ID/Secret is a new Vincit-wide secret** that needs secure distribution to every dev's machine before `--oauth-setup` can run.

Recommended: **1Password**, reusing the existing vault (`AI driven SAP development`) that already holds the BYOT bearer token (item `ai-driven-sap-RW API token`). Add a new item, e.g. `mcp-atlassian-oauth-app`, fields `client_id` / `client_secret`.

Retrieval at setup time (no plaintext export, no custom popup code — 1Password's own app-integration unlock prompt (Touch ID/Windows Hello/master password) fires automatically on `op read`):

```bash
export ATLASSIAN_OAUTH_CLIENT_ID=$(op read "op://AI driven SAP development/mcp-atlassian-oauth-app/client_id")
export ATLASSIAN_OAUTH_CLIENT_SECRET=$(op read "op://AI driven SAP development/mcp-atlassian-oauth-app/client_secret")
uvx mcp-atlassian --oauth-setup
```

Prerequisites this adds: **1Password CLI (`op`)** installed + signed in, **1Password desktop app with CLI integration enabled** (Settings → Developer → "Integrate with 1Password CLI").

Alternative (skip 1Password, use OS keychain directly) — viable but weaker for a team-shared secret (no central rotation/audit, and Windows `cmdkey` can't be read back via CLI, would need PowerShell `SecretManagement` module instead):

```bash
# macOS
security add-generic-password -a "$USER" -s "vinsap-atlassian-oauth-client-id" -w "<client-id>"
security add-generic-password -a "$USER" -s "vinsap-atlassian-oauth-client-secret" -w "<client-secret>"
security find-generic-password -s "vinsap-atlassian-oauth-client-secret" -w   # read back
```

```powershell
# Windows
cmdkey /generic:vinsap-atlassian-oauth-client-id /user:vinsap /pass:<client-id>
cmdkey /generic:vinsap-atlassian-oauth-client-secret /user:vinsap /pass:<client-secret>
```

**Decision: not yet made** — 1Password is the recommended default given it's already in use, but not committed until this PRD is picked up.

## Slack ask for infra (drafted, not yet sent)

> Need an Atlassian OAuth 2.0 (3LO) app registered at developer.atlassian.com/console/myapps — gives us a Client ID + Client Secret, callback URL `http://localhost:8080/callback`, scoped to Jira/Confluence read+write. Can you set this up?

## Related, separate idea (also deferred): bundling the SAP MCP VS Code extension install

`/vinsap:onboard`'s prerequisite check already flags whether the Vincit SAP MCP VS Code extension is installed. Could go further: run `code --install-extension <extension-id>` automatically if missing (requires the `code` CLI on PATH and the extension's marketplace ID — not yet known). Note: installing the extension doesn't finish SAP MCP setup by itself — signing in to the SAP system is still a manual step regardless.

## Not yet decided / open questions

- Exact OAuth scope list `mcp-atlassian` actually needs (check its docs before registering the app).
- Whether to keep BYOT as a fallback path for CI/headless contexts where an interactive browser login isn't possible.
- Whether 1Password or OS keychain is the final answer for Client ID/Secret storage.
- SAP MCP VS Code extension's actual marketplace ID (needed for the auto-install idea).
