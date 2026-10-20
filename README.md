# solari-ticket-assistant

Solari Analytics support workspace: enter a subject and description to retrieve **historical precedent for agent review**, including original resolution notes when sufficiently relevant. **Applicability is unverified in every mode**; retrieved history is not a confirmed root cause or fix. Weak/conflicting history is separate and contains no resolution notes. No generated answers, training, paid API, database, GPU or Conda.

## Launchpad setup and run

Follow the [numbered Windows PowerShell runbook](docs/LAUNCHPAD_RUNBOOK.md): pull/transfer the intended code, bootstrap local Node, create venv/install dependencies, npm ci, provision model, preflight, tests, two-terminal startup, manual acceptance, ZIP inspection. Current changes remain local until the user manually publishes/transfers them; no commit/push/upload/submission was performed.

Original Launchpad: Python **3.10.0**, pip **21.2.3**, Node **20.10.0**, npm **10.2.3**, Git **2.43.0.windows.1**, CPU only. **It has not been executed here.** Actual host testing used Windows Python **3.10.11** in `.venv310` and **3.11.9** in `.venv`, venv pip **25.0.1**, Node **22.23.2**, npm **10.9.8**, Git **2.50.1.windows.1**. Python patch/sandbox/network restrictions still need manual Launchpad validation.

Angular needs an **additional compatible Node runtime**: Node 20.10.0 is insufficient. `scripts/bootstrap-node.ps1` downloads SHA256-verified Node 22.23.2 into `.runtime/`, leaving system installations intact. It supports Windows PowerShell basic parsing. Select that folder first on PATH in each frontend terminal; do not downgrade Angular or replace system Node. See runbook troubleshooting for precise errors if provisioning is blocked.

After fresh setup, start from root:

```powershell
$env:SOLARI_OFFLINE = '1'
./scripts/preflight.ps1
./.venv/Scripts/python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --no-access-log
```

In another root terminal:

```powershell
$env:Path = (Join-Path (Get-Location) '.runtime/node-v22.23.2-win-x64') + ';' + $env:Path
Push-Location frontend
npm start
```

Open `http://127.0.0.1:4200`. Ctrl+C stops each server; `Pop-Location` returns the frontend terminal to root. The dev proxy forwards `/api` to backend port 8000. Static build hosting requires equivalent API forwarding. Locally, substitute `.venv310/Scripts/python.exe` and `./scripts/preflight.ps1 -Python ./.venv310/Scripts/python.exe` to use the actual 3.10.11 compatibility environment.

## Runtime/dependency choices

Unchanged direct pins: FastAPI **0.115.8**, Uvicorn **0.34.0**, Pydantic **2.10.6**, NumPy **1.26.4**, scikit-learn **1.6.1**, Sentence Transformers **3.4.1**, Transformers **4.48.3**, Torch **2.6.0** (tested CPU runtime 2.6.0+cpu), HTTPX **0.28.1**, pytest **8.3.4**. `requirements.txt` installs the Python-3.10-compatible CPU/API stack; `requirements-py310-resolved.txt` records actual 3.10.11 transitives, and `requirements-resolved.txt` preserves the earlier 3.11 snapshot. No dependency/model was added for these corrections.

