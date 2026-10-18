# solari-ticket-assistant

Solari Analytics Support Ticket Similarity Assistant: an Angular workspace and FastAPI service that retrieve historical issues and their **original resolution notes** using keyword, semantic, or hybrid search. No generated fixes, database, GPU, paid API, or model training.

## Windows PowerShell setup

Run commands from this repository root. No Conda or global npm packages are needed. Use two terminals to run the service and UI.

The supplied target has Python 3.10.0 / pip 21.2.3 and Node 20.10.0 / npm 10.2.3. Python dependencies declare Python 3.10 support. The installed development host is Windows with Python 3.11.9, Node 22.23.2, npm 10.9.8, Git 2.50.1.windows.1. **The original target sandbox has not been executed**; do not confuse these environments.

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

Direct Python dependencies: FastAPI 0.115.8, Uvicorn 0.34.0, Pydantic 2.10.6, NumPy 1.26.4, scikit-learn 1.6.1, Sentence Transformers 3.4.1, Transformers 4.48.3, Torch 2.6.0, HTTPX 0.28.1 and pytest 8.3.4. Reasons: Python 3.10-compatible releases, stable typed API/testing support, and a small reproducible CPU retrieval stack. `requirements-resolved.txt` records the actual development environment, including transitive versions; prefer `requirements.txt` for cross-Python installation because the resolved development snapshot may include Python 3.11-only transitives.

Frontend exact versions: Angular runtime/compiler 20.3.34, CLI/build 20.3.40, TypeScript 5.9.2, RxJS 7.8.2, tslib 2.8.1, Playwright 1.56.1. Angular 20 is supported at implementation time; patch releases addressed audit findings from the initial 20.3.0 toolchain. `frontend/package-lock.json` is the reproducible frontend lockfile. No system Node installation is replaced.

Official compatibility references: [Angular versions](https://angular.dev/reference/versions), [Angular support schedule](https://angular.dev/reference/releases), [Sentence Transformers release metadata](https://pypi.org/pypi/sentence-transformers/3.4.1/json), [FastAPI release metadata](https://pypi.org/pypi/fastapi/0.115.8/json), [MiniLM model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).

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

Known evaluation failures: hybrid/keyword suggest HubSpot authentication for the supplied Snowflake example, and password rejection for the missing-reset-email example. Semantic abstains on Snowflake but misses the held-out HTTP 429 match. These heuristic limitations are documented, not fixed by tuning on held-out cases. For a clear no-match demonstration, try “Office delivery” with “A parcel containing a desk lamp was delivered to the wrong building.”

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

## Model and cache

Model: `sentence-transformers/all-MiniLM-L6-v2`, immutable revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, CPU, normalized 384-dimensional vectors. The model card describes 256-wordpiece truncation. Historical embeddings live in `.cache/embeddings/`; the key contains a dataset content hash, model ID/revision and preprocessing version. Cache reads use NumPy with `allow_pickle=False`. The model loads once on startup, and historical indexes are not rebuilt per request.

A fresh clone requires dependency and model downloads; a ZIP excludes model weights. After pre-download, `SOLARI_OFFLINE=1` reuses local files. To demo without the model, set `$env:SOLARI_KEYWORD_ONLY='1'` before starting the backend; health/UI explicitly show degradation. To restore semantic capabilities, remove that variable (`Remove-Item Env:SOLARI_KEYWORD_ONLY`), pre-download the model, and restart. No-match thresholds are heuristics; cosine and fusion values are not probabilities. See evaluation documentation for development decisions and measured limitations.

## Checks and evaluation

```powershell
./.venv/Scripts/python.exe -m pytest -m 'not integration' -q
$env:SOLARI_OFFLINE = '1'
./.venv/Scripts/python.exe -m pytest -m integration -q
./.venv/Scripts/python.exe -m evaluation.run --split development --output evaluation/development-results.json
./.venv/Scripts/python.exe -m evaluation.run --split held_out --output evaluation/results.json
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

See [evaluation/README.md](evaluation/README.md) for actual metrics, denominators, hardware and warm latency. Machine-readable results are in `evaluation/results.json`. The synthetic sample and AI-assisted labels do not establish production accuracy or throughput. See `PROJECT_STATUS.md` for checks actually run and their outcomes; a command listed above is not itself a claim that it passed.

Actual local validation: **33 Python tests and 4 Chromium browser tests passed**, along with frontend type checking/build, `pip check`, and a clean npm audit. [Detailed validation record](docs/VALIDATION.md) includes recovered failures and verification limits. Screenshots in ignored `artifacts/` were visually inspected; they are excluded from the source ZIP.

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
| Shared continuity | `AGENTS.md`, `.github/copilot-instructions.md`, `PROJECT_STATUS.md` |

## Limitations and troubleshooting

- **Model unavailable:** run the download command with network access, then restart. Health exposes a safe message. Keyword mode remains available explicitly. Windows may warn about Hugging Face symlinks; the cache can work with copied files at greater disk cost.
- **Invalid data:** startup fails rather than silently dropping records. Restore supplied JSON and inspect the local validation error; data is static and changes require restart.
- **Cannot reach API:** confirm both ports, backend readiness, proxy configuration, and that the browser uses port 4200. An unrelated process on either port must be handled separately.
- **npm engine errors:** confirm the project-local Node folder leads PATH in this terminal. Do not install latest Angular blindly or force incompatible peers.
- **Download or certificate failure:** respect network policies; provision dependencies/model using an approved connected environment. Do not disable TLS verification.
- **Scope:** English synthetic tickets, single workspace, no auth/tenant isolation, 256-wordpiece model truncation, in-memory/static indexes, heuristic abstention, no load/security/production certification. Real customer use requires access controls and isolation. Read `SOLUTION_DESIGN.md` for next investments.
