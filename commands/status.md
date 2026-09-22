---
description: Show current stage and per-milestone progress as a plain CLI kanban-style view.
---

Read `.sdlc/state.json`. No dedicated skill — format directly.

Output format:

```
VinSAP — <ticket/project id> Status

Stage Progress
✅ onboard
✅ config
✅ analyze/scope
⏳ milestones

Milestones
✅ M1: <title>   [develop ✓] [test ✓]
⏳ M2: <title>   [develop ✓] [test ⏳]
⬜ M3: <title>   [pending]

Progress: <block-bar> NN% (X/Y complete)

Last updated: <timestamp>
```

Icons: ✅ done, ⏳ in progress, ⬜ pending, ❌ failed/blocked. Compute the progress bar from milestones done/total. If `.sdlc/state.json` does not exist yet, tell the user to run `/vinsap:onboard` first.
