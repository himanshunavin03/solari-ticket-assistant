# Project status

Updated: 2026-10-19 11:33 -06:00 (America/Edmonton).

## Objective, scope, deadline

Solari Ticket Assistant: Angular/TypeScript, FastAPI, TF-IDF, pretrained CPU MiniLM, RRF, supplied JSON/in-memory indexes, original-resolution evidence, tests/evaluation/docs/local ZIP. No database, training, generated fixes, paid API or Conda. Scope/brief: `docs/IMPLEMENTATION_REQUEST.md`, `case-study-1-support-ticket-similarity/case-study-brief.md`; decisions: `SOLUTION_DESIGN.md`.

Deadline **Tuesday October 20, 2026 EOD; timezone unspecified**. Confirm recipient timezone before manual delivery.

## Current state and Git

**Completed:** implementation, requested checks, documentation, ZIP inspection and handoff. No unfinished edits or task-owned servers. Full preflight also passed under Windows PowerShell 5.1. Exact next user action: run README setup/preflight inside actual Launchpad, then review the archive and confirm submission timezone. No automatic commit/push/upload/submission.

Reviewed/actual HEAD: `0dbf77d1e9e8ceac1b9130a66c7049f34fbce6f7`; initial tree clean, no newer fixes. Current changes are uncommitted/un-staged: evidence/retrieval and response fields, related-history UI/browser tests, preflight/packaging scripts, evaluation snapshots/cases/reports, 3.10 resolved requirements, tests, docs/status and ignore rule. AGENTS/Copilot instructions unchanged. No commit, push, upload or submission performed. Git preservation diff confirms original supplied files and original evaluation JSON/cases unchanged.

## Actual runtimes and dependencies

**Windows Python 3.10.11**: official NuGet runtime at `.runtime/python310/tools`, project-local `.venv310`, pip **25.0.1**, direct manifest installation and real CPU inference/tests passed. Existing `.venv` remains **Python 3.11.9**, also tested. No system Python replacement. `requirements-py310-resolved.txt` is actual 3.10.11 snapshot (SciPy 1.15.3); `requirements-resolved.txt` preserves original 3.11 snapshot.

Original Launchpad **Python 3.10.0 / pip 21.2.3 / Node 20.10.0 / npm 10.2.3 / Git 2.43.0.windows.1 was NOT executed**. Exact patch and sandbox/network/policy compatibility remain manual. No Launchpad installation blocker can be reported because that sandbox is inaccessible here.

Frontend requires **additional compatible Node**, not the supplied 20.10.0. Existing checksum-verified `.runtime/node-v22.23.2-win-x64` bootstrap preserved; explicit local PATH route tested. Node **22.23.2**, npm **10.9.8**, host Git **2.50.1.windows.1**. Angular runtime/compiler **20.3.34**, CLI/build **20.3.40**, TypeScript **5.9.2**, RxJS **7.8.2**, tslib **2.8.1**, Playwright **1.56.1**; lockfile unchanged. Bootstrap now uses basic parsing for PowerShell 5.1; existing-runtime path tested on **5.1.26100.9711**. No Angular downgrade/system runtime replacement.

Direct Python pins unchanged: FastAPI 0.115.8, Uvicorn 0.34.0, Pydantic 2.10.6, NumPy 1.26.4, scikit-learn 1.6.1, Sentence Transformers 3.4.1, Transformers 4.48.3, Torch 2.6.0 (CPU runtime 2.6.0+cpu), HTTPX 0.28.1, pytest 8.3.4. Tested Python-3.10-compatible CPU stack; no extra inference model/dependencies. Complete versions/reasons: README and resolved files.

## Implemented decisions/artifacts

- `backend/evidence.py` / `retrieval.py`: **clause-coverage-v4** separates supported resolutions from potentially related metadata (resolution notes withheld). Support: overall cosine >=.65 plus every retained description clause covered >=.45; alternate generic shared >=3-digit identifier with overall/identifier-clause >=.60. No product names, IDs, specific code allowlist or example strings. Generic English splitting/four-word minimum; >8 query clauses abstain. TF-IDF/RRF ranking retained. Keyword, including degraded mode, is intentionally related-context-only; zero supported recall is a capability restriction, not an accuracy win. Semantic/hybrid unavailability still explicit 503.
- Same pinned `sentence-transformers/all-MiniLM-L6-v2@1110a243fdf4706b3f48f1d95db1a4f5529b4d41`; four CPU threads; safe normalized historical clause embeddings with versioned cache invalidation. Individual embeddings retain 256-wordpiece truncation.
- `frontend/src/`, `frontend/e2e/`: supported cards vs expandable metadata-only history; no-match, errors, stale suppression and new issue-level browser checks. `scripts/preflight.ps1`/`.py`: versions, exact dependencies, real offline embedding, owned HTTP readiness/all capabilities/cleanup, frontend checks; installs nothing.
- README, design, evaluation README, validation/demo/AI logs updated. Detailed commands/failures: `docs/VALIDATION.md`. Packaging requires current reports/freeze, original results, 3.10 snapshot, preflight and source; excludes all environments, models/caches/builds/Git/secrets.

## Evaluation provenance/results