Frontend: Angular runtime/compiler **20.3.34**, CLI/build **20.3.40**, TypeScript **5.9.2**, RxJS **7.8.2**, tslib **2.8.1**, Playwright **1.56.1**. `frontend/package-lock.json` remains the reproducible frontend lockfile; install with `npm ci`. Angular 20.3 requires newer Node and TypeScript >=5.8 <6. Official references: [Angular compatibility](https://angular.dev/reference/versions), [Python Windows runtimes](https://docs.python.org/3.10/using/windows.html), [Sentence Transformers metadata](https://pypi.org/pypi/sentence-transformers/3.4.1/json), [MiniLM model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).

## Retrieval and honest uncertainty

- TF-IDF indexes original subject plus description, preserves technical terms/numbers, and uses deterministic ID ties. Hybrid keeps positive-evidence RRF instead of adding incomparable raw scores.
- Preprocessing keeps **all nonempty alphanumeric clauses**, including `email never arrives`, `still fails`, `access denied` and negation. Punctuation-only fragments are ignored, internal identifier/version dots retained, and original displayed data never rewritten. More than eight query clauses abstains from displaying notes; short clauses count toward that limit.
- Keyword precedent requires overall TF-IDF cosine >=0.25 and **every retained clause** to have >=0.50 IDF-weighted meaningful-token coverage against historical clauses. Unknown terms remain in the denominator; negation/contractions are retained. Generic function-word filtering applies only to lexical coverage, not embeddings/display. This is conservative and misses paraphrases; it is not contradiction detection.
- Semantic/hybrid use the same MiniLM and previous overall/clause or technical-identifier heuristics with the corrected splitter. Keyword relevance is **not** OR-ed into semantic acceptance. Model similarity, numeric identifiers and clause overlap still do not establish root-cause agreement.
- Generic polite request framing is removed only for query scoring; its objects, symptoms, identifiers and negation remain. Short queries (2–12 distinct content tokens) have an additional conjunctive route: keyword >=.25, semantic >=.60, every clause >=.65 and lexical clause coverage >=.50. Global thresholds stay unchanged. [Measured informal-request correction](evaluation/INFORMAL_REVISION.md): hybrid Recall@3 .625→.875 on 8 exposed positives, zero note presentations on 10 confusing negatives; one informal 429 paraphrase still abstains.
- Every displayed original resolution is labeled **Applicability unverified**. Lower-relevance/conflicting candidates show metadata only. Even a clear duplicate-billing or 429 precedent must be checked against customer context.

Model: `sentence-transformers/all-MiniLM-L6-v2@1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, CPU, normalized 384-dimensional embeddings, loaded once. Historical whole-ticket/clause embeddings are safely cached as non-pickle NPY under `.cache/embeddings`; dataset/model/revision/preprocessing changes invalidate the cache. `informal-precedent-v6` invalidates the old short-clause cache. Individual embeddings still truncate at 256 wordpieces; this remains a limitation.

A fresh clone/ZIP needs dependency, Node and model provisioning. After `python -m scripts.download_model`, `SOLARI_OFFLINE=1` enables reuse. For actual keyword-only fallback set `SOLARI_KEYWORD_ONLY=1` before backend start: readiness reports degraded, keyword can still return unverified historical notes, and semantic/hybrid requests return 503. Remove that variable and restart after model provisioning to restore all modes.

## API outcomes (changed semantics)

Schema: `http://127.0.0.1:8000/docs`. Endpoints: `GET /api/health`, `GET /api/examples`, `POST /api/search`. Search requires subject 1–300 characters and description 1–10,000; whitespace-only rejected; mode keyword/semantic/hybrid; integer top_k 1–10, default 3.

| Response | Meaning |
| --- | --- |
| 200 `historical_precedents` | `matches` includes original resolutions for review, always `applicability=unverified`. |
| 200 `related_history_only` | No displayed resolution; `related_history` contains weak/conflicting metadata only. |
| 200 `no_relevant_history` | Neither relevant precedent nor related candidate retrieved. |
| 422 `error.code=invalid_input` | Input validation failure, not a no-match. |
| 503 `capability_unavailable` / `service_unavailable` | Service/model capability unavailable, not no relevant history. |

`result_semantics=historical-precedent-v1` replaces earlier matches/no_reliable_match and supported-resolution interpretation. `active_mode` states what actually ran; no silent semantic fallback. Both result lists respect top_k independently. Optional technical details expose ranking/coverage values, not accuracy percentages. CORS is restricted to localhost/127.0.0.1:4200. Default application logging does not include incoming ticket text.

```powershell
$body = @{subject='Duplicate charges'; description='Two identical monthly charges'; mode='keyword'; top_k=3} | ConvertTo-Json
Invoke-RestMethod http://127.0.0.1:8000/api/search -Method Post -ContentType application/json -Body $body
```

## Data quality

Required fields/types and unique IDs remain strict startup validation: malformed records are not silently dropped. `python -m scripts.inspect_data` also reports duplicate subject+description groups, using only whitespace collapse and casefold for **inspection**, never rewriting/deleting records. Repeated incidents can be legitimate. Current supplied data: **40 records; no duplicate-content groups** (`evaluation/data-quality-report.json`). No imputation, outlier removal or Isolation Forest. Negation, error codes, IDs, resolutions and original datasets are preserved.

## Checks, evaluation and limits

Actual current checks: **75 tests passed on Windows Python 3.10.11 and 3.11.9**, **7 Chromium browser tests passed** in the previous revision against actual full/keyword-only backends; its frontend typecheck/build also passed. Browser automation was not rerun for this backend-only correction; live API/proxy checks passed after restart. [Validation record](docs/VALIDATION.md) includes the initial 15 reproduced failures and recovery. Runbook contains exact commands. Browser tests cover billing/429, original misleading examples, short contradictory text, real degraded operation, no history, failure and stale responses.

`python -m evaluation.review_informal --output informal-local-results.json` writes a new current-definition report (choose an unused informal-*-results.json filename). The earlier v5 report is preserved and its writer now refuses v6. Previous release cases and all earlier inspected cases are now **exposed regression**, not untouched tests. Every existing evaluation artifact is preserved. Earlier supported/verified-resolution-style metrics and current **displayed historical precedent relevance** are not equivalent; do not compare their percentages as a calibrated acceptance improvement. Legacy evaluators refuse to overwrite old reports under new semantics.

Current conservative keyword workflow returns correct billing/429 notes, but recalls only 2/8 original and 3/8 prior-release positives; many valid paraphrases remain related-only. Semantic/hybrid scores on these small exposed sets are not production accuracy. New targeted tests show keeping the missing-email clause changes the actual-model result, but retaining text alone does not prove retrieval correctness. AI-authored synthetic labels and other mechanism/negation/identifier risks still require independent support-agent review. See [evaluation details](evaluation/README.md), [design](SOLUTION_DESIGN.md), [demo guide](docs/DEMO_GUIDE.md), and [AI assistance](docs/AI_ASSISTANCE.md).

## Packaging and submission

```powershell
./.venv/Scripts/python.exe -m scripts.package_submission
./.venv/Scripts/python.exe -m zipfile -t artifacts/solari-ticket-assistant.zip
Get-FileHash artifacts/solari-ticket-assistant.zip -Algorithm SHA256
```

The allowlisted ZIP includes source, original supplied data, direct/resolved manifests and frontend lockfile, tests, original/current evaluation, preflight/runbook and docs. Stable entry timestamps/order, required membership, CRC and source SHA256 are verified. `.git`, environments, runtimes, node_modules, weights, caches, secrets and builds are excluded. Creation is local only. Deadline: **October 20, 2026 EOD; timezone unspecified**. Verify original Launchpad and recipient timezone, review archive, then manually submit.

| Requirement | Artifact |
| --- | --- |
| Design/assumptions/trade-offs | `SOLUTION_DESIGN.md` |
| Retrieval/preprocessing/uncertainty | `backend/evidence.py`, `backend/retrieval.py` |
| Typed readiness/examples/search/errors | `backend/app.py` |
| Agent UI and browser smoke | `frontend/src/`, `frontend/e2e/` |
| Strict validation/non-destructive duplicate inspection | `scripts/inspect_data.py`, `tests/` |
| Current-definition regression, original preserved evidence | `evaluation/` |
| Windows numbered setup/run/acceptance/troubleshooting | `docs/LAUNCHPAD_RUNBOOK.md` |
| Actual checks, demo, factual assistance | `docs/VALIDATION.md`, `docs/DEMO_GUIDE.md`, `docs/AI_ASSISTANCE.md` |
| Submission ZIP | `scripts/package_submission.py` |
| Shared continuity | `AGENTS.md`, `.github/copilot-instructions.md`, `PROJECT_STATUS.md` |

No production auth/tenant isolation, security/load certification, physical-device/other-browser certification, or original sandbox verification is claimed. Static indexes require restart after data changes. For blocked downloads, incorrect runtime, offline cache or proxy errors, follow the runbook troubleshooting and retain exact errors; never disable TLS or claim an unrun check passed.
