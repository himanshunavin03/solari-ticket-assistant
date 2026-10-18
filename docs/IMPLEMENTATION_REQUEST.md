Act as the software engineer responsible for completing this FDE case study. Implement a working, tested application in this repository. Do not stop after producing a plan or scaffolding.

Read the actual assignment and existing files before making changes.

PROJECT
Solari Analytics — Support Ticket Similarity Assistant.

Existing repository structure:
case-study-1-support-ticket-similarity/
  case-study-brief.md
  starter_kit/
    README.md
    ticket_utils.py
    data/tickets.json
    data/new_tickets_example.json
README.md

Ignore __MACOSX metadata.

First read the brief, starter README, utility code, and both datasets. Treat the assignment as the source of truth. Preserve the original supplied files and dataset. Inspect existing repository instructions and changes; do not overwrite unrelated work.

OBJECTIVE
A support agent enters a new ticket’s subject and description and receives relevant historical tickets with their original resolution notes.

Build a complete, appropriately scoped solution that demonstrates:
- Requirements clarification and explicit assumptions.
- Sound engineering and ML judgment.
- Working end-to-end behavior.
- Measured retrieval quality.
- Honest limitations and reproducible setup.

ENVIRONMENT AND COMPATIBILITY
The target is a Windows sandbox with:
- Python 3.10.0
- pip 21.2.3
- Node.js 20.10.0
- npm 10.2.3
- Git 2.43.0.windows.1
- No required Python packages currently installed.
- Conda is not accessible and must not be required.
- No GPU or database dependency.

Inspect the local development environment first.

Verify Angular/Node/TypeScript compatibility against official documentation before choosing exact versions. Do not install Angular latest blindly: Node 20.10.0 may not satisfy its requirements.

Prefer a currently supported Angular version with a compatible project-local Node runtime if the sandbox runtime needs updating. Provide exact Windows installation/bootstrap instructions and explain any runtime change. Never silently replace a system installation or require an obsolete framework merely to preserve an old Node version.

Use Python 3.10-compatible backend dependencies and verify their Python requirements. Use a project-local virtual environment. If an additional runtime is needed locally, install it in a project-local or user-local location where feasible.

Pin tested direct dependencies, commit the frontend lockfile, and record actual resolved versions. Use npm ci for reproducible frontend installation. Do not commit virtual environments, node_modules, credentials, or downloaded model weights.

If a download or environment restriction blocks work, report it precisely and continue independent work. Never claim Windows sandbox verification based only on a Linux test.

IMPLEMENTATION
Use:
- Angular and TypeScript frontend.
- Python and FastAPI backend.
- scikit-learn TF-IDF baseline.
- Pretrained Sentence Transformer semantic retrieval.
- Reciprocal rank fusion for hybrid ranking.
- JSON data and in-memory indexes.
- Disk caching for historical embeddings.

Do not introduce a database, agent framework, generative LLM, paid API, or model training unless the supplied requirements genuinely demand it.

1. DATA
Validate historical tickets at startup:
- Unique IDs.
- Required fields and their types.
- Useful errors for malformed data.
- Do not silently discard invalid records.

Search historical subject + description consistently. Display original resolution notes as evidence rather than generating a new fix.

2. KEYWORD BASELINE
Implement TF-IDF and cosine similarity with sensible text handling.
Preserve meaningful identifiers, numbers, and technical error terms where practical.
Handle empty input, out-of-vocabulary input, and zero vectors.
Return deterministic results with stable tie-breaking.

3. SEMANTIC RETRIEVAL
Choose a small, CPU-friendly pretrained Sentence Transformer appropriate for English ticket similarity, such as all-MiniLM-L6-v2, after verifying compatibility and availability.

Do not train or fine-tune on the 40-ticket dataset.
Record the exact model identifier and resolved revision.
Load the model once; precompute historical embeddings.
Normalize embeddings consistently for cosine similarity.

Cache embeddings using a key incorporating:
- Dataset content hash.
- Model identifier/revision.
- Text preprocessing version.

Invalidate stale caches. Avoid unsafe pickle loading and allow_pickle=True for NumPy cache files.

Provide a documented model pre-download command and offline reuse instructions. A fresh clone still requires dependencies and model download unless provisioned beforehand.

4. HYBRID RANKING
Implement reciprocal rank fusion using keyword and semantic rankings.
Do not add raw TF-IDF and embedding scores directly.
Exclude zero-evidence keyword candidates from contributing arbitrary ranks.
Keep component scores available for inspection.

Fusion scores are ranking values, not confidence probabilities.

5. INSUFFICIENT EVIDENCE
Support an explicit no-reliable-match outcome.
Base thresholds on reviewed development examples and document the heuristic and its limitations.
Do not hardcode “Snowflake” or any example text into matching logic.

Distinguish:
- No reliable historical match.
- Search/model service unavailable.
- Invalid input.

Do not claim that a similarity threshold establishes a calibrated probability of a correct resolution.

