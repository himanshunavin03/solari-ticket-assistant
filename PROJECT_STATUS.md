# Project status

Last updated: 2026-10-17 22:59 -06:00 (America/Edmonton).

## Objective, scope and deadline

Solari Analytics Support Ticket Similarity Assistant: Angular agent UI and FastAPI service retrieve original historical resolutions from the 40 supplied synthetic tickets. Scope includes keyword/semantic/hybrid retrieval, evidence gating, tests, measured evaluation, documentation and local submission packaging. No generated answers, training, database, paid API, or production deployment.

Deadline: **Tuesday, October 20, 2026, EOD; timezone unspecified**. Confirm recipient timezone before manual delivery. Assignment budget is approximately 3–4 focused hours, with a 4–5 hour stop expectation. Sources: `case-study-1-support-ticket-similarity/case-study-brief.md`, `docs/IMPLEMENTATION_REQUEST.md`; decisions and trade-offs: `SOLUTION_DESIGN.md`.

## Current task and last verified milestone

Completed: all authorized local implementation, tests, evaluation, documentation and packaging. No unfinished edits. All four implementation milestones are implemented and tested locally. Next exact action for the user: follow README setup and checks in the original target sandbox; confirm the recipient's deadline timezone before manual submission. No commit, push, upload or submission authorized or performed.

Verified Git baseline: `5cc8bf4dc7bf08e9e093d090b13a7a1bd7644138` (`add changes`). Earlier status claiming only README was tracked is obsolete: the user committed the continuity files and supplied materials before authorizing implementation. Current uncommitted work: modified root README/status; new `.gitignore`, backend, frontend/lockfile, tests, evaluation artifacts, scripts, design and supporting docs. Existing AGENTS/Copilot instructions remain unchanged. All original supplied files are unchanged against HEAD (`git diff --exit-code HEAD -- case-study-1-support-ticket-similarity` passed). No application listeners on 8000/4200 after Playwright cleanup; no task-owned background servers/downloads remain.

## Confirmed environment and chosen dependencies

Windows development host: Python 3.11.9, venv pip 25.0.1 (system pip 24.0), Node 22.23.2, npm 10.9.8, Git 2.50.1.windows.1. Host CPU: Intel64 Family 6 Model 186 Stepping 2; 20 logical CPUs; Torch uses four threads. Project-local Node bootstrap downloaded and SHA256-verified Node 22.23.2 successfully; system installation untouched. `.venv` is project-local; no Conda.

User-stated target: Python 3.10.0 / pip 21.2.3 / Node 20.10.0 / npm 10.2.3 / Git 2.43.0.windows.1. **Original target sandbox not executed.** Official Angular compatibility requires newer Node; README bootstraps a local compatible runtime. PyPI direct-package requirements accept Python 3.10, but cross-version installation/runtime remains manual verification. `requirements-resolved.txt` is the actual Python 3.11 environment snapshot, not a tested Python 3.10 lock.

Exact direct Python pins/reasons in `requirements.txt` and README: FastAPI 0.115.8, Uvicorn 0.34.0, Pydantic 2.10.6, NumPy 1.26.4, scikit-learn 1.6.1, Sentence Transformers 3.4.1, Transformers 4.48.3, Torch 2.6.0 (runtime 2.6.0+cpu), HTTPX 0.28.1, pytest 8.3.4. Chosen Python-3.10-compatible API/retrieval/testing stack; exact resolved transitives recorded separately.

Angular runtime/compiler 20.3.34, CLI/build 20.3.40, TypeScript 5.9.2, RxJS 7.8.2, tslib 2.8.1, Playwright 1.56.1. Supported Angular line, compatible host/local Node, patched toolchain with clean npm audit. `frontend/package-lock.json` generated and verified by npm ci, ready for user-controlled version control.

## Architecture and completed paths

- `backend/retrieval.py`: strict startup data validation/unique IDs; subject+description TF-IDF; CPU normalized MiniLM; safe non-pickle embedding cache keyed by dataset/model/revision/preprocessing; stable ties; positive-evidence RRF; explicit candidate abstention. Pinned model: `sentence-transformers/all-MiniLM-L6-v2@1110a243fdf4706b3f48f1d95db1a4f5529b4d41`.
- `backend/app.py`: typed search/readiness/examples API; restricted dev CORS; safe errors; sync inference handlers; keyword-only degradation is explicit and hybrid/semantic fail with 503 when unavailable.
- `frontend/src/`: accessible responsive form/examples/results, original resolutions/descriptions/tags, optional evidence details, errors/loading/no-match/degradation, abort+sequence stale-response protection.
- `tests/`, `frontend/e2e/`: offline/API/cache tests, real pretrained model integration, real UI flow and focused simulated failure/concurrency states.
- `evaluation/`: fixed development/held-out AI-assisted relevance labels/rationales, development diagnostics, initial/final development results, held-out results and reproducible metric script.
- `README.md`, `SOLUTION_DESIGN.md`, `docs/DEMO_GUIDE.md`, `docs/AI_ASSISTANCE.md`, `docs/VALIDATION.md`: setup, decisions, honest limits, demonstration, assistance and actual validation record.
- `scripts/`: checksum-verified Node bootstrap, model download/prefetch, reproducible allowlisted ZIP with CRC/content verification. Archive/manifest in ignored `artifacts/`.

