# Project status

Updated: 2026-10-19 20:28 -06:00 (America/Edmonton). Latest informal-request policy/results and live processes are recorded at the end.

## Objective, requirements and deadline

Solari Ticket Assistant: Angular/TypeScript, FastAPI, TF-IDF, pinned CPU MiniLM, hybrid RRF, original JSON and in-memory indexes. Retrieve original historical resolution notes for agent review; applicability is always unverified. No generated fixes, database, new model/framework, training, Conda or paid service. Preserve supplied materials. Brief/scope: `case-study-1-support-ticket-similarity/case-study-brief.md`, `docs/IMPLEMENTATION_REQUEST.md`; current design: `SOLUTION_DESIGN.md`.

Deadline **Tuesday October 20, 2026 EOD; timezone unspecified**. Confirm recipient timezone before manual delivery. No commit, push, upload or submission authorized/performed.

## Git, completed work and current task

Actual starting/current HEAD: `319fb5f49bc2bae59042fd32732528a4ec19aca3` (user committed previous work; clean at start). Older reviewed `0dbf77d` is historical. Current focused corrections are **uncommitted and unstaged**: backend evidence/retrieval, UI/API/browser contracts, tests, non-destructive data inspection, current-definition evaluation, packaging and docs. AGENTS/Copilot instructions unchanged.

**Implemented and tested:**
- `backend/evidence.py`: retain all alphanumeric short clauses/negations; discard empty/punctuation-only fragments; preserve dotted/hyphenated technical identifiers. All retained clauses count toward eight-clause limit. Original displayed/stored data untouched. Versioned cache invalidation in `backend/retrieval.py`.
- Keyword precedent requires overall TF-IDF >=.25 plus minimum IDF-weighted per-clause token coverage >=.50; unknown terms stay in denominator. Semantic/hybrid keep previous .65 overall/.45 clause or .60 corroborated-identifier rules; no keyword OR bypass. Policy `historical-precedent-v5`. No product/ticket/example hardcoding or relevance-threshold retuning from final outcomes.
- API outcomes `historical_precedents`, `related_history_only`, `no_relevant_history`; errors remain 422/503. `result_semantics=historical-precedent-v1`, every note-bearing match `applicability=unverified`. UI clearly separates original review notes, weak/conflicting metadata, no history and unavailable service. This is not verified root-cause agreement.
- `scripts/inspect_data.py`: strict required-field/duplicate-ID validation retained; whitespace/casefold-only duplicate-content inspection reports repeats without deleting incidents. Actual supplied data: 40 records, no duplicate-content groups. No imputation/Isolation Forest.
- Test-first regressions `tests/test_focused_corrections.py`; actual degraded keyword backend in browser tests. Docs, approximately 1–2 page design, numbered Windows `docs/LAUNCHPAD_RUNBOOK.md`, packaging required members updated.

**Current task: completed.** ZIP generated and independently inspected (88 members; 27 original supplied/evaluation files byte-identical); CRC/source hashes and unchanged-source reproducibility verified. No unfinished application edits or task-owned servers; no listeners on 8000/8001/4200 at last check. Packaging is local and reproducible, not submission. Exact next action after completion: follow numbered runbook in actual Launchpad, then manual archive review/delivery.

## Confirmed runtime/dependency decisions

Tested actual Windows **Python 3.10.11** (`.venv310`, official local NuGet runtime `.runtime/python310/tools`) and **3.11.9** (`.venv`), venv pip **25.0.1**. Python 3.10.0 in original Launchpad was **not tested**. Original pip21.2.3, Node20.10.0, npm10.2.3 and Git2.43.0.windows.1 sandbox remain unverified; no precise Launchpad blocker observed because inaccessible here.

Angular requires an **additional project-local Node**, not original Node20.10.0: existing checksum bootstrap and explicit PATH retained; tested **Node22.23.2/npm10.9.8**, Windows PowerShell **5.1.26100.9711**, Git **2.50.1.windows.1**. System runtimes unchanged. Angular20.3.34, CLI/build20.3.40, TypeScript5.9.2, RxJS7.8.2, tslib2.8.1, Playwright1.56.1; lockfile unchanged.

