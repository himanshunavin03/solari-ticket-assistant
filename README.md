# solari-ticket-assistant

Solari Analytics Support Ticket Similarity Assistant: an Angular workspace and FastAPI service that retrieve historical issues and their **original resolution notes** using keyword, semantic, or hybrid search. No generated fixes, database, GPU, paid API, or model training.

## Windows PowerShell setup

Run commands from this repository root. No Conda or global npm packages are needed. Use two terminals to run the service and UI.

The supplied Launchpad target has Python 3.10.0 / pip 21.2.3, Node 20.10.0 / npm 10.2.3 and Git 2.43.0.windows.1, CPU only. Backend dependencies were installed and **46 tests passed on actual Windows Python 3.10.11**, in a separate project-local `.venv310`, as well as Python 3.11.9. Node 22.23.2/npm 10.9.8/Git 2.50.1.windows.1 were used here. **Original Launchpad/Python 3.10.0 was not executed.** Patch/runtime and sandbox restrictions may differ; run preflight there before submission.

Angular 20.3 requires Node `^20.19.0 || ^22.12.0 || ^24.0.0` and TypeScript `>=5.8 <6`. The original Node 20.10.0 is insufficient. The following verified-checksum bootstrap downloads Node 22.23.2 to `.runtime/`, leaving the system installation intact. It requires network access, Windows x64, and permission to run PowerShell scripts. If policy blocks scripts, use an organization-approved execution method rather than changing machine policy.

```powershell
# Optional on this development host; required when using the supplied Node 20.10.0.
./scripts/bootstrap-node.ps1
$env:Path = "$(Get-Location)\.runtime\node-v22.23.2-win-x64;" + $env:Path
node --version
npm --version

python --version
python -m venv .venv
./.venv/Scripts/python.exe -m pip install --upgrade pip==25.0.1
./.venv/Scripts/python.exe -m pip install -r requirements.txt
./.venv/Scripts/python.exe -m pip check

Push-Location frontend
npm ci
Pop-Location

# Downloads the pinned model into .cache/models and verifies a real embedding.
./.venv/Scripts/python.exe -m scripts.download_model
```

Direct Python dependencies: FastAPI 0.115.8, Uvicorn 0.34.0, Pydantic 2.10.6, NumPy 1.26.4, scikit-learn 1.6.1, Sentence Transformers 3.4.1, Transformers 4.48.3, Torch 2.6.0, HTTPX 0.28.1 and pytest 8.3.4. Reasons: Python 3.10-compatible releases, stable typed API/testing support, and a small reproducible CPU retrieval stack. `requirements-py310-resolved.txt` records the actual tested Python 3.10.11 environment (including SciPy 1.15.3); `requirements-resolved.txt` preserves the original Python 3.11 snapshot. Use `requirements.txt` for cross-version setup; use the corresponding resolved snapshot only when reproducing its tested interpreter environment. The virtual-environment pip upgrade leaves the supplied system pip unchanged.

Frontend exact versions: Angular runtime/compiler 20.3.34, CLI/build 20.3.40, TypeScript 5.9.2, RxJS 7.8.2, tslib 2.8.1, Playwright 1.56.1. Angular 20 is supported at implementation time; patch releases addressed audit findings from the initial 20.3.0 toolchain. `frontend/package-lock.json` is the reproducible frontend lockfile. No system Node installation is replaced.

