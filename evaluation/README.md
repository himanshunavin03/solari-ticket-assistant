# Evaluation: historical precedent for review

## Definition and limits

A note-bearing result is **original historical precedent with applicability unverified**, never verified root cause or a confirmed fix. Weak related metadata is not a displayed resolution. Invalid input and unavailable service are separate errors. All retained cases have been inspected and are **exposed regression benchmarks**. Labels are AI-authored synthetic judgments, not independent support-agent review or production accuracy evidence.

The supplied four examples, complete original inputs, all three modes, component scores and actual note visibility are recorded in [SAMPLE_TICKET_RESULTS.md](SAMPLE_TICKET_RESULTS.md) and [sample-ticket-results.json](sample-ticket-results.json). Hybrid displays T-1201 for the chart and T-1303 for billing; reset-email and unfamiliar Snowflake issues show related metadata without notes. Keyword abstains on the supplied chart example because lexical clause coverage .431559 is below .50. No policy changes were needed for these examples.

## Retained current-policy measurements

`informal-baseline-results.json` (v5) and `informal-revised-results.json` (v6) use the same displayed-precedent definitions and pinned MiniLM. `informal-freeze.json` records the 18-case input hash and baseline source hashes before the change. The original reported informal input is preserved exactly: subject `i charged twice`; description `i charged twice please validate this transaction`.

| Informal exposed cases: 8 positive / 10 negative | Recall@3 / MRR v5 → v6 | Positive abstentions | Negative queries displaying notes |
| --- | --- | --- | --- |
| Keyword | .250 → .375 | 6/8 → 5/8 | 0/10 → 0/10 |
| Semantic | .625 → .875 | 3/8 → 1/8 | 0/10 → 0/10 |
| Hybrid | .625 → .875 | 3/8 → 1/8 | 0/10 → 0/10 |

The reported request originally scored keyword .262235, semantic .559230 and clause .606230. It failed overall semantic >=.65, although clause coverage passed >=.45; no shared identifier applied. Query-only generic polite-framing removal preserves objects, symptoms and negation. The narrow short-query route requires keyword >=.25, semantic >=.60, all clauses >=.65, lexical coverage >=.50 and complete context. Global thresholds did not decrease. Revised semantic .642657 / clause .723596 / lexical .666667 qualify; original notes remain unverified.

Existing original (8 positive/4 negative), previous-release (8/4) and short-clause (4/3) metrics are unchanged: semantic/hybrid Recall@3/MRR 1.0; keyword .25/.375/.5. No negative-query notes appear on these small sets. This is not perfect precision: one short login-failure case returns irrelevant T-1004 alongside correct T-1001. The informal HTTP 429 paraphrase remains related-only, missing T-1702; the existing explicit 429 control passes. Keyword misses many valid paraphrases. No further tuning was performed to eliminate all observed failures. Generic negation/mechanism ambiguity, unknown products and synthetic labels remain risks.

Recall@3 is the macro-average fraction of labeled relevant IDs displayed on positive queries. MRR uses the first relevant displayed rank. Precision@3 divides relevant displayed IDs by **3**, even if fewer results are shown. Positive abstentions count queries with no displayed notes; extras on positives are counted separately. Negative note presentations count negative queries with any notes. Related metadata is excluded from these measures. Per-case IDs, scores, input/data/source hashes, versions and warm timing samples are in the JSON. Timing runs overlapped development activity and are not controlled speed comparisons, throughput or SLA claims. These definitions differ from older supported-resolution experiments; those experiments remain in the working repository rather than the focused submission.

## Reproduce without overwriting reports

From the project root, provision the pinned model first, then:

```powershell
$env:SOLARI_OFFLINE = '1'
./.venv/Scripts/python.exe -m evaluation.review_informal --policy current --output "informal-current-$(Get-Date -Format yyyyMMdd-HHmmss)-results.json"
./.venv/Scripts/python.exe -m evaluation.review_informal --policy baseline --output "informal-baseline-$(Get-Date -Format yyyyMMdd-HHmmss)-results.json"
./.venv/Scripts/python.exe -m pytest -q
# With FastAPI running:
./.venv/Scripts/python.exe -m scripts.verify_samples
```

The evaluator verifies frozen informal input bytes and refuses existing output paths. `baseline_v5/` contains the recorded prior evidence/retrieval implementation; only its import path and repository-root calculation are adapted for the nested location. A test reverses those two adaptations and verifies the original recorded SHA256 hashes. This makes the retained comparison reproducible without Git metadata or obsolete experiments. Baseline JSON hashes refer to original source locations; new baseline runs identify the shipped snapshot source hashes.

`results.json`, `run.py`, `review_precedents.py` and `precedent-regression-results.json` are retained for preservation/refusal tests and provenance. Legacy writers refuse current policy rather than overwrite historical results. `metrics.py` retains the denominator definitions tested by the suite. All other case files included here are inputs used by the current evaluator; no shipped test is silently omitted. `data-quality-report.json` records strict 40-record validation and non-destructive duplicate inspection. No imputation or removal of repeated incidents.
