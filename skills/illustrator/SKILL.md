---
name: illustrator
description: Use whenever a diagram is needed (architecture, process flow, milestone dependency) for doc-generator or milestone-planner. Generates draw.io themed diagrams, or mermaid for lightweight inline cases.
---

# Illustrator

Follow `../_shared/context-contract.md` for read/write conventions.

## Choosing the tool

- **draw.io** (default, per `.sdlc/config.json` `diagram_tool`) — for architecture diagrams and anything going into a Functional/Technical document. Use `references/drawio-theme/` for consistent styling.
- **mermaid** — lightweight fallback for inline diagrams in markdown output (e.g. a quick milestone flow shown in chat or in `outputs/scope.md`) where a full draw.io file is overkill. See `references/mermaid-patterns.md`.

## Steps

1. Determine what the diagram needs to show (architecture, process flow As-Is/To-Be, milestone dependency) and which document/context it's for.
2. Check `.sdlc/config.json` for the configured tool; default to draw.io for anything destined for a formal document.
3. Apply `references/illustration-guidelines.md` — simple, single-concept, consistently styled, fully labeled.
4. For draw.io: build the `.drawio` file using `references/drawio-theme/` styling, then export via the headless `drawio` CLI (ships with the desktop app — see `onboarding-guide/references/prerequisites.md`), e.g. `drawio -x -f svg -o output.svg diagram.drawio`, in the format the destination document needs (embed-ready image or the native `.drawio` file, per what `doc-generator` requests). If `drawio` isn't installed, tell the user and fall back to mermaid rather than failing silently.
5. For mermaid: use a pattern from `references/mermaid-patterns.md`, adapt to the specific content.
6. Return the diagram to the calling skill (`doc-generator` or `milestone-planner`) — this skill does not decide where the diagram is used, only how it's built.

## Notes

- Never invent visual conventions ad hoc if `illustration-guidelines.md` or `drawio-theme/` already defines one — consistency across a project's diagrams matters more than cleverness in any single diagram.
