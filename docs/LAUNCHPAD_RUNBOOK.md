# Windows PowerShell Launchpad runbook

Start in the extracted project or repository root. For a Git checkout, inspect the revision and local changes before pulling; a ZIP does not contain Git metadata.

Tested here: Windows Python **3.10.11** and **3.11.9**, venv pip **25.0.1**, Node **22.23.2**, npm **10.9.8**, Windows PowerShell **5.1.26100.9711** and PowerShell **7.6.7**, Git **2.50.1.windows.1**. This is **not** verification inside original Launchpad (Python 3.10.0 / pip 21.2.3 / Node 20.10.0 / npm 10.2.3 / Git 2.43.0.windows.1). Angular requires the additional local Node runtime; system runtimes stay intact.

1. **Pull latest code**, after preserving/reconciling local changes:

   ```powershell
   git status --short
   git pull --ff-only
   git log -1 --oneline
   Get-Content README.md
   ```

   Skip Git commands for an extracted ZIP. Expected: `backend/evidence.py` and `scripts/preflight.ps1` are present. Never reset/overwrite local work to force a pull.

2. **Bootstrap local Node and set this terminal's PATH**:

   ```powershell
   ./scripts/bootstrap-node.ps1
   $env:Path = (Join-Path (Get-Location) '.runtime/node-v22.23.2-win-x64') + ';' + $env:Path
   Get-Command node
   node --version
   npm --version
   ```

   Expected: `.runtime` executable, `v22.23.2`, npm `10.9.8`. Fresh downloads are checked against official SHA256. Node 20.10.0 cannot build this Angular app. Repeat PATH selection in each new frontend terminal; no system installation is replaced.

3. **Create Python venv and install dependencies** in a fresh environment; preserve any existing environment you still need:

   ```powershell
   python --version
   python -m venv .venv
   ./.venv/Scripts/python.exe --version
   ./.venv/Scripts/python.exe -m pip install --upgrade pip==25.0.1
   ./.venv/Scripts/python.exe -m pip install -r requirements.txt
   ./.venv/Scripts/python.exe -m pip check
   ```

   Expected: selected Python >=3.10 and no broken requirements. Original Launchpad should show 3.10.0, which still needs verification there; actual local compatibility testing used 3.10.11. Only venv pip is upgraded. `.venv310` is this developer machine's separate compatibility environment, not a required Launchpad directory. `requirements-py310-resolved.txt` records tested 3.10.11 transitives; setup uses `requirements.txt`.

4. **Install the frontend lockfile**:

   ```powershell
   Push-Location frontend
   npm ci
   Pop-Location
   ```

   Expected: successful install without force/legacy-peer flags. Engine errors mean the wrong Node leads PATH; repeat step 2 rather than downgrading Angular.

5. **Download and verify the pinned model**:

   ```powershell
   Remove-Item Env:SOLARI_OFFLINE -ErrorAction SilentlyContinue
   ./.venv/Scripts/python.exe -m scripts.download_model
   $env:SOLARI_OFFLINE = '1'
   ```

   Expected: `sentence-transformers/all-MiniLM-L6-v2@1110a243fdf4706b3f48f1d95db1a4f5529b4d41: verified (1, 384)`. Fresh setup needs downloads; ZIP excludes weights. Offline reuse requires prior provisioning.

6. **Run preflight**:

   ```powershell
   Remove-Item Env:SOLARI_KEYWORD_ONLY -ErrorAction SilentlyContinue
   ./scripts/preflight.ps1
   ```

   Expected: versions/dependencies, real offline embedding, temporary HTTP `ready` with keyword/semantic/hybrid, frontend typecheck/build, `PREFLIGHT PASSED`. Its owned server stops automatically. On failure inspect `Get-Content .cache/preflight-backend.log`. It installs nothing.

7. **Run backend tests, data inspection and current regression**:

   ```powershell
   $env:SOLARI_OFFLINE = '1'
   ./.venv/Scripts/python.exe -m pytest -q
   ./.venv/Scripts/python.exe -m scripts.inspect_data
   # With the backend running (step 8): python -m scripts.verify_samples
   ./.venv/Scripts/python.exe -m evaluation.review_informal --output "informal-check-$(Get-Date -Format yyyyMMdd-HHmmss)-results.json"
   ```

   Expected: all shipped tests pass (final counts are recorded in SUBMISSION_VALIDATION.md) for current source; a nonfatal dependency deprecation warning was observed here. Inspection: 40 valid records, no duplicate-content groups in supplied data. Repeats would be reported, never deleted. Current regression uses **unverified historical precedent**, not old supported-resolution semantics, and writes a new timestamped informal report without overwriting earlier results.

   Optional browser checks **before starting manual servers**:

   ```powershell
   $env:SOLARI_TEST_PYTHON = '.venv/Scripts/python.exe'
   Push-Location frontend
   npx playwright install chromium
   npm run test:e2e
   Pop-Location
   ```

   Expected: 9 passing browser tests; ports 8000, 8001 and 4200 free beforehand. Tests start/stop real full and keyword-only backends. A blocked browser download means a blocked check, not a Launchpad pass.

