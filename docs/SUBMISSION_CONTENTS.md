# Submission contents

The packager uses this explicit file allowlist; it does not recursively sweep repository folders. `artifacts/included-files.txt` and `artifacts/manifest.json` list actual members and source SHA256 values after generation. ZIP membership, CRCs and source hashes are verified. Stable entry order/timestamps make unchanged-source builds reproducible.

Current/baseline evaluation snapshots and case files support reproduction. Original results and legacy refusal scripts remain only where shipped tests need them; metric tests use the small metrics module instead of importing obsolete experiment runners. All tests are shipped. Historical experiments and internal documents remain in the working repository.

Excluded: AGENTS.md, PROJECT_STATUS.md, .github/copilot-instructions.md, internal prompts/session notes, unused experiments, .git, Mac metadata, bytecode, environments, node_modules, runtimes, model caches/weights, logs, builds and generated archives/manifests. No secrets are collected by directory discovery.

Optional final PDF: `docs/SOLUTION_DESIGN.pdf`. It is **not currently supplied**. Add the reviewed real document there and rerun packaging; the script reports its absence rather than creating a substitute.

## Required files

```text
README.md
SOLUTION_DESIGN.md
requirements.txt
requirements-resolved.txt
requirements-py310-resolved.txt
pytest.ini
.gitignore
backend/__init__.py
backend/app.py
backend/evidence.py
backend/retrieval.py
frontend/package.json
frontend/package-lock.json
frontend/angular.json
frontend/tsconfig.json
frontend/proxy.json
frontend/playwright.config.ts
frontend/src/main.ts
frontend/src/index.html
frontend/src/app.html
frontend/src/styles.css
frontend/e2e/smoke.spec.ts
tests/test_api.py
tests/test_evaluation.py
tests/test_evidence.py
tests/test_focused_corrections.py
tests/test_informal.py
tests/test_integration.py
tests/test_retrieval.py
tests/test_packaging.py
scripts/__init__.py
scripts/bootstrap-node.ps1
scripts/download_model.py
scripts/prefetch-model.ps1
scripts/preflight.py
scripts/preflight.ps1
scripts/inspect_data.py
scripts/package_submission.py
scripts/verify_samples.py
docs/LAUNCHPAD_RUNBOOK.md
docs/SUBMISSION_VALIDATION.md
docs/SUBMISSION_CONTENTS.md
evaluation/__init__.py
evaluation/README.md
evaluation/SAMPLE_TICKET_RESULTS.md
evaluation/sample-ticket-results.json
evaluation/review_informal.py
evaluation/informal-cases.json
evaluation/informal-freeze.json
evaluation/informal-baseline-results.json
evaluation/informal-revised-results.json
evaluation/baseline_v5/__init__.py
evaluation/baseline_v5/evidence.py
evaluation/baseline_v5/retrieval.py
evaluation/metrics.py
evaluation/cases.json
evaluation/release-cases.json
evaluation/precedent-cases.json
evaluation/data-quality-report.json
evaluation/run.py
evaluation/results.json
evaluation/review_precedents.py
evaluation/precedent-regression-results.json
case-study-1-support-ticket-similarity/case-study-brief.md
case-study-1-support-ticket-similarity/starter_kit/data/tickets.json
case-study-1-support-ticket-similarity/starter_kit/data/new_tickets_example.json
```