Trade-offs: JSON/in-memory static indexes require restart for updates; no production permissions/isolation. MiniLM truncates at 256 wordpieces. RRF avoids adding incomparable raw scores. Final gates keyword 0.25 / semantic 0.70 were selected using development evidence **before held-out execution**; cosine/fusion values are not probabilities. Hybrid OR gate inherits lexical false acceptances. See design/evaluation docs rather than expanding scope here.

## Checks actually completed and observed failures

Detailed commands/failure causes: `docs/VALIDATION.md`.

- Final `.venv/Scripts/python -m pytest -q` with `SOLARI_OFFLINE=1`: **33 passed**, one nonfatal Starlette/AnyIO deprecation warning. Separate offline run: 32 passed/1 deselected; integration run: 1 passed/32 deselected. Real model offline encoding verified (1,384), history (40,384).
- `pip install -r requirements.txt`, `pip check`: satisfied pins, no broken requirements. Actual resolved packages saved. Initial large-wheel stall recovered through official checksum-verified curl download; temporary missing-package/collection failures resolved.
- Frontend `npm ci`, `npm run typecheck`, `npm run build`, `npm audit --audit-level=low`, `npm ls --depth=0`: passed; zero audit findings, 175.87 kB raw initial bundle. Initial 20.3.0 vulnerabilities and old-peer ERESOLVE resolved by patching and fresh lock generation. Cleanup rejection handled through reversible generated backups, not force/legacy peers.
- `npm run test:e2e`: **4 passed**, Chromium 141.0.7390.37/build 1194. Known-match/no-match, original evidence/reset, mobile width, invalid input/backend failure, stale responses and simulated degraded health verified. Desktop/mobile screenshots in artifacts visually inspected. First run had a failed Snowflake abstention assumption; actual retrieval error documented and UI no-match test uses a pre-existing development negative instead. Gates unchanged.
- Development and held-out evaluation ran for all three modes. Held-out final 60 warm samples/mode: keyword median/p95 0.302/0.348 ms; semantic 9.018/14.243 ms; hybrid 9.540/13.088 ms. No throughput/concurrent SLA claim.
- Held-out positives: keyword/hybrid Recall@3/MRR 1.0, P@3 .3333; semantic Recall@3/MRR .875, P@3 .2917. No-match correct rejections keyword/hybrid 2/4, semantic 3/4. Hybrid did not beat keyword on held-out quality. Full per-case results in `evaluation/results.json`.
- `git diff --check` passed (only configured line-ending conversion warnings). Final ZIP packaging verified 49 files, required membership, CRCs and source SHA256 equality; final archive includes this handoff and validation documentation. No source-only checks represented as application tests.
- Two unchanged-source packaging runs produced identical ZIP SHA256, confirming deterministic output. Final status refresh is included by regenerating the archive. Final process inspection found no Python/Node processes; `Get-Process` returned exit 1 for an empty match list, an idle-state diagnostic rather than an application failure.

## Known limitations, blockers and remaining work

No unresolved blocker to local implementation. **Known quality failures:** keyword/hybrid accept supplied Snowflake as HubSpot auth, and missing-reset-email as reset rejection. Semantic also accepts reset-email and rejects the 429 positive. Do not tune on those held-out outcomes. New representative development labels and independent support-agent review are needed. AI-assisted synthetic evaluation does not establish production accuracy/security/scale. No original sandbox, Firefox/Safari/physical mobile, production load, tenant isolation or accessibility certification verified.

Ignored local generated artifacts: `.venv`, `.runtime`, model/embedding/wheel `.cache`, frontend node_modules/build/cache, browser reports/screenshots, ZIP. Reversible initial npm backups (`frontend/node_modules.previous`, `frontend/package-lock.previous.json`) remain ignored and excluded from packaging; they are not unfinished application work.

Priority next steps: (1) manually run README setup/checks in the actual target sandbox with local Node bootstrap; (2) independently review labels and inspect known failures; (3) confirm deadline timezone, review archive and choose repository/ZIP submission; (4) user performs any commit/push/submission. No further feature implementation is required by this local handoff.

## Exact resume/run commands (PowerShell, repository root)

Read AGENTS.md and this status, inspect `git status --short`, `git diff`, and new/untracked files before changing anything. Verify the handoff rather than treating it as proof. Do not repeat completed work without a reason.

```powershell
# Existing verified local environment:
$env:SOLARI_OFFLINE = '1'
./.venv/Scripts/python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --no-access-log
# Separate terminal, same root:
$env:Path = "$(Get-Location)\.runtime\node-v22.23.2-win-x64;" + $env:Path
Push-Location frontend
npm start
# Open http://127.0.0.1:4200 ; Ctrl+C stops each server.
Pop-Location

# Checks, evaluation, packaging from root; stop servers before browser tests:
./.venv/Scripts/python.exe -m pytest -q
./.venv/Scripts/python.exe -m evaluation.run --split held_out --output evaluation/results.json
Push-Location frontend
npm run typecheck
npm run build
npm run test:e2e
Pop-Location
./.venv/Scripts/python.exe -m scripts.package_submission
Get-FileHash artifacts/solari-ticket-assistant.zip -Algorithm SHA256
```

For a fresh target environment, use the complete Windows bootstrap/install/model commands in README; the above commands assume installed dependencies and a provisioned model. No task-started running processes need resuming.