Official compatibility references: [Angular versions](https://angular.dev/reference/versions), [Angular support schedule](https://angular.dev/reference/releases), [Sentence Transformers release metadata](https://pypi.org/pypi/sentence-transformers/3.4.1/json), [FastAPI release metadata](https://pypi.org/pypi/fastapi/0.115.8/json), [MiniLM model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).

The frontend **requires the additional compatible Node runtime**; the original Node 20.10.0 cannot build this Angular application. No Angular downgrade, Conda, or silent system runtime replacement is used. Launchpad installation restrictions cannot be checked from this machine: no actual Launchpad download failure is claimed. If bootstrap fails there, retain the exact URL/HTTP/TLS or execution-policy error and use an approved provisioned runtime; do not disable TLS or substitute an incompatible Node.

After setup, run the short Windows preflight:

```powershell
$env:SOLARI_OFFLINE = '1'
./scripts/preflight.ps1
# On this developer machine's separate compatibility environment:
# ./scripts/preflight.ps1 -Python ./.venv310/Scripts/python.exe
```

It reports active shell Python/Node and selected backend Python, checks exact direct Python packages plus `pip check`/`npm ls`, generates a real offline embedding, starts an owned temporary backend to check readiness/all capabilities, stops it, then typechecks/builds the frontend. It installs nothing and leaves no server running. Run dependency/model setup first. A failed check exits nonzero with its cause; backend startup details are in `.cache/preflight-backend.log`.

## Run

Terminal 1, from repository root:

```powershell
# After a successful pre-download, prohibit further model network access.
$env:SOLARI_OFFLINE = '1'
./.venv/Scripts/python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --no-access-log
```

Terminal 2, from repository root (set the local Node PATH here too if needed):

```powershell
$env:Path = "$(Get-Location)\.runtime\node-v22.23.2-win-x64;" + $env:Path
Push-Location frontend
npm start
```

Open `http://127.0.0.1:4200`. Stop both servers with Ctrl+C. The frontend dev proxy forwards `/api` to port 8000. Build output alone needs hosting with equivalent `/api` forwarding; the dev server is the documented local demo path.

Select “Getting charged twice this month” for a known match. Search defaults to hybrid and three suggestions. Inspect original descriptions or relevance details when needed. Clear/reset and edits invalidate previous requests. Resolution notes are precedent to investigate, not a promise that the same fix applies.

The reviewed revision's OR gate incorrectly presented HubSpot authentication for Snowflake and password rejection for missing reset email. The current hybrid policy withholds those original examples' resolutions and still accepts duplicate billing and HTTP 429. It separately shows **potentially related history without resolution notes**. Keyword mode, including degraded operation, provides this metadata-only context and cannot endorse resolution evidence. An unrelated parcel query is no longer the only no-match browser test.

This remains a heuristic: newly worded missing-mail and SMS password-recovery queries were falsely accepted during intermediate evaluation; a broad rate-limit paraphrase and some valid multi-issue context are rejected. Final release evaluation also has one false rejection. See evaluation documentation for all failures; neither “supported” nor any score is a correctness guarantee.

## API

Interactive schemas: `http://127.0.0.1:8000/docs`.

| Endpoint | Behavior |
| --- | --- |
| `GET /api/health` | Readiness, active capabilities, ticket count, model ID/revision; `degraded` means keyword-only. |
| `GET /api/examples` | Four supplied examples, unchanged. |
| `POST /api/search` | Subject (1–300 chars), description (1–10,000), mode (`keyword`, `semantic`, `hybrid`), top_k integer 1–10 (default 3). Whitespace-only fields rejected. |

```powershell
$body = @{subject='Billed twice'; description='Two identical charges on my card for one subscription month'; mode='hybrid'; top_k=3} | ConvertTo-Json
Invoke-RestMethod http://127.0.0.1:8000/api/search -Method Post -ContentType application/json -Body $body
```

`200` with `outcome=no_reliable_match` is successful abstention. `422` returns `error.code=invalid_input`; `503` indicates service/capability unavailability. Semantic/hybrid never silently fall back. Keyword requests carry `degraded=true` if the model is unavailable. CORS is limited to localhost/127.0.0.1 on frontend port 4200. The application does not log incoming ticket text by default; `--no-access-log` also suppresses access logging in the documented command.

`matches` contains only heuristically supported historical resolutions. `related_history` has ticket ID/subject/category/tags and scores/reason, **no resolution text**; it may be nonempty with `no_reliable_match`. Both lists respect top_k independently. Technical details expose whole-ticket cosine, weakest clause coverage, RRF and the evidence reason. Keyword-only results have no supported matches by design.

## Model and cache

Model: `sentence-transformers/all-MiniLM-L6-v2`, immutable revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, CPU, normalized 384-dimensional vectors. The model card describes 256-wordpiece truncation. Historical embeddings live in `.cache/embeddings/`; the key contains a dataset content hash, model ID/revision and preprocessing version. Cache reads use NumPy with `allow_pickle=False`. The model loads once on startup, and historical indexes are not rebuilt per request.

Current evidence policy (`backend/evidence.py`): overall cosine ≥0.65 plus every retained description clause covered at ≥0.45 by a candidate subject/description clause, **or** a shared generic numeric technical identifier with overall and identifier-clause cosines ≥0.60. These are additional symptom/identifier signals, not keyword OR semantic acceptance. Coordination/contrast splitting is generic English, with four-word minimum fragments; more than eight query clauses abstains instead of silently approving truncated context. The revised cache includes these historical clauses and a new preprocessing version; original cache entries are invalidated. More clauses increase CPU latency; no extra model or dependency is introduced.

A fresh clone requires dependency and model downloads; a ZIP excludes model weights. After pre-download, `SOLARI_OFFLINE=1` reuses local files. To demo without the model, set `$env:SOLARI_KEYWORD_ONLY='1'` before starting the backend; health/UI explicitly show degradation. To restore semantic capabilities, remove that variable (`Remove-Item Env:SOLARI_KEYWORD_ONLY`), pre-download the model, and restart. No-match thresholds are heuristics; cosine and fusion values are not probabilities. See evaluation documentation for development decisions and measured limitations.

## Checks and evaluation

```powershell
./.venv/Scripts/python.exe -m pytest -m 'not integration' -q
$env:SOLARI_OFFLINE = '1'
./.venv/Scripts/python.exe -m pytest -m integration -q
./.venv/Scripts/python.exe -m evaluation.compare_revision --split development
./.venv/Scripts/python.exe -m evaluation.compare_revision --split regression
./.venv/Scripts/python.exe -m evaluation.compare_revision --split release
Push-Location frontend
npm run typecheck
npm run build
npm audit --audit-level=low
npx playwright install chromium
# Stop existing port-8000/4200 servers first; Playwright starts/stops its own.
npm run test:e2e
Pop-Location
```

Offline tests cover data/request validation, ranking/ties, technical tokens, zero vectors, no-match, safe cache reuse/invalidation/corruption, unavailable semantics, API contracts/errors, and CORS. The integration test uses the actual pinned pretrained model. Browser tests cover real known-match/no-match flow plus validation, request failure, stale responses, mobile width, and a simulated degraded capability state. Mocks in cache/browser tests are not evidence of real semantic quality.

See [evaluation/README.md](evaluation/README.md) for actual before/after metrics, denominators, hardware and warm latency. Current results are `evaluation/release-results.json` and `release-regression-results.json`. Original `evaluation/results.json` is preserved historical evidence; its exposed “held_out” split is now a **regression benchmark**, not an untouched test. Intermediate fresh sets became exposed through iteration; `release-cases.json` was frozen before scoring the final policy. AI-authored synthetic labels remain unreviewed by independent support agents.

Actual validation: **46 tests passed on Python 3.10.11 and 3.11.9**, and **6 Chromium browser tests passed** against the Python 3.10.11 API. Real model, HTTP preflight, frontend typecheck/build, dependency checks and npm audit passed. [Detailed validation record](docs/VALIDATION.md) records recovered failures and limits. Original October 17 counts are historical. Screenshots and build outputs in ignored directories are excluded from the source ZIP.

## Packaging and handoff

```powershell
./.venv/Scripts/python.exe -m scripts.package_submission
Get-FileHash artifacts/solari-ticket-assistant.zip -Algorithm SHA256
```

The script creates `artifacts/solari-ticket-assistant.zip` using a source allowlist, stable entry ordering/timestamps, and verifies CRCs, membership and SHA256 content hashes against source. `artifacts/manifest.json` records entries. No Git metadata, virtual environment, node_modules, model weights, caches, secrets, metadata forks, or builds are included. The archive is created locally only. Inspect it and verify on the target sandbox before manually submitting. Deadline: Tuesday, October 20, 2026 EOD, timezone unspecified; confirm the recipient's timezone before delivery.

| Requirement | Artifact |
| --- | --- |
| Assumptions, architecture, trade-offs | `SOLUTION_DESIGN.md` |
| Validated data, TF-IDF, semantics, RRF, cache, abstention | `backend/retrieval.py` |
| Health, examples, typed search/errors | `backend/app.py` |
| Agent UI, evidence, accessibility/states | `frontend/src/` |
| Offline/API and real-model tests | `tests/` |
| Browser smoke and stale-response test | `frontend/e2e/` |
| Split labels, evaluation metrics/results | `evaluation/` |
| Demonstration and AI assistance | `docs/DEMO_GUIDE.md`, `docs/AI_ASSISTANCE.md` |
| Reproducible archive | `scripts/package_submission.py` |
| Windows runtime/dependency/model/readiness/build preflight | `scripts/preflight.ps1`, `scripts/preflight.py` |
| Shared continuity | `AGENTS.md`, `.github/copilot-instructions.md`, `PROJECT_STATUS.md` |

## Limitations and troubleshooting

- **Model unavailable:** run the download command with network access, then restart. Health exposes a safe message. Keyword mode remains available explicitly. Windows may warn about Hugging Face symlinks; the cache can work with copied files at greater disk cost.
- **Invalid data:** startup fails rather than silently dropping records. Restore supplied JSON and inspect the local validation error; data is static and changes require restart.
- **Cannot reach API:** confirm both ports, backend readiness, proxy configuration, and that the browser uses port 4200. An unrelated process on either port must be handled separately.
- **npm engine errors:** confirm the project-local Node folder leads PATH in this terminal. Do not install latest Angular blindly or force incompatible peers.
- **Download or certificate failure:** respect network policies; provision dependencies/model using an approved connected environment. Do not disable TLS verification.
- **Scope:** English synthetic tickets, single workspace, no auth/tenant isolation, 256-wordpiece model truncation, in-memory/static indexes, heuristic abstention, no load/security/production certification. Real customer use requires access controls and isolation. Read `SOLUTION_DESIGN.md` for next investments.
