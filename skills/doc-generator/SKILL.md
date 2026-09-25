---
name: doc-generator
description: Use for /vinsap:docs — interactively generates a Functional, Technical, or Test document from the Vincit template, filling sections conversationally and optionally publishing to Confluence.
---

# Doc Generator

Follow `../_shared/context-contract.md` for read/write conventions.

## Steps

1. Ask the user which document to create: **Functional**, **Technical**, or **Test**.
2. Present the section list below for that doc type; let the user pick, add, or remove sections.
3. Load the matching template from `references/templates/`:
   - Functional → `Functional Document.docx`
   - Technical → `Technical Document.docx`
   - Test → `test-doc-template.md`
4. Fill each section:
   - Pull what's derivable from `tickets/<active>/outputs/scope.md`, `tickets/<active>/state.json`, milestone/code output (`abap-developer`/`fiori-developer` results), and test results (`test-runner` output, `tickets/<active>/outputs/reviews/`).
   - Ask the user for anything that can't be derived — same interview style as `scope-builder`.
   - Follow `references/writing-style.md`: simple English, bullet points over long paragraphs, 15–25 words per bullet, prefer a diagram over a wall of text where one says it faster.
   - Request diagrams from the `illustrator` skill wherever a section calls for one (architecture, process flow).
5. Flag the drafted document for **UX review** before finalizing — surface it to the user explicitly as a review checkpoint, don't silently mark it done.
6. Save the filled document to `tickets/<active>/outputs/docs/`.
7. Ask whether to publish to **Confluence** via the `mcp-atlassian` MCP connector:
   - **Create a new page** — defaults to `documentation.confluence_parent_id` from `.sdlc/config.json` (the ADSD space's documentation folder) as the parent, so it nests there rather than at the space root. Confirm with the user, don't silently assume a different parent.
   - **Update an existing page** (search/select) instead, if one already exists for this ticket/doc.
   - Attach the generated file to that page.
   - **Every time a Confluence page is created or updated this way, add a comment on the ticket's Jira issue with that page's URL** (via `mcp-atlassian`) — creation gets a new comment, an update gets a fresh comment too (don't rely on the user finding an old link buried in history). Skip this if the ticket has no linked Jira issue (manually-dropped-input tickets).
8. For the Test document, follow `.sdlc/config.json` → `documentation.screenshot_mode`:
   - `auto` — Playwright captures screenshots in the background (subagent, fire-and-forget) and they're embedded automatically.
   - `manual` — tell the user exactly which screens/actions to capture and where to drop them (`tickets/<active>/inputs/screenshots/`), then embed once supplied.
9. Append a `tickets/<active>/timeline.jsonl` entry.

## Functional Document sections

Document Control · Overview/Business Purpose · Business Requirement · Scope (In/Out) · Actors/Roles/Stakeholders · Current Process (As-Is — only if enhancing an existing process, skip otherwise) · Proposed Process (To-Be, diagram) · Functional Specifications per Milestone · Acceptance Criteria · Assumptions & Constraints · Open Questions/Risks (carried from `scope-builder` gaps) · Glossary · Change Log.

## Technical Document sections

Document Control · Overview/Purpose · System Landscape · Architecture Diagram · Object Inventory (`ZMASTER` packages) · Data Model/DDIC · Interfaces · Implementation Details per Milestone · Authorization/Security (including any guardrail bypasses taken — check `tickets/<active>/timeline.jsonl` for `guardrail_bypass` entries) · Transport Details · Dependencies · Performance Considerations · Known Limitations · Test Summary (reference the Test Doc, don't duplicate) · Change Log.

## Test Document sections

Test Strategy/Approach · Test Coverage (ABAP Unit/QUnit/Playwright mapped per milestone) · Test Results Summary (from `tickets/<active>/state.json` / `timeline.jsonl`) · Test Case Details (Given/When/Then, matches the AAA pattern in `abap-developer/references/unittest-guidelines.md`) · UI Screenshots · Known Issues/Failures · Regression Notes.
