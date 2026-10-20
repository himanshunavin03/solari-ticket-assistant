# Current informal-request revision (v6)

See [INFORMAL_REVISION.md](INFORMAL_REVISION.md) for exact rejection diagnosis, policy, frozen exposed cases, comparable before/after results and remaining failures. Hybrid informal Recall@3/MRR .625→.875; negative note presentations 0/10→0/10. All earlier artifacts below remain historical v5 measurements; their writer refuses v6. Current reports: `informal-baseline-results.json` / `informal-revised-results.json`.

---

# Preserved v5 evaluation — historical precedent, applicability unverified

## Changed semantics and preserved evidence

Current `historical-precedent-v1` measures whether useful historical resolution notes are retrieved **for agent review**, never whether root cause or applicability has been verified. Every note-bearing match is `applicability=unverified`. Weak/conflicting candidates are metadata only; no relevant history and service unavailable are separate outcomes.

Earlier `supported` resolution interpretation and current historical precedent are **not equivalent definitions**. Do not present changes in their percentages as calibrated acceptance/accuracy improvement. For example, v4 keyword deliberately displayed no notes; v5 restores a conservative note-bearing workflow, not verified mechanism agreement.

All earlier cases/results/freeze artifacts remain unchanged. Their inspected release sets are now **exposed regression** for this correction. Prior narratives are preserved in `ORIGINAL_EVALUATION.md` and `V4_EVALUATION.md`; they describe their historical revisions only. Legacy result-writing evaluators refuse this changed policy rather than overwrite historical results under different semantics. The earlier case/source hashes remain historical provenance, not a current untouched-test claim.

New reports: `precedent-regression-results.json` (current), `precedent-initial-results.json` (first current-definition run, retained), `data-quality-report.json` (strict data/duplicate inspection). `precedent-cases.json` adds targeted diagnosis/regressions; it was authored after the problem was exposed and is not a blind test. AI-authored synthetic labels/rationales are not independent human support-agent judgments.

## Cases and actual current results

`python -m evaluation.review_precedents` evaluates the real pinned MiniLM with all three retrieval modes on:

- `original_exposed`: original 8 positive / 4 negative held-out cases, now regression.
- `previous_release_now_exposed`: previous 8 positive / 4 negative release cases, now regression.
- `targeted_exposed`: 4 positive / 3 negative short-clause, identifier, billing/429 and punctuation regressions.

| Exposed split | Mode | Precedent Recall@3 / MRR | Positive queries without note-bearing precedent | Irrelevant note presentations on negative queries |
| --- | --- | --- | --- | --- |
| Original | Keyword | .250 / .250 | 6/8 | 0/4 |
| Original | Semantic | 1.000 / 1.000 | 0/8 | 0/4 |
| Original | Hybrid | 1.000 / 1.000 | 0/8 | 0/4 |
| Prior release | Keyword | .375 / .375 | 5/8 | 0/4 |
| Prior release | Semantic | 1.000 / 1.000 | 0/8 | 0/4 |
| Prior release | Hybrid | 1.000 / 1.000 | 0/8 | 0/4 |
| Targeted | Keyword | .500 / .500 | 2/4 | 0/3 |
| Targeted | Semantic | 1.000 / 1.000 | 0/4 | 0/3 |
| Targeted | Hybrid | 1.000 / 1.000 | 0/4 | 0/3 |

These are current-definition retrieval measurements, not a before/after claim against v4 supported-resolution metrics. The tests demonstrate an actual behavioral correction: the literal completed-reset-plus-missing-email query previously displayed T-1001 after dropping its failure clause; it now retains the clause and withholds that resolution. A splitter unit test alone would not prove that effect.

Keyword duplicate billing and the explicit integration/429 regression display original notes even without the semantic model, with unverified applicability. The supplied missing reset email, Snowflake query and literal short contradiction stay related-only in keyword/hybrid. Punctuation-only inputs produce no relevant history. Actual degraded behavior and unavailable hybrid requests are covered by a real second test backend, not only a simulated health response.

Remaining measured failure: the targeted `short-still-fails` query displays correct T-1001 **and extra irrelevant T-1004** in semantic/hybrid (1/4 positive queries with an irrelevant extra precedent). Recall@3/MRR of 1.0 therefore does not mean every displayed note is relevant. No policy tuning was performed to remove this observed failure.

## Policy and trade-offs

The old four-word filter is removed: retain every alphanumeric short clause/negation, ignore punctuation/empty fragments, preserve dots/hyphens/connective-looking identifier components. Original text/data are not rewritten. All retained clauses count toward the eight-clause limit; excess context cannot display notes. Cache preprocessing version changed so historical clause embeddings rebuild safely.

Keyword precedent requires overall TF-IDF cosine >=.25 and minimum IDF-weighted meaningful-token clause coverage >=.50. Generic function-word filtering retains negation/contractions; out-of-vocabulary terms remain weighted in the denominator. This avoids treating only the known topical words as the complete query. Semantic/hybrid retain previous similarity/identifier rules with corrected clauses; they never bypass them through keyword OR acceptance. No product, ticket-ID, specific-code or example-text rules.

The **keyword false-abstention cost is substantial**: 6/8 original and 5/8 prior-release positive queries show no note-bearing precedent. Correct contextual history may remain available as metadata. This is a conservative lexical workflow, not robust paraphrase matching; no thresholds were retuned until all examples passed. Semantic similarity/identifier matching still cannot prove negation, mechanism or root-cause equivalence. Short generic fragments can suppress valid retrieval; per-embedding 256-wordpiece truncation remains. Strong scores on small, known synthetic cases do not establish production accuracy or throughput. Independently reviewed representative data remains necessary.

## Metric definitions, runtime and reproducibility

- `precedent_recall_at_3`: relevant displayed note-bearing IDs divided by labeled relevant IDs, macro-average over positive queries. `precedent_mrr`: reciprocal rank of first relevant displayed precedent, zero if absent. `precedent_precision_at_3`: relevant displayed IDs / **3**, even if fewer were returned. These measure review precedent, not fix correctness.
- `positive_precedent_abstentions`: positive queries with no note-bearing result. Wrong/extra precedents on positives are separately counted; relevance metrics penalize wrong IDs. `irrelevant_precedent_presentations`: negative queries with any displayed resolution. Related metadata is never counted as displayed resolution; negative cases are excluded from relevance averages.
- Hardware/OS/Python/package versions, code/case/data SHA256, pinned model/revision, outcome counts and per-case scores/IDs are in the JSON. Actual runtime is Windows Python **3.10.11**, CPU, four Torch threads. This is not original Launchpad 3.10.0 validation.
- One warmup per query/mode, then five sequential timed searches: 60 samples/mode for each 12-query regression and 35 for the 7-query targeted set. JSON records median and nearest-lower-rank p95. Timings exclude cold model load, HTTP and browser time; no concurrency/SLA/production-throughput claim. Initial run overlapped browser startup; final report refreshed after test servers stopped, without changing relevance thresholds.

```powershell
$env:SOLARI_OFFLINE = '1'
./.venv/Scripts/python.exe -m evaluation.review_precedents
./.venv/Scripts/python.exe -m scripts.inspect_data
```

On this host, `.venv310/Scripts/python.exe` selects the tested compatibility interpreter; fresh Launchpad setup uses `.venv`. Reruns update only current-definition report(s), never earlier release/original JSON. Reuse is regression checking, not a newly untouched test. No missing checks are represented as passed.
