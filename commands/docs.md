---
description: Interactively generate a Functional, Technical, or Test document from the Vincit template, and optionally publish to Confluence.
---

Invoke the `doc-generator` skill.

1. Ask the user which document to create: **Functional**, **Technical**, or **Test**.
2. Present the proposed section list for that doc type (see `SKILL.md`); let the user pick, add, or remove sections.
3. Load the matching Vincit template from `references/templates/` (`Functional Document.docx`, `Technical Document.docx`, or `test-doc-template.md`).
4. Fill sections conversationally — pull what can be derived from `tickets/<active>/outputs/scope.md`, `tickets/<active>/state.json`, milestone/code output, and test results; ask the user for anything that can't be derived. Follow `references/writing-style.md` (simple English, bullet points 15–25 words each over long paragraphs, prefer illustrations). Generate diagrams via the `illustrator` skill (draw.io themed, or mermaid fallback) per `illustrator/references/illustration-guidelines.md`.
5. Flag the drafted document for **UX review** before finalizing.
6. Save the filled document to `tickets/<active>/outputs/docs/`.
7. Ask whether to publish to **Confluence** (via the `mcp-atlassian` MCP connector) — create a new page or update an existing one, attaching the generated file.
8. For the Test document, follow `documentation.screenshot_mode` from `.sdlc/config.json`: `auto` (Playwright captures screenshots in the background) or `manual` (tell the user exactly what to capture and where to drop it, then embed).
9. Append an entry to `tickets/<active>/timeline.jsonl`.
