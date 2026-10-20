# Solari Ticket Assistant

Find relevant historical support tickets and their **original resolution notes**. Every displayed resolution has **applicability unverified**: it is precedent for an agent to review, not a confirmed diagnosis or fix. Weak or conflicting history is shown separately without notes.

## Quick Start — Windows PowerShell

Run commands from the extracted project/repository root. Use Python **3.10 or 3.11**; development validation used **3.10.11 and 3.11.9**. Original Launchpad **3.10.0 remains unverified**. Angular requires Node **^20.19.0, ^22.12.0 or >=24**. **Launchpad Node 20.10.0 cannot build this Angular version.** The existing bootstrap installs an additional project-local Node without replacing system Node:

```powershell
./scripts/bootstrap-node.ps1
$env:Path = (Join-Path (Get-Location) '.runtime/node-v22.23.2-win-x64') + ';' + $env:Path
python --version
node --version
python -m venv .venv
./.venv/Scripts/python.exe -m pip install --upgrade pip==25.0.1
./.venv/Scripts/python.exe -m pip install -r requirements.txt
./.venv/Scripts/python.exe -m pip check
Push-Location frontend
npm ci
Pop-Location
Remove-Item Env:SOLARI_OFFLINE -ErrorAction SilentlyContinue
./.venv/Scripts/python.exe -m scripts.download_model
$env:SOLARI_OFFLINE = '1'
Remove-Item Env:SOLARI_KEYWORD_ONLY -ErrorAction SilentlyContinue
./scripts/preflight.ps1
./.venv/Scripts/python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --no-access-log
```

Preserve any existing virtual environment you still need. Fresh setup requires network access for dependencies, Node and model weights. The model command loads pinned `sentence-transformers/all-MiniLM-L6-v2@1110a243fdf4706b3f48f1d95db1a4f5529b4d41` on CPU and verifies a real `(1, 384)` embedding. Offline mode is enabled only afterward.

In a **second PowerShell terminal**, start at the same project root:

```powershell
$env:Path = (Join-Path (Get-Location) '.runtime/node-v22.23.2-win-x64') + ';' + $env:Path
Push-Location frontend
npm start
```

Open **http://127.0.0.1:4200**. Ctrl+C stops each server. The Angular dev proxy forwards `/api` to port 8000.

**Backend-only fallback:** if frontend setup is blocked, keep FastAPI running and open **http://127.0.0.1:8000/docs**. Use `POST /api/search` → Try it out with subject, description, mode (`keyword`, `semantic`, `hybrid`) and `top_k` (1–10). Check `GET /api/health` for active capabilities. Swagger UI assets load from a CDN; if that is blocked, `/openapi.json` and PowerShell HTTP requests still expose the backend API. If model provisioning is blocked, explicitly set `$env:SOLARI_KEYWORD_ONLY='1'` before backend startup and select keyword; readiness is degraded and semantic/hybrid return 503, not silent fallback.

For exact runtime diagnostics, download troubleshooting, acceptance checks and packaging, see the [detailed runbook](docs/LAUNCHPAD_RUNBOOK.md). Do not disable TLS or replace pinned dependencies to work around a blocked download; retain its exact error.

## Validation and behavior

```powershell
$env:SOLARI_OFFLINE = '1'
./.venv/Scripts/python.exe -m pytest -q
./.venv/Scripts/python.exe -m scripts.verify_samples
# Browser checks start their own servers; stop manual servers first.
$env:SOLARI_TEST_PYTHON = '.venv/Scripts/python.exe'
Push-Location frontend
npx playwright install chromium
npm run typecheck
npm run build
npm run test:e2e
Pop-Location
```

The four supplied examples are recorded in [SAMPLE_TICKET_RESULTS.md](evaluation/SAMPLE_TICKET_RESULTS.md): hybrid shows original empty-chart and duplicate-billing notes; reset-email and unfamiliar-integration cases withhold misleading notes. [Validation](docs/SUBMISSION_VALIDATION.md) distinguishes actual checks, reused resources and unverified environments. [Evaluation](evaluation/README.md) explains measured recall, false matches and reproducibility.

## Known limitations

- MiniLM similarity and lexical overlap do not prove mechanism, negation or root-cause agreement. Historical notes always need human review.
- Conservative keyword matching misses many paraphrases. One informal HTTP 429 example still abstains; one short login-failure example includes an irrelevant extra precedent.
- Results use small, exposed, AI-authored synthetic regression sets; no independent labeling or production accuracy is claimed.
- English request-framing rules are limited. More than eight clauses cannot show notes; individual embeddings truncate at 256 wordpieces.
- Static JSON/in-memory indexes need restart after data changes. Downloads, cold startup, other browsers/devices and original Launchpad restrictions remain environment-dependent.

## Not handled yet

Authentication, tenant/access filtering, live ingestion, persisted agent feedback, automatic ticket updates, generated answers, production deployment/security/load certification and realistic growth planning. These need customer requirements and measurement first.

## Package and design

```powershell
./.venv/Scripts/python.exe -m scripts.package_submission
./.venv/Scripts/python.exe -m zipfile -t artifacts/solari-ticket-assistant.zip
Get-Content artifacts/included-files.txt
```

The [explicit package contents](docs/SUBMISSION_CONTENTS.md) include source, pinned manifests, original data, all tests and their evaluation dependencies. Session instructions, internal prompts, obsolete experiments, environments, weights and generated output are excluded. The final design PDF is included **only if supplied at `docs/SOLUTION_DESIGN.pdf`**; it is currently a manual deliverable, not generated by this project. [SOLUTION_DESIGN.md](SOLUTION_DESIGN.md) is the authoritative implementation design.

Built with AI-assisted coding; design decisions and validation reviewed by the author.

AI-authored synthetic evaluation labels are not independent human review.
