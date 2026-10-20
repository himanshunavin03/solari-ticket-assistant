# Project status

Updated: 2026-10-19 21:49:41 -0600 (America/Edmonton).

## Objective, scope and deadline

Solari Ticket Assistant: reduce repeated investigation and inconsistent support answers by retrieving original historical resolution notes for agent review. Angular/TypeScript, FastAPI, TF-IDF, pinned CPU MiniLM, RRF, original JSON and in-memory indexes. Every note has applicability unverified. No generated fixes, live ingestion, persisted feedback, new models/frameworks or database. Brief: `case-study-1-support-ticket-similarity/case-study-brief.md`; current design: `SOLUTION_DESIGN.md`. Original implementation request remains in the working repository, excluded from submission.

Deadline Tuesday October20,2026 EOD; recipient timezone unspecified. No commit, push, upload or submission authorized/performed by this task. Confirm delivery requirements/timezone manually.

## Actual Git and current task

Starting/current HEAD: `58718664920bf90f80baeca357938219bec2152e`; initial working tree clean. Earlier revisions and their uncommitted-state descriptions are historical. Current **uncommitted/unstaged finalization**: README/design/runbook/evaluation documentation, current evaluator baseline option/snapshot/metric helper, sample API report/script/tests, explicit packager/tests, validation/content docs and this handoff. Application retrieval source, model/dependency pins/lockfile, original supplied material and all earlier tracked JSON evaluation artifacts unchanged (preservation diff passed).

**Complete:** all four supplied examples verified in three modes, focused docs, self-contained explicit package, backend/frontend/browser checks, baseline/current result reproduction, fresh-directory ZIP checks and final handoff. No unfinished implementation or pending tool process. All previous owned dev servers were stopped for tests; no listeners on8000/8001/4200 at final check. Next action is manual Launchpad verification/PDF review, not additional features.

## Implemented decisions and files

- Existing `informal-precedent-v6` remains unchanged: retain short clauses/negation/identifiers; query-only generic polite-framing removal retains objects; global semantic/clause .65/.45, corroborated identifier .60, keyword .25/.50 and narrow short-query conjunctive route unchanged. API separates unverified historical precedent, weak related metadata, no relevant history and service errors. More than8clauses abstains; embeddings truncate256wordpieces. Dataset40tickets, strict fields/unique IDs, non-destructive duplicate-content inspection.
- README now has complete short Windows Quick Start, explicit extra Node requirement, backend-only `/docs` fallback, limitations/not handled and requested AI-assistance disclosure. Design722words, approximately1–2pages: wasted investigation/inconsistent answers, justified assumptions, actual diagram/policy/trade-offs, no invented concurrency/growth/latency or arbitrary vector-store threshold.
- `scripts/verify_samples.py`, `evaluation/SAMPLE_TICKET_RESULTS.md` and `sample-ticket-results.json`:12real HTTP requests, unchanged inputs, returned IDs/component scores, original notes and unverified labels. No retrieval correction was necessary. Four new API regression cases.
- `scripts/package_submission.py`:66explicit members, standard-library-only packager, deterministic ZIP/CRC/SHA verification, optional real PDF at `docs/SOLUTION_DESIGN.pdf`. No directory sweeping. All tests included. Session instructions/status/copilot, prompts/notes, unused experiments, Git/metadata/environments/dependencies/weights/caches/logs/builds/generated artifacts excluded. Original repository history/files retained.
- `evaluation/metrics.py` preserves the tested legacy denominator function without shipping unused experiment imports. `baseline_v5/` supports reproduction without Git: only import/root relocation; a test reverses these adaptations and verifies frozen original hashes. `review_informal.py --policy current|baseline` refuses existing output paths. Legacy report guards/results retained only for shipped tests/provenance. Every shipped project import and Markdown link resolves; excluded-file mentions in package tests are intentional exclusion assertions.
- Submission-facing validation/content docs: `docs/SUBMISSION_VALIDATION.md`, `docs/SUBMISSION_CONTENTS.md`. Historical `docs/VALIDATION.md` and superseded experiments stay in repository, excluded from ZIP. Original informal input remains exactly subject `i charged twice`, description `i charged twice please validate this transaction`.