Direct pins unchanged: FastAPI0.115.8, Uvicorn0.34.0, Pydantic2.10.6, NumPy1.26.4, scikit-learn1.6.1, Sentence Transformers3.4.1, Transformers4.48.3, Torch2.6.0 (actual CPU2.6.0+cpu), HTTPX0.28.1, pytest8.3.4. Tested Python-3.10-compatible CPU stack without new dependencies. `requirements-py310-resolved.txt` preserves 3.10.11 transitives; original 3.11 snapshot preserved. Reasons/complete setup: README and runbook.

Model unchanged: `sentence-transformers/all-MiniLM-L6-v2@1110a243fdf4706b3f48f1d95db1a4f5529b4d41`; actual offline (1,384) embedding, four CPU threads. JSON/in-memory indexes minimize infrastructure; restart on data changes. MiniLM similarity is not entailment; 256-wordpiece truncation and mechanism/negation ambiguity remain.

## Actual checks, commands and failures

- BEFORE behavior changes: `.venv310/Scripts/python -m pytest tests/test_focused_corrections.py -q` **15 failed**, including actual-model false reset-rejection notes after dropping short delivery clause; afterward 15 passed. An expanded identifier test later failed once because connector splitting broke `HTTP-429-and-retry`; generic connector boundaries fixed, cache suffix advanced. Not hidden as passing checks.
- Final `.venv310/Scripts/python -m pytest -q`: **62 passed** on3.10.11; `.venv/Scripts/python -m pytest -q`: **62 passed** on3.11.9. One nonfatal Starlette/AnyIO deprecation warning each. Includes deterministic policy, actual-model, strict data, API/cache, no-match/degraded/error tests.
- Frontend `npm run typecheck` and `npm run build`: passed, initial177.49kB/estimated transfer49.47kB. `SOLARI_TEST_PYTHON=.venv310/Scripts/python.exe`, frontend `npm run test:e2e`: **7 passed**, actual full and keyword-only HTTP backends, billing/429, missing-email/Snowflake, contradictory short clauses, no-history, errors/stale responses/mobile. Owned processes stopped.
- Windows PowerShell5.1 `scripts/preflight.ps1 -Python .venv310/Scripts/python.exe` with local Node PATH: passed runtime/packages/pip check/npm ls, actual offline embedding, HTTP ready/all capabilities, cleanup, frontend typecheck/build. No original Launchpad claim.
- `.venv310/Scripts/python -m scripts.inspect_data`: passed40records/no duplicate-content groups; repeats retained in tests. `python -m evaluation.review_precedents`: completed actual-model exposed regression; final source/case/data hashes and runtime/latency recorded in new report.
- `.venv310/Scripts/python -m compileall -q backend scripts evaluation tests`: passed final source. Preservation `git diff --exit-code 319fb5f -- case-study-1-support-ticket-similarity 'evaluation/*.json'`: passed, original data and tracked historical JSON unchanged.
- `git diff --check` caught trailing blank EOF in validation doc; removed. Final `git diff --check` passed (configured LF/CRLF warnings only). Initial independent ZIP audit incorrectly included intentionally excluded `__MACOSX` metadata and raised KeyError; corrected exclusion and rerun passed. Earlier tool quoting/doc context errors were corrected without application changes. Full details: `docs/VALIDATION.md`.

## Honest evaluation and remaining failures

Earlier original/release cases are now **exposed regression**, not fresh tests. All previous JSON/results preserved. New `precedent-regression-results.json` uses displayed historical-precedent relevance, **not equivalent to old supported-resolution definitions**. Initial current run retained as `precedent-initial-results.json`; old narratives retained in `V4_EVALUATION.md`/`ORIGINAL_EVALUATION.md`. No cross-definition accuracy claim. New targeted cases are also exposed, AI-authored labels, not independent human review.

Current Recall@3/MRR: original keyword .25/.25 (6/8 positive abstentions); prior-release keyword .375/.375 (5/8); targeted keyword .5/.5 (2/4). Semantic/hybrid1.0/1.0 on all these small splits, but targeted `short-still-fails` returns correctT-1001 **plus irrelevant extraT-1004** (1/4 positives) in semantic/hybrid. Zero note-bearing results on labeled negatives (4/4/3); this does not establish general safety. The short missing-email contradiction now withholds false reset-rejection notes in actual-model/browser tests. Conservative keyword recall is a substantial cost; no tuning to remove all observed failures.

