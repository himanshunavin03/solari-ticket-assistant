# October 19 revision — current validation

Reviewed baseline: `0dbf77d1e9e8ceac1b9130a66c7049f34fbce6f7`, clean at start; no newer implementation fixes existed. All original supplied materials and original evaluation cases/results remain unchanged. The section below the separator preserves October 17 historical checks, not current behavior.

## Actual runtimes and compatibility

Windows x64; actual **Python 3.10.11** provisioned from the official `python` NuGet package into `.runtime/python310/tools`, following the Python Windows documentation's CI/runtime route. It created `.venv310`; pip upgraded inside that venv from 23.0.1 to **25.0.1**. No Conda, system Python replacement, or PATH change to system installation. Installed `requirements.txt` successfully, including a real CPU Torch wheel. `requirements-py310-resolved.txt` records actual transitives (SciPy 1.15.3). **Python 3.11.9** in existing `.venv` also verified. The original Launchpad **Python 3.10.0 / pip 21.2.3** environment was not accessible or executed; exact patch/sandbox validation remains manual.

Frontend: **Node 22.23.2, npm 10.9.8**, Angular runtime/compiler **20.3.34**, CLI/build **20.3.40**, TypeScript **5.9.2**, RxJS **7.8.2**, tslib **2.8.1**, Playwright **1.56.1**. Git host **2.50.1.windows.1**. Angular was not downgraded; original Node 20.10.0 is insufficient. Existing `.runtime/node-v22.23.2-win-x64` bootstrap retained; explicit local PATH selection was used for preflight/build. No Launchpad installation-policy failure is invented: this machine allowed the runtime route, and actual Launchpad restrictions remain unknown.

## Commands actually run and results

| Command | Result |
| --- | --- |
| `.runtime/python310/tools/python.exe --version`; `... -m venv .venv310` | Python 3.10.11; local venv created. |
| `.venv310/Scripts/python -m pip install --upgrade pip==25.0.1`; `... -m pip install -r requirements.txt`; `... -m pip check` | Installed successfully; no broken requirements. |
| `SOLARI_OFFLINE=1`, then `.venv310/Scripts/python -m scripts.download_model` | Actual pinned CPU MiniLM produced normalized (1,384) embedding; no mock. |
| `.venv310/Scripts/python -m pytest -q` | **46 passed**, one nonfatal Starlette/AnyIO deprecation warning. Includes deterministic policy boundaries/identifier guards, original-result protection, metric denominators, real billing/429 and both supplied no-match regressions. |
| `.venv/Scripts/python -m pytest -q` | **46 passed** on Python 3.11.9; same nonfatal warning. |
| `.venv310/Scripts/python -m compileall -q backend scripts evaluation tests` | Passed syntax compilation. |
| `./scripts/preflight.ps1 -Python ./.venv310/Scripts/python.exe` | Passed active runtime reporting, exact package/dependency checks, real offline embedding, owned HTTP server readiness with keyword/semantic/hybrid, cleanup, npm dependency check, frontend typecheck/build. Repeated with project-local Node explicitly first on PATH; passed. |
| `powershell.exe -NoProfile -File scripts/preflight.ps1 -Python .venv310/Scripts/python.exe` | Full preflight passed under Windows PowerShell **5.1.26100.9711**, with local Node PATH, real Python 3.10.11/model/readiness/build and cleanup. Existing-runtime Node bootstrap path also passed there; basic parsing added for download compatibility. This is not a fresh-download or original Launchpad certification. |
| `npm run typecheck`; `npm run build` (through preflight, frontend) | Passed; final initial bundle **177.30 kB**, estimated transfer **49.44 kB**. |
| `npm audit --audit-level=low` (frontend) | Zero reported vulnerabilities. Existing manifest and lockfile unchanged. |
| `SOLARI_TEST_PYTHON=.venv310\Scripts\python.exe`, `npm run test:e2e` (frontend) | **6 passed**, real Python 3.10.11 API. Billing, HTTP 429, Snowflake/missing-email no-match with withheld resolutions, unrelated no-match, clear/mobile, failures/validation, stale responses, simulated degradation. Test-owned servers stopped. |
| `.venv310/Scripts/python -m evaluation.compare_revision --split development/regression/release` (three commands) | All modes measured against exact reviewed baseline. Original/earlier results preserved. Source/case hashes frozen before release evaluation; no tuning afterward. Final regression/release latency rerun after browser server cleanup. See evaluation README and release JSON for full results. |
| `git diff --exit-code 0dbf77d1e9e8ceac1b9130a66c7049f34fbce6f7 -- case-study-1-support-ticket-similarity evaluation/results.json evaluation/cases.json evaluation/development-results.json evaluation/development-initial-results.json evaluation/development-evidence.json` | Passed; originals unchanged. |

