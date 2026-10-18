# GitHub Copilot repository instructions

Read `PROJECT_STATUS.md` before starting work. It is the shared source of progress information for GitHub Copilot and Codex; do not create a separate handoff.

Read and follow the **Shared continuity rules (Codex and Copilot)** and **Resuming after interruption** sections of root `AGENTS.md`. These apply equally to Copilot: record intended meaningful work as in progress before editing, checkpoint after milestones/decisions/dependency changes/failures/blockers and during long tasks, and leave exact next actions, unfinished edits, and process information before ending. Distinguish implemented/tested/planned work; only claim checks that ran successfully; capture actionable failures concisely. Keep the shared status factual, timestamped with timezone, and free of secrets. Do not commit or push without explicit user authorization.

Before editing, read `case-study-1-support-ticket-similarity/case-study-brief.md`, `docs/IMPLEMENTATION_REQUEST.md`, and relevant existing documentation, code, and data. The current user request determines task scope; the preserved implementation request does not itself authorize starting application implementation. Preserve original supplied files and unrelated work; ignore `__MACOSX` metadata.

On resume, verify the handoff against Git status, diffs, and actual files (including untracked files). Reconcile conflicting interrupted edits, find the last verified milestone, and resume the highest-priority unfinished task. Do not repeat completed work without a verification-based reason.