Final hybrid warm median/p95: original10.187/20.704ms; prior-release12.924/17.376ms; targeted11.143/15.244ms. Windows3.10.11, four Torch threads, one warmup plus5searches/query, no concurrent test servers; excludes HTTP/model startup, no SLA/load claim. Definitions/denominators/remaining limitations: `evaluation/README.md`.

## Remaining manual steps and exact resume

1. Verify original Launchpad Python3.10.0 and download/execution permissions using `docs/LAUNCHPAD_RUNBOOK.md`; do not substitute host testing. Retain exact blocked URL/HTTP/TLS/runtime error; do not disable TLS.
2. Review actual UI/archive and independent representative relevance labels. Physical devices/other browsers, production security/load/tenant isolation remain unverified.
3. Confirm deadline timezone; manually publish/transfer and submit. Current changes are not on remote; `git pull` alone will not fetch uncommitted corrections. No automatic publication.

Resume from root: read AGENTS/status, `git status --short`, inspect diffs/new files, reconcile handoff with actual code. Last verified milestone is full tests/browser/preflight/current evaluation; do not repeat implementation without evidence. Complete numbered commands and troubleshooting: `docs/LAUNCHPAD_RUNBOOK.md`.

```powershell
# Existing developer environment; fresh Launchpad creates .venv per runbook.
$env:Path = (Join-Path (Get-Location) '.runtime/node-v22.23.2-win-x64') + ';' + $env:Path
$env:SOLARI_OFFLINE = '1'
./scripts/preflight.ps1 -Python .venv310/Scripts/python.exe
./.venv310/Scripts/python.exe -m pytest -q
./.venv310/Scripts/python.exe -m scripts.package_submission
./.venv310/Scripts/python.exe -m zipfile -t artifacts/solari-ticket-assistant.zip
```

No running process requires resuming. Ignored environments/runtimes/model caches/node_modules/build/browser outputs excluded from archive.

## Local application startup — 2026-10-19 16:44 -06:00 (America/Edmonton)

**In progress:** run existing application only; no feature/source changes. Actual clean HEAD is `605c4bc744150b7d07628b8cd282b09d3abfaeaf`; earlier uncommitted descriptions above are historical. Read AGENTS/status/README/runbook and inspected Git/runtime/ports. Active Python3.11.9, compatible system Node22.23.2/npm10.9.8. Existing `.venv` Python3.11.9 and `.venv310` preserved; no environment creation needed. Ports8000/4200 free. Next: pinned pip install/check, npm ci, model verification, preflight/tests, separate server processes and HTTP checks. Use existing local Node PATH; no system replacement/bootstrap download needed.

Startup milestone: existing .venv reused; pip install -r requirements.txt completed successfully (all pinned requirements already satisfied), pip check: No broken requirements found. Local Node22.23.2/npm10.9.8 selected. npm ci and model provisioning/verification still in progress; no success claimed yet.

Startup milestone: npm ci passed (411 packages, audit zero vulnerabilities). Cleared SOLARI_OFFLINE, scripts.download_model passed pinned MiniLM real embedding verification (1,384); offline re-enabled for subsequent processes. Preflight/tests in progress.

Startup milestone: documented preflight passed under Python3.11.9/local Node22.23.2, including offline embedding, temporary HTTP ready with keyword/semantic/hybrid and40tickets, dependency checks, frontend typecheck/build. Full backend pytest still running.

Startup milestone: backend pytest passed62tests in15.90s on Python3.11.9, one nonfatal Starlette/AnyIO deprecation warning. Starting separate hidden PowerShell terminal processes with log redirection; final HTTP verification pending.

### Startup complete — 2026-10-19 16:47 -06:00 (America/Edmonton)

Current task completed: existing application running, no application changes. This startup section supersedes earlier statements about no running servers/current HEAD. HEAD `605c4bc744150b7d07628b8cd282b09d3abfaeaf`; initial working tree clean; only PROJECT_STATUS.md changed by this task. Existing environments preserved. No commit/push/submission, bootstrap download or system runtime changes.