Snapshot comparison: exposed regression hybrid false acceptances **2→0**, false rejections **0→0**, Recall@3/MRR **1→1**. Release set hybrid false acceptances **2→0**, false rejections **1→1**, Recall@3/MRR **.875→.875**; candidate recall 1.0. Supported and related context are measured separately. Keyword now provides related metadata only, so its zero supported recall is a deliberate capability restriction, not an accuracy win.

## Failures, recovery and unverified limits

- First revised coverage policy rejected valid original HTTP 429 despite fixing both supplied false acceptances. Added a generic shared numeric identifier signal. Initial corroboration cutoff .65 still failed two real-model assertions: overall cosine .649 and identifier clause .608. Chose .60 corroboration using the already-exposed regression, verified both tests, then froze a new release set before scoring V4. No specific HTTP code, product, ticket ID or example text rule.
- Intermediate fresh sets became exposed through those iterations. Their reports and policy functions remain preserved; they are **not** untouched final tests. Final release set was frozen separately, but all labels are still AI-authored by the same implementer, not independent human judgments.
- Remaining observed failures: release widget-overlap is related-only (false rejection); development broad rate-limit paraphrase is related-only, and one secondary multi-issue sync ticket loses supported recall. Intermediate reports record falsely accepted SMS recovery as two-factor delivery and a newly phrased reset-email query. Passing the two original target examples does not solve those whole failure classes.
- A PowerShell metrics display command had a parser error from piping a foreach statement directly; assigned its result and reran successfully. A documentation patch context mismatch was corrected after reading the actual file. Neither altered model/evaluation outcomes.
- No original Launchpad, Python 3.10.0 exact patch, Firefox/Safari/physical mobile, production load/security/tenant isolation, calibrated abstention, or independent support-agent review verified. Additional Node download and script execution must be permitted in Launchpad. If blocked, preflight/bootstrap surfaces the concrete runtime/HTTP/TLS/execution error; no such Launchpad error was observed here.

Packaging verification is recorded in PROJECT_STATUS.md and artifacts/manifest.json after the final documentation refresh. No commit, push, upload or submission performed.

---

# Historical October 17 validation (preserved)
# Actual validation record

Executed on Windows, October 17, 2026 (America/Edmonton). This records actual commands and outcomes, not a suggested test plan. The supplied Python 3.10.0/Node 20.10.0 sandbox was not run. See `README.md` for target setup and remaining manual verification.