## Actual runtimes and dependency reasons

Windows Python3.11.9 (`.venv`) and3.10.11 (`.venv310`), pip25.0.1; project-local Node22.23.2/npm10.9.8; Git2.50.1.windows.1. Current shell PowerShell7.6.7; extracted preflight also passed Windows PowerShell5.1.26100.9711. System runtimes unchanged. Original Launchpad Python3.10.0/pip21.2.3/Node20.10.0/npm10.2.3/Git2.43.0.windows.1 **not executed**. Node20.10.0 cannot build current Angular; checksum-verified additional local runtime route remains explicit.

Pins unchanged: FastAPI0.115.8, Uvicorn0.34.0, Pydantic2.10.6, NumPy1.26.4, scikit-learn1.6.1, Sentence Transformers3.4.1, Transformers4.48.3, Torch2.6.0 (CPU2.6.0+cpu), HTTPX0.28.1, pytest8.3.4. Tested CPU/API stack compatible with3.10.11; resolved3.10/3.11 manifests retained. Angular20.3.34, CLI/build20.3.40, TypeScript5.9.2, RxJS7.8.2, tslib2.8.1, Playwright1.56.1. Model `sentence-transformers/all-MiniLM-L6-v2@1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, normalized384dimensions/four CPU threads. Static JSON/in-memory architecture avoids infrastructure; persistence/updates/filtering/memory/measured latency would guide future storage decisions.

## Actual checks and results

- Targeted sample/evaluation10passed; targeted packaging/evaluation6passed before final full checks. No test was removed/skipped to pass packaging.
- Full backend:83passed/0failed/0skipped on3.11.9(22.62s),83passed/0failed/0skipped on3.10.11(22.97s). One nonfatal Starlette/AnyIO warning each. Actual pinned model required.
- Frontend typecheck/build passed;177.49kB initial/49.47kB estimated transfer. Repository Playwright:9passed/0failed/0skipped(38.5s), including actual Swagger Try-it-out search, chart/billing/429, exact informal query, misleading examples, short contradiction, degradation, errors/no-history/stale/mobile.
- Supplied examples all3modes:12direct API requests passed. Hybrid NT-1 metadata onlyT-1001/T-1004 (no forced reset/report notes), NT-2T-1201 original notes, NT-3T-1303 original notes, NT-4metadata onlyT-1105. Keyword chart abstains (lexical.431559<.50); semantic/hybrid chart passes. Full scores/inputs in sample report.
- Initial66-file ZIP extracted to fresh Temp `solari-submission-check-l0go_1as`: byte equality/CRC/exclusions/Markdown links/project-import audit passed. Reused original Python venv/packages/local Node/Chromium; **copied modelcache into extractedroot**, fresh npmci installed411packages/zero audit findings. Not a clean installation. Imports explicitly confirmed from extracted backend, not original source directory.
- Extracted preflight passed under PowerShell7.6.7 and Windows5.1.26100.9711 (offline real embedding, all capabilities/40tickets, pip check/npm ls, typecheck/build/cleanup). Extracted backend83passed(22.41s); browser9passed(37.3s);12direct and12proxied sample requests passed; docsHTTP200/Swagger execution passed.
- Extracted current AND baseline evaluator runs completed. Asserted every non-timing relevance/error metric and per-case expected/displayed/related ID/outcome matched retained reports on all4splits/3modes. No performance claim: timing overlaps dev activity.
- Final regenerated ZIP re-extracted separately into Temp `solari-submission-final-1opi81uf`: all66members CRC/source bytes/exclusions/links passed; only4Markdown files differ from the fully browser-verified extraction. All executable/test/data files identical. Final extracted backend83passed/0failed/0skipped(21.36s), one dependency warning, with reused Python and copied modelcache.
- Final ZIP repeat generation SHA256 identical: `21B9FD5FE8F352BDA3E3FEF788610B0BF295933BFB3D8865898E27686FFEFE04`;160877bytes. Paths `artifacts/solari-ticket-assistant.zip`, `artifacts/manifest.json`, `artifacts/included-files.txt`. CRC test Done testing. Compileall, original-source/data/JSON preservation diff and whitespace check passed.
- One rg audit initially failed because Windows passed literal scripts/*.py; corrected to -g '*.py' and reran. No unresolved application/test/build failure or model/browser skip. Color/prebundling/deprecation notices nonfatal. Earlier test-first policy failures are historical, not relabeled as passing checks.

## Measured limitations and manual blockers

All evaluation sets are exposed AI-authored synthetic regressions, not independent accuracy evidence. Informal hybrid Recall@3/MRR.625→.875; abstentions3/8→1/8; notes on negatives0/10→0/10. Keyword recall.25→.375. Informal429 still missesT-1702; explicit429 passes. Older short login case still includes an irrelevant extraT-1004. Semantic/lexical overlap cannot prove mechanism or negation equivalence. No further policy tuning during finalization.

No PDF found in project/parent/supplied attachments. Add the genuine final reviewed document at `docs/SOLUTION_DESIGN.pdf`, then regenerate ZIP if required. No fake PDF created. Cannot compare an unavailable separate PDF: manually align unverified applicability, sample outcomes, v6 policy/measurements and runtime caveats with Markdown design. Original Launchpad exact patch/network/execution policies remain unverified. Independent labels, other devices/browsers, production access/security/load remain future/manual work. Confirm deadline timezone before manual delivery.

## Exact resume / next action

Read AGENTS/status, inspect git status/diffs/actual files. Implementation/finalization are complete; do not repeat work unless verification reveals a reason. Full fresh setup and troubleshooting: README and `docs/LAUNCHPAD_RUNBOOK.md`. Test command uses an existing environment here; Launchpad creates `.venv` as documented.

```powershell
git status --short
$env:Path = (Join-Path (Get-Location) '.runtime/node-v22.23.2-win-x64') + ';' + $env:Path
$env:SOLARI_OFFLINE = '1'
./scripts/preflight.ps1
./.venv/Scripts/python.exe -m pytest -q
# Backend terminal, root:
./.venv/Scripts/python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --no-access-log
# Separate frontend terminal: set same local Node PATH, then:
Push-Location frontend
npm start
# Verify supplied examples once API is running, from root:
./.venv/Scripts/python.exe -m scripts.verify_samples
# After adding genuine final PDF if required:
./.venv/Scripts/python.exe -m scripts.package_submission
./.venv/Scripts/python.exe -m zipfile -t artifacts/solari-ticket-assistant.zip
Get-Content artifacts/included-files.txt
```

No process requires stopping/resuming now. Ignored temporary extraction environments/caches and original dev environments are preserved outside ZIP. Previous detailed handoff backup: `.cache/project-status-before-final-handoff.md`; historical committed state remains in Git. No automatic publication/submission.
Application startup in progress: verified clean HEAD beec725 and free ports. Starting existing servers and checking readiness. Initial combined background-launch command was rejected by tool policy before execution; using separate terminal sessions instead.

Startup complete 2026-10-19 21:55:43 -06:00 (America/Edmonton): HEAD beec725aa2a0af8937300a4b9cf8c375272c568d, existing environments preserved. Backend terminal session52558 (Uvicorn67436) running offline at8000; frontend terminal session37169 started with Windows PowerShell5.1, project-local Node PATH, Push-Location frontend and npm.cmd start. Frontend HTTP200; direct and proxied API ready/all3capabilities/40tickets verified. Initial background command policy rejection and pwsh frontend AccessDenied resolved by separate sessions and explicit powershell.exe. No source changes, commits or publication. Servers intentionally remain running; next action open http://127.0.0.1:4200. Stop via Ctrl+C in each terminal/session; inspect port owners before stopping processes by PID. Previous stopped-server status above is historical.