Actual checks: Python3.11.9 (.venv), pip25.0.1; active and selected local Node22.23.2/npm10.9.8; Git2.50.1.windows.1. Pinned pip install succeeded, pip check no broken requirements; npm ci411packages/zero audit findings. Model command with SOLARI_OFFLINE cleared verified pinned revision and real (1,384) embedding; subsequent processes offline. Preflight passed all dependency/model/API/frontend checks. Backend tests62passed in15.90s, one nonfatal Starlette/AnyIO deprecation warning. No failed install/test commands. Initial HTML diagnostic checked incorrect tag solari-app (false); actual source uses app-root, which was confirmed present. Angular nonfatal prebundling notice: disabled with scripts optimization. No original Launchpad3.10.0 claim.

Running **separate hidden PowerShell terminal processes**, intentionally left running for user:
- Backend terminal26348; Uvicorn listener46960 on127.0.0.1:8000. Offline, all capabilities. Logs `.cache/run-backend.out.log` / `.cache/run-backend.err.log`.
- Frontend terminal67832; Angular listener49224 on127.0.0.1:4200. Logs `.cache/run-frontend.out.log` / `.cache/run-frontend.err.log`.
- Launcher scripts `.cache/run-backend.ps1` / `.cache/run-frontend.ps1`; PID record `.cache/run-processes.json`. All ignored/local only.

Verified HTTP: UI200 with app-root; API statusready, capabilities keyword/semantic/hybrid,40tickets, pinned model revision, message null. Angular `/api/health` proxy ready. POST via Angular `/api/search` for duplicate billing returned historical_precedents,1match, applicabilityunverified. Not a new browser automation or manual visual check.

Exact setup/check commands executed from repository root (existing .venv meant no creation needed; compatible active Node meant no bootstrap needed):

```powershell
git status --short
git rev-parse HEAD
git log -1 --oneline
git diff --stat
Get-Command python,node,npm
python --version
node --version
npm --version
git --version
./.venv/Scripts/python.exe --version
./.venv/Scripts/python.exe -m pip --version
./.venv/Scripts/python.exe -m pip install -r requirements.txt
./.venv/Scripts/python.exe -m pip check
$env:Path = (Join-Path (Get-Location) '.runtime/node-v22.23.2-win-x64') + ';' + $env:Path
Push-Location frontend
npm ci
Pop-Location
Remove-Item Env:SOLARI_OFFLINE -ErrorAction SilentlyContinue
./.venv/Scripts/python.exe -m scripts.download_model
$env:SOLARI_OFFLINE = '1'
Remove-Item Env:SOLARI_KEYWORD_ONLY -ErrorAction SilentlyContinue
./scripts/preflight.ps1
./.venv/Scripts/python.exe -m pytest -q
```

Exact server launcher contents (created using PowerShell literal here-strings and Set-Content; no machine execution-policy change):

`.cache/run-backend.ps1`:
```powershell
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$env:SOLARI_OFFLINE = '1'
Remove-Item Env:SOLARI_KEYWORD_ONLY -ErrorAction SilentlyContinue
& ./.venv/Scripts/python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --no-access-log
```

`.cache/run-frontend.ps1`:
```powershell
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$env:Path = (Join-Path (Get-Location) '.runtime/node-v22.23.2-win-x64') + ';' + $env:Path
Set-Location frontend
& npm.cmd start
```

Exact process-start commands:
```powershell
$backendScript = (Resolve-Path .cache/run-backend.ps1).Path
$frontendScript = (Resolve-Path .cache/run-frontend.ps1).Path
$backendTerminal = Start-Process powershell.exe -ArgumentList @('-NoProfile','-File',('"' + $backendScript + '"')) -WorkingDirectory (Get-Location).Path -WindowStyle Hidden -RedirectStandardOutput .cache/run-backend.out.log -RedirectStandardError .cache/run-backend.err.log -PassThru
$frontendTerminal = Start-Process powershell.exe -ArgumentList @('-NoProfile','-File',('"' + $frontendScript + '"')) -WorkingDirectory (Get-Location).Path -WindowStyle Hidden -RedirectStandardOutput .cache/run-frontend.out.log -RedirectStandardError .cache/run-frontend.err.log -PassThru
```

