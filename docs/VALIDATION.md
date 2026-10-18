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