Old `held_out` is now **exposed regression**, never described as untouched for this revision. Original cases/results preserved; baseline source frozen from reviewed commit. Intermediate V2/V3 fresh sets became exposed during iteration and retain results/policy snapshots. Final `release-cases.json` and source hashes froze at **2026-10-19 17:21:51 UTC before release scoring**; no policy tuning afterward. Text hashes normalize CRLF; raw data/archive hashes retain bytes. These AI-authored labels are not independent human review.

Current results/denominators/all modes: `evaluation/README.md`, `release-development-results.json`, `release-regression-results.json`, `release-results.json`.

| Hybrid | False acceptances | False rejections | Recall@3 | MRR |
| --- | --- | --- | --- | --- |
| Development (12 positive/4 negative) | 3→0 | 1→1 | .9167→.875 | .9167→.9167 |
| Exposed regression (8/4) | 2→0 | 0→0 | 1→1 | 1→1 |
| Frozen release (8/4) | 2→0 | 1→1 | .875→.875 | .875→.875 |

Both supplied misleading examples withhold resolutions; billing and original HTTP 429 still accepted. Release widget-overlap is related-only; development broad rate-limit paraphrase and one secondary multi-issue ticket lose support. Candidate recall 1.0 for revised hybrid release/regression does not mean supported-resolution recall. Earlier sets retain SMS recovery/2FA and newly phrased reset-mail false acceptances: general mechanism ambiguity remains unresolved. No quality advantage of hybrid over semantic on release.

Release hybrid warm median/p95 **16.675/26.485→17.852/24.720 ms**, 60 samples/mode, Windows 3.10.11, Intel64 Family 6 Model 186 Stepping 2 / 20 logical CPUs / four Torch threads. Final rerun after browser cleanup; scheduling noise, no production/SLA/throughput claim.

## Actual checks and failures

- Full `pytest -q`: **46 passed on 3.10.11**, **46 passed on 3.11.9**, one nonfatal Starlette/AnyIO warning each. Deterministic policy, cache/API, real billing/429/target no-match, original-result protection and metric denominators covered. Targeted evaluation tests after hash helper change: **2 passed**; explicit release hash/no-drift assertions passed.
- Preflight passed with 3.10.11 and explicit local Node, including Windows PowerShell **5.1.26100.9711**: pip check, packages, actual offline (1,384) MiniLM embedding, HTTP ready/all three capabilities, cleanup, npm ls/typecheck/build. Bundle **177.30 kB**, estimated transfer **49.44 kB**. npm audit: **zero findings**. Compileall passed.
- Browser tests against actual 3.10.11 API: **6 passed**, including both misleading examples without resolution text, billing/429, unrelated no-match, mobile/reset, errors, stale responses and simulated degradation. Owned servers stopped.
- V2/V3 policy initially rejected valid 429; two real-model tests failed. Generic identifier corroboration .60 chosen on exposed regression, tested before final release freeze. All reports retained; no product-specific patches. PowerShell display/parser and doc-patch context failures corrected without evaluation effect. Whitespace check initially found blank EOF in validation doc; trimmed and `git diff --check` passed (configured CRLF warnings only).
- ZIP generated and independently inspected: **79 files**, required current/original evaluation, docs/manifests/preflight; **40 original tickets byte-for-byte unchanged**; CRC and source SHA256 verified. Final archive regenerated with current docs/status; unchanged-source repeat packaging verifies deterministic output. Manifest: `artifacts/manifest.json`; archive: `artifacts/solari-ticket-assistant.zip`. No listeners remain on 8000/4200.

## Remaining manual work and exact resume

No unresolved local implementation/test blocker. Original Launchpad patch/network/policy restrictions, independent labels, physical mobile/other browsers, production security/load/tenant isolation remain unverified. MiniLM is not entailment; short fragments, negation and numeric collisions can mislead. Confirm deadline timezone, review demo and archive, then user manually submits. No automatic publication authorized. Ignored `.venv*`, `.runtime`, `.cache`, npm backups/build/browser outputs remain excluded from ZIP.

Read AGENTS/status and verify `git status --short`, diffs and new files before editing. Local checks use `.venv310/Scripts/python.exe`; fresh Launchpad setup uses its Python to create `.venv` (complete commands also in README):

```powershell
python --version
node --version
./scripts/bootstrap-node.ps1
$env:Path = "$(Get-Location)\.runtime\node-v22.23.2-win-x64;" + $env:Path
python -m venv .venv
./.venv/Scripts/python.exe -m pip install --upgrade pip==25.0.1
./.venv/Scripts/python.exe -m pip install -r requirements.txt
Push-Location frontend
npm ci
Pop-Location
./.venv/Scripts/python.exe -m scripts.download_model
$env:SOLARI_OFFLINE = '1'
./scripts/preflight.ps1
./.venv/Scripts/python.exe -m pytest -q
./.venv/Scripts/python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --no-access-log
# Separate root terminal: set same local Node PATH, then:
Push-Location frontend
npm start
# Open http://127.0.0.1:4200; Ctrl+C stops each server, then Pop-Location.
# Packaging from root using installed venv:
./.venv/Scripts/python.exe -m scripts.package_submission
```

If provisioning is blocked, retain exact bootstrap/preflight runtime/HTTP/TLS/execution error. Offline reuse requires prior model provisioning. No task-owned process needs resuming after final checks finish.