HTTP verification commands:
```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/health
Invoke-WebRequest http://127.0.0.1:4200 -UseBasicParsing
Invoke-RestMethod http://127.0.0.1:4200/api/health
$body = @{subject='Duplicate charges';description='Two identical monthly charges';mode='keyword';top_k=3} | ConvertTo-Json
Invoke-RestMethod http://127.0.0.1:4200/api/search -Method Post -ContentType application/json -Body $body
```

**Next action:** open http://127.0.0.1:4200 and use the application. API schema http://127.0.0.1:8000/docs. No unfinished edits; servers intentionally live. To stop this session's trees, first confirm IDs still belong to these processes (avoid PID reuse), then:
```powershell
Get-Process -Id 26348,67832 -ErrorAction SilentlyContinue
Get-NetTCPConnection -State Listen | Where-Object { $_.LocalPort -in 8000,4200 }
taskkill /PID 26348 /T /F
taskkill /PID 67832 /T /F
```
To restart later after stopping, run the launcher scripts in separate root terminals (`./.cache/run-backend.ps1` and `./.cache/run-frontend.ps1`), or documented runbook commands. Do not start duplicate listeners. Latest archive predates this status-only update; archive was not regenerated because this request is local startup only.

## Informal-request investigation — in progress
User reported hybrid false rejection: reproduce scores/rule, freeze varied regression cases, implement small domain-neutral handling of generic request wording without lowering global thresholds, preserve symptoms/negation, run actual-model before/after and existing checks. Existing status-only changes preserved; HEAD605c4bc. No dependencies/runtimes/commits/pushes. Running servers from startup may require backend restart after final verification.

Milestone: reproduced original scores keyword.262235/semantic.559230/clause.606230. Exact blocker overall semantic<.65, not clause coverage; no shared identifier. Frozen18cases plus original/prior-release/short regressions baseline saved before behavior change. New tests10failed before implementation. In progress: query-only polite-framing removal retains objects/negation; short2–12content-token route requires keyword>=.25, semantic>=.60, ALLclauses>=.65, lexical>=.50 and complete context. Global thresholds unchanged. No result-driven retuning planned.

Milestone: targeted10tests passed after implementation; first revised report retained as informal-initial-v6-results.json. Informal hybrid recall/MRR.625→.875, positive abstentions3/8→1/8, negatives with notes0/10→0/10. Remaining informal429 paraphrase abstains; no threshold retuning. Existing original/prior-release/short-case relevance unchanged, including known extra login precedent. Diff review caught a Windows text-encoding read corrupting curly-apostrophe token regex; restored original Unicode character and added explicit regression. Final-source tests/report in progress; older current evaluator now refuses overwriting v5 report.

## Informal-request revision complete — 2026-10-19 20:28 -06:00 (America/Edmonton)

This section supersedes previous policy/test/live-backend descriptions. HEAD remains605c4bc744150b7d07628b8cd282b09d3abfaeaf. Existing status-only startup edits preserved; current uncommitted changes are evidence/retrieval, tests, independent evaluation scripts/cases/reports, README/design/validation/evaluation/runbook/status. No dependency/runtime/lockfile/data changes, commit, push or submission.

**Implemented:** `backend/evidence.py` query-only generic polite-framing removal preserves its objects, symptoms, negation and technical identifiers. `backend/retrieval.py` uses normalized query for scoring, original historical/displayed text unchanged. Existing global semantic/clause/identifier thresholds unchanged. Additional short-context route (2–12 distinct meaningful tokens) conjunctively requires keyword>=.25, semantic>=.60, ALL retained clauses>=.65, lexical>=.50 and complete context; raw clause cap still enforced. No product/ID/billing-query hardcoding. Policy/cache version `informal-precedent-v6`; API semantics remain historical-precedent-v1, applicability always unverified. No relevance tuning after evaluation.

**Reproduced exact cause:** reported query T-1303 keyword.262235, semantic.559230, clause.606230. Original overall semantic requirement>=.65 failed; clause>=.45 passed; no shared technical identifier. Generic related-history reason did not identify the specific gate, so scores/code were inspected. Revised keyword.262235, semantic.642657, clause.723596, lexical.666667: short route returns original notes (not verified root cause/fix).

