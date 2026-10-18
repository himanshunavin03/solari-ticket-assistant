# Repository instructions for Codex

Before starting work, read `PROJECT_STATUS.md`, the shared progress handoff for Codex and GitHub Copilot. Read the assignment at `case-study-1-support-ticket-similarity/case-study-brief.md`, the detailed user requirements in `docs/IMPLEMENTATION_REQUEST.md`, and relevant existing documentation, code, and data before editing. The preserved implementation request describes future application work; the current user request determines the authorized task scope.

Preserve supplied materials, existing content, and unrelated changes. Ignore `__MACOSX` metadata. Merge documentation updates without duplication or conflicting instructions.

## Shared continuity rules (Codex and Copilot)

- Before a meaningful task, record the intended change in `PROJECT_STATUS.md` and mark it **in progress**.
- Update the status immediately after each completed milestone, dependency change, important decision, test failure, or blocker. Checkpoint during long tasks instead of waiting for session end.
- Before ending a session, record the exact next action, unfinished edits, and any running processes, including stop/resume commands when applicable.
- Distinguish implemented, tested, and planned work. Never mark a check as passed unless it actually ran successfully. Record commands, results, failed commands, and actionable causes without excessive logs.
- Keep the handoff concise and factual. Link detailed documents instead of duplicating them. Maintain objective/scope, requirements/deadline, confirmed runtimes, chosen dependency versions and reasons, architecture trade-offs, completed paths, current work, checks, blockers/assumptions, prioritized next steps, exact resume commands, timestamp with timezone, relevant Git commit, and uncommitted work.
- Never include credentials, tokens, secret-bearing private URLs, or sensitive data.
- Do not automatically commit or push. Require explicit user authorization. Respect the implementation request's publication and submission restrictions.

## Resuming after interruption

1. Read repository instructions and `PROJECT_STATUS.md`.
2. Inspect `git status`, relevant diffs, and actual files, including untracked files, to verify the handoff. Treat status as guidance, not proof that code or tests are correct.
3. Identify the last verified milestone and resume the highest-priority unfinished task within the current user's scope. Do not repeat completed work unless verification reveals a reason.
4. Reconcile interrupted edits with the handoff before proceeding if they conflict.
