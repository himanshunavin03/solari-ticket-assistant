# Historical original evaluation (October 17, 2026)

The following records the reviewed revision only. Its held_out set is now exposed regression evidence, NOT an untouched test for the current revision. Do not run its old output-overwriting commands; current commands and results are in evaluation/README.md.

# Retrieval evaluation

`cases.json` is a fixed, AI-assisted issue-level relevance set authored after inspecting all 40 historical ticket subjects/descriptions and supplied resolutions. It is not independently reviewed by support agents. Every query carries a relevance rationale. Resolution text is excluded from incoming queries. Examples focus on observable symptoms rather than the fixes described in resolutions.

Development has six positive queries and three no-match queries. One positive permits both T-1104 and T-1401 because they describe missing recent transactions and the export resolution explicitly links the sync issue. Held-out has eight positives and four no-match queries, including supplied NT-4 (Snowflake) and NT-1 (missing reset email). The latter is intentionally strict: T-1001 concerns a rejected password after the email arrived; T-1003 concerns SMS 2FA. A category-level neighbor is not necessarily a relevant resolution. Labels and split were written before executing either split; held-out outcomes must not be used to tune this implementation.

## Ranking and evidence policy

TF-IDF cosine and normalized MiniLM cosine form separate rankings. Hybrid RRF sums `1/(60+rank)` for each positive-evidence component ranking; zero keyword scores contribute nothing. Scores use stable ticket-ID tie-breaking. A displayed candidate must pass the selected mode's evidence gate; hybrid permits either component to pass. Consequently the API may return fewer than three results. The gate has no hardcoded product names or sample text.

Initial development candidates were keyword cosine 0.25 and semantic cosine 0.50 (`development-initial-results.json`). After reviewing only `development-evidence.json`, the final gates are **keyword 0.25, semantic 0.70**, frozen before held-out execution. The weakest positive semantic match was 0.72457 (viewer widget editing); the highest irrelevant neighbor observed was 0.64807 (reset rejection for a lockout query). Raising the semantic gate suppresses those misleading tails while retaining both relevant recent-transaction tickets (0.77879 and 0.74556). The unseen BigQuery connector's highest semantic score was 0.39361. Keyword 0.25 separates observed negative maxima (up to 0.21128) from positive first matches (at least 0.37505), but loses the second relevant transaction-export ticket at 0.21586. This is an explicit recall trade-off, not evidence of universal separation. The development set is too small to justify fine-grained numeric tuning.

These values are heuristic cosine cutoffs, not calibrated confidence probabilities. A global cutoff cannot reliably distinguish every unseen integration from familiar terminology. Fusion scores are rank values only. The threshold change and rationale were recorded in `PROJECT_STATUS.md` before running the held-out evaluation.

## Metrics and reproducibility

```powershell
$env:SOLARI_OFFLINE = '1'
./.venv/Scripts/python.exe -m evaluation.run --split development --output evaluation/development-results.json
./.venv/Scripts/python.exe -m evaluation.run --split held_out --output evaluation/results.json
```

- Precision@3: number of relevant returned IDs divided by **3**, even if fewer were returned. Macro-average over positive queries only. For a single relevant ID its maximum is 1/3.
- Recall@3: relevant returned IDs divided by the number of labeled relevant IDs; macro-average over positives only.
- MRR: reciprocal of the first relevant returned rank (1–3), or zero when absent; macro-average over positives only.
- No-match cases are excluded from those relevance denominators and reported separately as correct rejections and false acceptances. Positive false rejections are also reported.
- Metrics are computed on the **gated results shown to agents**, not an ungated diagnostic ranking.
- One warmup per query/mode, then five sequential measured searches per query. Median and nearest-lower-rank p95 cover the resulting samples; this is retriever latency, not HTTP/browser latency. No cold model load, concurrent load, or throughput estimate is included.
- JSON includes hardware/OS, Python/package versions, CPU thread setting, sample counts, model revision, dataset/case hashes, thresholds, per-case IDs and component scores. Unavailable modes are explicitly marked unavailable, never replaced with simulated embeddings.

The sample is small, synthetic and selected by the implementer. The held-out split prevents threshold reuse on these cases but is not an independent production benchmark. Human relevance review, larger customer-derived cases, repeated hardware tests and concurrency measurements remain future work. Do not claim production accuracy or throughput from these results.

## Measured held-out quality

| Mode | Precision@3 | Recall@3 | MRR | Correct no-match rejections | False acceptances | Positive false rejections |
| --- | --- | --- | --- | --- | --- | --- |
| Keyword | 0.3333 | 1.0000 | 1.0000 | 2/4 | 2 | 0/8 |
| Semantic | 0.2917 | 0.8750 | 0.8750 | 3/4 | 1 | 1/8 |
| Hybrid | 0.3333 | 1.0000 | 1.0000 | 2/4 | 2 | 0/8 |

Keyword and hybrid falsely accept **Snowflake as T-1105 (HubSpot authentication)** and **missing password-reset email as T-1001 (password rejected after reset)**. Semantic rejects Snowflake, but still falsely accepts the reset-email query and rejects the genuinely relevant HTTP 429 query at its 0.70 evidence gate. These are meaningful issue-equivalence and abstention failures. No thresholds were changed in response to these held-out outcomes.

Hybrid improves development recall for the multi-label recent-transactions case over keyword (1.0 vs 0.9167 macro recall), but has **no held-out quality advantage over keyword** and adds CPU inference cost. Its OR evidence gate inherits keyword false acceptances. Semantic is more conservative on unseen integration terms at the cost of positive recall. Precision@3 remains 1/3 when exactly one relevant ID exists, even if only that result is shown; interpret that denominator alongside per-case results and no-match outcomes.

Final measured warm latency (60 samples per mode): keyword median **0.302 ms**, p95 **0.348 ms**; semantic median **9.018 ms**, p95 **14.243 ms**; hybrid median **9.540 ms**, p95 **13.088 ms**. Exact machine context is in `results.json`. Latencies are local sequential retrieval measurements, not production response-time promises. The initial held-out run overlapped browser-server startup; the final rerun used unchanged frozen gates after browser tests and their servers had stopped. No controlled idle-machine or sustained-load claim is made.