**Actual checks/artifacts:** before change `pytest tests/test_informal.py -q`10failed; after10passed. Expanded final full suite `./.venv/Scripts/python.exe -m pytest -q`:75passed on3.11.9 in6.41s; `./.venv310/Scripts/python.exe -m pytest -q`:75passed on3.10.11 in34.21s, one nonfatal Starlette/AnyIO warning each. Final targeted13passed in5.46s after evaluator output-path guard changes. Actual pinned model required, no mock-only correctness claim. Compileall passed backend/evaluation/tests. Preservation diff and whitespace check passed. No frontend/browser automation rerun for this backend-only revision; earlier UI tests remain historical.

`evaluation/informal-cases.json` froze18exposed cases (8positive/10negative) before policy edits; freeze records SHA/time/baseline source. `informal-baseline-results.json` vs `informal-revised-results.json` use SAME displayed unverified-precedent metrics; previous results untouched. First v6 run preserved as informal-initial-v6-results.json. Diff review caught Windows default decoding accidentally corrupting curly apostrophe in lexical tokenizer; restored original Unicode, added regression, reran final checks/report. Frozen case/baseline/final source hashes verified. AI-authored labels are synthetic exposed diagnosis, not fresh independent evaluation.

Informal keyword Recall@3/MRR.25→.375; positive abstentions6/8→5/8. Semantic/hybrid.625→.875; abstentions3/8→1/8. Negative note presentations0/10→0/10; no extra wrong precedents on informal positives. Existing original/prior-release/short regressions relevance/error metrics unchanged, including Snowflake/missing-email withholding and explicit429/billing controls. Remaining miss: short informal429 query stays related-only. Previously known login case still includes an irrelevant extra precedent. No tuning to erase these failures. Timings are recorded but overlap compatibility testing/dev servers, so no controlled performance comparison. Full diagnosis/trade-offs: `evaluation/INFORMAL_REVISION.md`.

**Live application:** only previous owned backend tree26348 was identity-checked and stopped (`taskkill /PID 26348 /T /F`), then `.cache/run-backend.ps1` restarted using Start-Process powershell.exe -NoProfile -File with WindowStyle Hidden and log redirects. New backend terminal**50096**, Uvicorn listener**53476** on8000; logs `.cache/run-backend-v6.out.log`/`.cache/run-backend-v6.err.log`. Frontend terminal**67832**, listener**49224** on4200 unchanged. Updated `.cache/run-processes.json`. Verified API ready/all3capabilities/40tickets and POST through Angular proxy returns current v6 T-1303 notes. UI http://127.0.0.1:4200 remains running; no unfinished edits/process waits.

Exact evaluation commands actually executed, with SOLARI_OFFLINE=1:
```powershell
./.venv/Scripts/python.exe -m evaluation.review_informal --output informal-baseline-results.json
# After policy implementation; initial v6 run later preserved under informal-initial-v6-results.json.
./.venv/Scripts/python.exe -m evaluation.review_informal --output informal-revised-results.json
# Final-source report refreshed using that now-free output path after preserving first run.
./.venv/Scripts/python.exe -m pytest -q
./.venv310/Scripts/python.exe -m pytest -q
./.venv/Scripts/python.exe -m pytest tests/test_informal.py -q
./.venv/Scripts/python.exe -m compileall -q backend evaluation tests
git diff --exit-code 605c4bc -- case-study-1-support-ticket-similarity 'evaluation/*.json'
git diff --check
```

**Exact next action:** use running UI to review reported query and limitations; independent representative labels remain needed. For future verification, output names must be new (existing reports are protected):
```powershell
$env:SOLARI_OFFLINE='1'
./.venv/Scripts/python.exe -m pytest -q
./.venv/Scripts/python.exe -m evaluation.review_informal --output "informal-check-$(Get-Date -Format yyyyMMdd-HHmmss)-results.json"
Invoke-RestMethod http://127.0.0.1:8000/api/health
```
To stop current trees, verify terminal PID ownership first, then `taskkill /PID 50096 /T /F` and `taskkill /PID 67832 /T /F`. Reuse existing .cache launchers in separate terminals after stopping; no duplicate listeners. Existing submission ZIP predates this application correction and must be regenerated if packaging this revision (not requested in this task). Original Launchpad3.10.0 remains untested; runtime requirements/deadline/manual publication restrictions above unchanged.
