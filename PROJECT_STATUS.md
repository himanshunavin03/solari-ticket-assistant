# Project status

Updated: 2026-10-19 12:00 -06:00 (America/Edmonton).

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