8. **Start separate terminals**, each initially at repository root.

   Terminal A:

   ```powershell
   $env:SOLARI_OFFLINE = '1'
   ./.venv/Scripts/python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --no-access-log
   ```

   Terminal B:

   ```powershell
   $env:Path = (Join-Path (Get-Location) '.runtime/node-v22.23.2-win-x64') + ';' + $env:Path
   Push-Location frontend
   npm start
   ```

   Expected: UI `http://127.0.0.1:4200`; API schema `http://127.0.0.1:8000/docs`. Ctrl+C stops each server; run `Pop-Location` in B after stopping to return to root.

9. **Manual acceptance checklist**:

   - Supplied empty-chart example in hybrid: T-1201 original notes, applicability unverified.
   - Duplicate-billing example in hybrid and keyword: original notes shown with **Applicability unverified**, never a confirmed fix.
   - Subject `API returns 429 rate limit`, description `Integration started receiving 429 errors`: historical rate-limit precedent, applicability unverified.
   - Supplied Snowflake and missing-reset-email examples: **Related history only**, no original resolution notes, in keyword/hybrid.
   - Subject `Password reset issue`, description `The customer completed the password reset successfully but email never arrives.`: short failure retained, reset-rejection resolution withheld.
   - Unrelated office-parcel query: **No relevant history**. Blank input: validation. Clear/edit/new search: no stale results.
   - Stop backend, search: service error rather than no-history. Restart afterward.
   - For actual degradation: stop A, set `$env:SOLARI_KEYWORD_ONLY='1'`, rerun its backend command and reload UI. Keyword billing still shows unverified precedent; selecting hybrid returns capability unavailable. Restore by stopping, removing `Env:SOLARI_KEYWORD_ONLY`, restarting.

   These are exposed regressions, not production accuracy evidence. Conservative keyword matching still misses many valid paraphrases; model mechanism errors remain possible.

10. **Generate and inspect ZIP**, from root after stopping manual servers:

    ```powershell
    ./.venv/Scripts/python.exe -m scripts.package_submission
    ./.venv/Scripts/python.exe -m zipfile -t artifacts/solari-ticket-assistant.zip
    ./.venv/Scripts/python.exe -m zipfile -l artifacts/solari-ticket-assistant.zip
    Get-FileHash artifacts/solari-ticket-assistant.zip -Algorithm SHA256
    Get-Content artifacts/manifest.json
    ```

    Expected: required members, CRCs and source SHA256 verified; ZIP test `Done testing`. Inspect the explicit list in `artifacts/included-files.txt`. Session instructions/status, internal prompts, superseded experiments and generated environments/caches/builds are excluded. The PDF is optional at `docs/SOLUTION_DESIGN.pdf`; add the final reviewed PDF and regenerate if supplied. Creation is local, not submission. Confirm the recipient timezone for **October 20, 2026 EOD**, review limitations, then submit manually.

## Troubleshooting

- **Wrong runtime:** check `Get-Command node`, `node --version`, and selected `.venv/Scripts/python.exe --version`. Reapply local Node PATH in the same terminal before npm. Never report the 3.10.11 host tests as original 3.10.0 sandbox validation.
- **Blocked downloads:** retain exact URL/HTTP/TLS/proxy/execution errors; use an approved environment to provision exact dependencies/runtime/model. Do not disable TLS or substitute latest packages. Optional retrying official-source `scripts/prefetch-model.ps1` can prefetch; always rerun Python model verification afterward. Launchpad restrictions have not been observed from this development host.
- **Script policy:** use an organization-approved execution route; do not silently change machine policy. Bootstrap supports basic parsing on Windows PowerShell 5.1.
- **Offline model missing:** clear `SOLARI_OFFLINE`, provision through step 5, re-enable offline and restart. Windows symlink warnings may be nonfatal; copied caches were tested.
- **Readiness/build failure:** inspect preflight log and exact pip/npm errors. Handle only your own port-conflicting processes. Dev proxy expects port 8000; build files alone need equivalent API forwarding.