| Command (repository root unless stated) | Actual outcome |
| --- | --- |
| `python --version`, `python -m pip --version`, `node --version`, `npm --version`, `git --version` | Host Python 3.11.9, system pip 24.0, Node 22.23.2, npm 10.9.8, Git 2.50.1.windows.1. |
| `python -m venv .venv`; `.venv/Scripts/python -m pip install --upgrade pip==25.0.1` | Succeeded; project-local environment, no Conda. |
| `.venv/Scripts/python -m pip install -r requirements.txt`; `... -m pip check` | Final install satisfied all pins; no broken requirements. Initial large-wheel download needed the recovery below. Actual resolved versions in `requirements-resolved.txt`. |
| `./scripts/bootstrap-node.ps1` | Downloaded Node 22.23.2 under `.runtime`, checked official SHA256, executable printed v22.23.2. Local npm printed 10.9.8. No system replacement. |
| `npm ci` (frontend) | Succeeded from regenerated exact-version lockfile. |
| `npm run typecheck` / `npm run build` (frontend) | Both passed on final UI code. Initial bundle 175.87 kB raw, approximately 49.10 kB estimated transfer. |
| `npm audit --audit-level=low` / `npm ls --depth=0` (frontend) | Zero reported vulnerabilities on patched dependency tree; exact direct packages matched manifest. |
| `.venv/Scripts/python -m compileall -q backend scripts evaluation tests` | Passed syntax compilation. |
| `./scripts/prefetch-model.ps1` | Pinned model snapshot prefetched; LFS safetensors SHA256 verified. Remote resets were recovered with retrying curl, TLS verification intact. |
| `.venv/Scripts/python -m scripts.download_model` | Pinned pretrained model loaded and returned a real normalized (1,384) embedding. Repeated successfully with `SOLARI_OFFLINE=1`. |
| `... -m pytest -m 'not integration' -q` | Final separate offline run: 32 passed, 1 deselected. |
| `... -m pytest -m integration -q` | Real model run: 1 passed, 32 deselected. No mock embedding claim. |
| `SOLARI_OFFLINE=1` then `.venv/Scripts/python -m pytest -q` | Final combined suite after gate finalization: **33 passed**, one nonfatal Starlette/AnyIO deprecation warning. |
| `... -m evaluation.review_development` | Inspected development-only top component evidence; artifact `evaluation/development-evidence.json`. |
| `... -m evaluation.run --split development --output evaluation/development-initial-results.json` | Initial 0.25/0.50 gates measured. After review, semantic gate raised to 0.70 before held-out execution. |
| `... -m evaluation.run --split development --output evaluation/development-results.json` | Final 0.25/0.70 development metrics measured; keyword recall .9167, semantic/hybrid 1.0. All modes correctly rejected 3/3 negatives. |
| `... -m evaluation.run --split held_out --output evaluation/results.json` | All three modes measured with frozen gates; final latency rerun after browser servers stopped. See evaluation README for quality failures and exact results. |
| `npx playwright install chromium` (frontend) | Installed Chromium and headless shell, build 1194 (141.0.7390.37). |
| `npm run test:e2e` (frontend) | Final **4 passed**: real API/model/UI known-match and no-match; mobile overflow and reset; validation/backend failure; stale response suppression; mocked degraded health. Servers started/stopped by Playwright. |
| `git diff --exit-code HEAD -- case-study-1-support-ticket-similarity` | Passed: all original supplied materials unchanged. |
| `git diff --check` | Passed for tracked changes; Git warns about configured LF→CRLF conversion. New files were reviewed directly. |
| `.venv/Scripts/python -m scripts.package_submission` | Creates local ZIP; verifies required members, CRCs, SHA256 equality and excluded path components. Final artifact details are recorded in `PROJECT_STATUS.md` and `artifacts/manifest.json`. |

## Failures and recovery

- Initial npm 20.3.0 installation reported 24 vulnerabilities, including two critical. Updated Angular runtime/compiler to 20.3.34 and CLI/build to 20.3.40. The first update hit ERESOLVE against old exact peers; regenerated from a fresh tree, without force or legacy-peer bypass. Cleanup was rejected by execution policy; reversibly renamed generated directories/files instead. Ignored backups remain at `frontend/node_modules.previous` and `frontend/package-lock.previous.json`, excluded from the archive. Final npm audit is clean.
- Initial full pip process appeared stalled on the 204 MB Torch wheel. Stopped only verified task-owned pip processes, installed the lightweight dependencies, then downloaded the official wheel with curl and verified its SHA256 against PyPI release metadata. Installed the wheel and remaining dependencies, then reran the full manifest install and `pip check`. A parallel Invoke-WebRequest wheel download eventually succeeded too. Wheels/cache are excluded. The temporary no-dependencies installation reported absent Torch/regex until those packages were installed; final environment is consistent.
- A premature test run failed collection because installation was incomplete. After install, four validation assertions failed because the test searched for substring `input`, also present in the intentional `invalid_input` error code. The corrected test checks absence of actual private input and raw input keys; all subsequent tests passed.
- Hugging Face requests initially encountered remote connection resets. Retry succeeded without disabling TLS. Windows cache symlink warning is nonfatal; copied files work offline.
- First browser run had 3 passes and 1 failure: it assumed hybrid would abstain on held-out Snowflake. Actual retrieval falsely accepted HubSpot. Kept frozen gates and documented the quality failure; changed the UI no-match fixture to an existing development negative. Final 4 tests passed, without altering held-out labels or thresholds.
- Diagnostic HEAD to the bare PyPI file host returned 404 (no artifact path). Artifact-specific HEAD returned 200 with the expected wheel length; no dependency issue remained.

## Practical limits

Actual browser checks are Chromium only, with a mobile viewport rather than a physical phone. Desktop/mobile screenshots in `artifacts/` were visually inspected. No production load, security, accessibility certification, independent human label review, or original sandbox runtime verification is claimed. No commit, push, upload, or submission was made.