If semantic model loading fails, keep keyword search available only with an explicit degraded-mode indicator. A hybrid request must not silently pretend that semantic retrieval ran.

6. API
Provide documented endpoints for:
- Health/readiness, including active retrieval capabilities.
- Ticket search.
- Supplied example tickets if useful for the frontend.

Validate whitespace-only inputs, length limits, requested mode, and top-k bounds.
Use typed request/response models.
Return clear, consistent errors without leaking stack traces.
Restrict local development CORS origins.
Avoid logging raw ticket text by default.
Ensure model loading and index creation do not happen per request.
Keep blocking inference from unnecessarily blocking the async event loop.

7. FRONTEND
Build a polished, restrained Solari Analytics support-agent interface:
- Subject and description fields.
- Example-ticket selector.
- Search action and clear/reset.
- Top-three matches by default.
- Historical ticket ID, subject, category/tags, and resolution notes.
- Expandable original ticket description.
- Clearly labelled relevance evidence.
- Loading, validation, backend failure, degraded-mode, and no-match states.
- Accessible labels, keyboard operation, and responsive layout.

Prevent stale results from an earlier request overwriting a newer search.
Do not display relevance scores as “percentage accuracy.”
Keep developer diagnostics out of the default agent workflow; use an optional technical-details view.

8. EVALUATION
Create a small, manually reviewed evaluation dataset grounded in the supplied tickets:
- Clear matches.
- Meaning-preserving paraphrases.
- Confusable issues with similar vocabulary.
- Unrelated/no-match queries.
- The supplied Snowflake example.

Inspect all relevant historical tickets before assigning expected IDs.
Allow multiple relevant IDs where appropriate.
Document relevance-label rationale.

Separate development examples used for threshold tuning from held-out evaluation examples. Do not tune using the held-out set.
Do not include historical resolution text in incoming evaluation queries.

Compare keyword, semantic, and hybrid retrieval using:
- Precision@3.
- Recall@3.
- MRR.
- No-match acceptance/rejection outcomes.
- Warm search latency, with hardware and sample-count context.

Define metric denominators and treatment of no-match cases.
Report actual measurements only.
Do not force hybrid to win; explain the observed trade-off.
State clearly that this small synthetic evaluation does not establish production accuracy or throughput.

9. TESTS
Implement meaningful tests for:
- Data validation.
- Ranking and deterministic ties.
- Blank and out-of-vocabulary queries.
- Top-k bounds.
- No-match logic.
- Cache invalidation.
- Semantic-unavailable behavior.
- API contracts and error responses.

Separate fast offline tests from actual model integration tests.
Mocks must not be presented as evidence that real embeddings work.

Run frontend build/type checks and an end-to-end smoke test.
If browser automation is available, verify at least:
- A known-match search.
- No reliable match.
- Validation.
- Backend failure.
- Stale-request handling where practical.

10. DOCUMENTS
Produce:
- SOLUTION_DESIGN.md: approximately 1–2 pages covering the restated problem, assumptions and reasons, architecture, trade-offs, and improvements with more time/data/budget.
- README.md: exact Windows PowerShell setup/run/test instructions, runtime versions, model download/offline behavior, example usage, limitations, and troubleshooting.
- evaluation/README.md and actual machine-readable evaluation results.
- docs/DEMO_GUIDE.md: a short demonstration narrative and likely panel questions.
- docs/AI_ASSISTANCE.md: a factual log of AI assistance; do not invent Copilot reviews or approvals.

Keep the design document concise; put detailed results in evaluation files.

Document production considerations proportionately:
Customer permissions and tenant isolation would be required for real customer data; the supplied synthetic dataset contains no tenant identifiers. Do not claim production security, scale testing, or functionality that was not implemented.

11. PACKAGING
Provide a reproducible packaging script that creates one submission ZIP containing source, provided data, dependency manifests/lockfiles, required documents, and evaluation artifacts.

Exclude .git, node_modules, virtual environments, model weights, caches, secrets, and unnecessary build outputs.
Verify the resulting archive contents.
Do not publish, push changes, upload to OneDrive, or submit on my behalf.

WORKFLOW
Start with a brief requirements checklist and implementation plan, then proceed with implementation.
Keep scope aligned with the assignment’s approximately 3–4 focused-hour expectation; prioritize a complete core flow.
Avoid speculative infrastructure and optional features that threaten completion.

Implement in working milestones:
1. Dataset validation and keyword baseline.
2. Semantic retrieval, caching, hybrid ranking, and no-match behavior.
3. API and frontend.
4. Evaluation, tests, documentation, and packaging.

Run appropriate checks after each milestone.
Inspect failures and fix their root causes.
Do not fabricate successful checks.

FINISH WITH
- What was implemented.
- Exact tested runtime and dependency versions.
- Actual commands/checks run and their results.
- Known limitations and any blocked checks.
- Exact Windows sandbox commands.
- A requirement-to-artifact checklist.
- The remaining manual sandbox verification and submission steps.