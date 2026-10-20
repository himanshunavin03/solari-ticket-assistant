# Final submission validation

Validated October 19, 2026 (America/Edmonton), from repository HEAD `58718664920bf90f80baeca357938219bec2152e` plus local finalization changes. Application retrieval code, model, dependency manifests, original supplied data and earlier JSON evaluation artifacts were not changed by finalization.

## Actual outcomes

| Check | Actual result |
| --- | --- |
| Full backend suite, Python 3.11.9 | **83 passed, 0 failed, 0 skipped**,22.62 s; one nonfatal Starlette/AnyIO deprecation warning. |
| Full backend suite, Python 3.10.11 | **83 passed, 0 failed, 0 skipped**,22.97 s; same warning. Original Launchpad 3.10.0 was not run. |
| Frontend typecheck / production build | Both passed; initial 177.49 kB, estimated transfer 49.47 kB. |
| Repository Playwright/Chromium suite | **9 passed, 0 failed, 0 skipped**,38.5 s. Real full and keyword-only APIs, chart/billing/429, exact informal query, misleading examples, short contradictions, no history, failures, stale responses/mobile and Swagger fallback. |
| Four supplied examples, actual HTTP API | **12 requests passed**, zero hybrid expectation failures. Original notes and unverified labels checked. Exact inputs/scores: evaluation/SAMPLE_TICKET_RESULTS.md and sample-ticket-results.json. |
| Focused packaging/dependency checks | Explicit66-file list; all existing backend/browser test files retained. ZIP CRC/membership/source SHA256, exclusions, all shipped Markdown links and project Python imports passed. |
| Extracted ZIP frontend install | `npm ci`:411 packages, zero audit findings; lockfile install into the fresh extraction, using existing npm cache where available. |
| Extracted ZIP preflight | Passed actual cached offline (1,384) embedding, HTTP ready/all three capabilities / 40 tickets, pip check/npm ls, typecheck/build. Passed under PowerShell 7.6.7 and Windows PowerShell 5.1.26100.9711. Owned temporary servers stopped. |
| Extracted ZIP backend suite | **83 passed, 0 failed, 0 skipped**,22.41 s using existing Python 3.11.9 environment, importing application code from the extracted directory. |
| Extracted ZIP Playwright suite | **9 passed, 0 failed, 0 skipped**,37.3 s; starts extracted backend/frontend/keyword-only backend. Includes real Swagger Try-it-out search. |
| Extracted sample/API flow | Another12direct API and12Angular-proxied sample requests passed; docsHTTP 200. All3capabilities ready. |
| Extracted baseline/current evaluators | Both completed. All non-timing relevance/error metrics and per-case expected/displayed/related IDs and outcomes matched retained reports across all four splits and three modes. |
| Preservation/compile/whitespace | Original application/manifests/data/JSON diff unchanged; Python compileall and git diff whitespace checks passed. |

No model/browser check was skipped or replaced with a mock. Node color and Angular prebundling notices were nonfatal. One audit command initially passed a literal Windows wildcard to rg; it was corrected to `-g '*.py'` and rerun successfully. No application test/build failure remained. Earlier test-first failures belong to their historical revisions and are not described as successful checks here.

## Extraction and resource reuse

The 66-file ZIP was extracted into a newly created temporary directory. Every member was compared byte-for-byte with source; session instructions/status, prompts, obsolete experiments, environments, node_modules, runtimes, weights, caches, logs and generated outputs were absent. Local links/import dependencies were audited; negative package tests mention excluded files only to assert their absence. Legacy refusal scripts protect historical paths without loading omitted experiments. Optional PDF was absent, not substituted.

This was **not a completely clean installation**. The existing Python 3.11.9 venv and installed packages, project-local Node 22.23.2 / npm 10.9.8 and installed Chromium were reused. Model files were copied into the extraction's own `.cache/models`; embeddings were constructed/checked there. Frontend dependencies were freshly installed into extracted `node_modules` with npm ci. Application imports were explicitly confirmed to resolve inside the extracted tree. Interpreter/runtime paths were passed through supported parameters/environment variables rather than encoded into shipped source. No fresh Python dependency download/venv creation, Node bootstrap download or Chromium download was performed for this validation.

The extracted run exercised the documented preflight, model verification, tests and backend/frontend commands through the same CLI entry points. It used an explicit existing interpreter instead of creating `.venv`. Independent source location, copied model cache and the reproduced evaluations show no dependency on the original working directory. Timings overlapped development checks and are not throughput, SLA or controlled performance comparisons.

## Reproduce

Follow README Quick Start for fresh setup and docs/LAUNCHPAD_RUNBOOK.md for diagnostics. From project root:

```powershell
$env:SOLARI_OFFLINE = '1'
./scripts/preflight.ps1
./.venv/Scripts/python.exe -m pytest -q
# After starting FastAPI:
./.venv/Scripts/python.exe -m scripts.verify_samples
# Stop manual servers before browser tests:
$env:SOLARI_TEST_PYTHON = '.venv/Scripts/python.exe'
Push-Location frontend
npm run typecheck
npm run build
npm run test:e2e
Pop-Location
```

For comparison reproduction, use the two timestamped baseline/current commands in evaluation/README.md. Existing reports are protected. Packaging command: `python -m scripts.package_submission`; actual member and hash lists are written under artifacts. The final archive is regenerated after documentation updates; unchanged tested executable/test/data files are checked byte-for-byte against the verified extraction, and final ZIP membership/CRC/links are rechecked.

## Remaining manual checks and PDF

Original Launchpad Python 3.10.0 / pip 21.2.3 / Node 20.10.0 / npm 10.2.3 / Git 2.43.0.windows.1 remains unverified. Angular requires the additional local Node route; actual Launchpad download/execution restrictions must be checked there. Blocked dependencies/model/browser downloads are blocked checks, never passes. Swagger UI uses CDN assets; JSON/OpenAPI and PowerShell HTTP remain alternatives if those assets are blocked.

No final PDF was found in the project, parent project directory or supplied local attachments. Intended destination: **docs/SOLUTION_DESIGN.pdf**. Add the real reviewed PDF and regenerate/inspect the ZIP if required; no fake PDF is generated. Because the separate PDF was unavailable, no line-by-line discrepancy comparison was possible. Ensure it matches current unverified-applicability wording, chart/billing versus reset-email/Snowflake sample behavior, v6 short-request handling, conservative keyword recall and synthetic-label limitations. The Markdown design is the authoritative implementation description.

Physical-device/other-browser review, independent representative labels, production security/access isolation/load and recipient deadline timezone remain manual. No commit, push, upload or submission was performed. All validation-owned servers were stopped; start the application using README when needed.
