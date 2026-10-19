# Retrieval evaluation — October 19 revision

All labels are AI-authored synthetic judgments after inspection of the supplied tickets, not independent support-agent review. Every query has a rationale; incoming queries exclude historical resolution text. This evaluation does not establish production accuracy, calibrated confidence, or throughput.

## Provenance and preserved evidence

- Reviewed baseline: commit `0dbf77d1e9e8ceac1b9130a66c7049f34fbce6f7`. `frozen_reviewed_retrieval.py` is its byte-for-byte backend source; SHA256 is checked by the comparison runner. Baseline and revised policies run with the same model revision, dataset and interpreter for each comparison.
- Original `cases.json`, `results.json`, `development-results.json`, `development-initial-results.json`, and `development-evidence.json` remain unchanged. Historical narrative is preserved in `ORIGINAL_EVALUATION.md`. Its JSON split name `held_out` is historical: those 8 positive/4 negative cases are now an **exposed regression benchmark**, and informed this revision.
- `revision-cases.json`: 12 positive/4 negative development queries cover unfamiliar integrations, different mechanisms, valid paraphrases, duplicate billing, HTTP 429, and a multi-ID transaction case. Its first fresh partition (8 positive/6 negative) was frozen before V2 scoring. Those results (`revision-*-results.json`) became exposed through iteration; they are not an untouched evaluation of the final policy.
- `final-cases.json` and `final-*-results.json` preserve the V3 iteration (6 positive/4 negative fresh cases). These too became exposed. V2/V3 policy functions are preserved in `frozen_clause_v2_evidence.py` and `frozen_clause_v3_evidence.py`; results include policy hashes. Original-case failures and the insufficient numeric corroboration check were inspected before V4 selection.
- Final V4 policy passed regression tests before `release-cases.json` was frozen. Its 8 positive/4 negative queries and policy/retriever hashes were recorded in `release-freeze.json` at 2026-10-19 17:21:51 UTC, **before any release-case scoring**. The runner rejects changes to these hashes. No tuning followed release results. This is a single-author sequential split, not an independently blind benchmark.

Source/case text SHA256 comparisons normalize CRLF to LF so Windows Git line-ending conversion does not masquerade as policy edits. Dataset and archive hashes retain exact source bytes.

## Final evidence policy

TF-IDF and normalized whole-ticket MiniLM rankings remain separate; hybrid uses RRF `1/(60+rank)` with deterministic ID ties and no contribution from zero keyword evidence. RRF ranks candidates; it does not decide whether a resolution is supported.

`backend/evidence.py` distinguishes supported evidence from related topics:

1. Overall cosine at least 0.65 **and** every retained query description clause has cosine at least 0.45 against some subject/description clause of the candidate; or
2. A shared generic technical identifier containing at least three digits, overall cosine at least 0.60, and identifier-bearing clause alignment at least 0.60.

Otherwise keyword cosine at least 0.25 or whole-ticket semantic cosine at least 0.50 can retrieve **related metadata only**. Its resolution is absent from both API response and UI. Pure keyword mode never endorses resolutions; supported Recall@3 is therefore zero by design. Candidate recall is separately reported so that feature restriction is not misrepresented as superior retrieval quality.

Generic English coordination/contrast markers split clauses, with a four-word minimum and whole-text fallback; candidate subjects also contribute context. More than eight query clauses abstains rather than approving partial context. No product names, ticket IDs, example strings, or special-case HTTP codes appear in policy. This is not an NLI/entailment model: short-fragment loss, negation ambiguity, product mismatch and numeric collisions remain possible.

Development diagnosed the OR failure: reset-mail topical cosine .678 hid a delivery-clause alignment near .369; the supplied exposed reset example hid a .289 delivery clause. V2 coverage stopped those but rejected valid rate-limit wording. The generic identifier route was added and its initial .65 alignment requirement failed two real-model tests; .60 corroboration was chosen using that **already exposed** regression, then frozen before release scoring. This is a new evidence signal, not raising a single cutoff until the target examples pass. Recall costs were retained and measured.

## Actual before/after results

Final comparisons use Windows Python **3.10.11**, Torch 2.6.0 CPU with four threads, Intel64 Family 6 Model 186 Stepping 2 (20 logical CPUs). Exact hardware, package versions, source/case/data hashes, sample counts and returned IDs are in JSON. Original October 17 measurements used Python 3.11.9 and are preserved, not substituted for current measurements.

| Split / mode | False acceptances baseline → revised | False rejections baseline → revised | Recall@3 baseline → revised | MRR baseline → revised |
| --- | --- | --- | --- | --- |
| Development / keyword | 3 → 0 (4 negatives) | 1 → 12 (12 positives) | .9167 → .0000 | .9167 → .0000 |
| Development / semantic | 0 → 0 | 2 → 1 | .8333 → .8750 | .8333 → .9167 |
| Development / hybrid | 3 → 0 | 1 → 1 | .9167 → .8750 | .9167 → .9167 |
| Exposed regression / keyword | 2 → 0 (4 negatives) | 0 → 8 (8 positives) | 1.0000 → .0000 | 1.0000 → .0000 |
| Exposed regression / semantic | 1 → 0 | 1 → 0 | .8750 → 1.0000 | .8750 → 1.0000 |
| Exposed regression / hybrid | 2 → 0 | 0 → 0 | 1.0000 → 1.0000 | 1.0000 → 1.0000 |
| Frozen release / keyword | 2 → 0 (4 negatives) | 1 → 8 (8 positives) | .8750 → .0000 | .8750 → .0000 |
| Frozen release / semantic | 0 → 0 | 1 → 1 | .8750 → .8750 | .8750 → .8750 |
| Frozen release / hybrid | 2 → 0 | 1 → 1 | .8750 → .8750 | .8750 → .8750 |

The two supplied misleading examples now have no supported resolution in semantic/hybrid; related metadata can remain visible. Duplicate payment and the original HTTP 429 query still retrieve the correct supported resolution. Hybrid has no final-release advantage over semantic and adds ranking overhead; it is not forced to win.

Development supported recall **decreases** for hybrid because the recent-sync-plus-CSV query only supports the export ticket, placing the second linked sync ticket under related history. The broad code-free rate-limit paraphrase is still related-only. Release false rejection: `release-layout`, a valid widget-overlap case, is returned as related, not supported. Supported-plus-related candidate recall is 1.0 on release and exposed regression for revised semantic/hybrid. This candidate metric does not mean agents received a supported resolution.

Remaining failure evidence is preserved, not erased: V2 first-fresh accepted SMS password-recovery as SMS 2FA; V3 second-fresh accepted a new missing-reset-mail phrasing. The final release happened to reject all four negatives, but does not prove those broader failure classes are solved. These exposed failures were not patched with product-specific rules. Further changes require a new evaluation, independently reviewed labels, and larger realistic cases.

## Metric definitions and latency

- A false acceptance is a negative/no-relevant-ID query receiving any **supported** resolution. Related metadata is not a supported acceptance. A false rejection is a positive query receiving no supported result; a wrong supported ID is separately counted as `wrong_resolution_on_positive` and penalized in recall/MRR.
- Recall@3 is relevant supported IDs divided by all labeled relevant IDs, macro-averaged over positives. MRR is reciprocal first relevant supported rank, zero when absent. Precision@3 divides relevant supported IDs by 3 even when fewer than three are returned. Negative cases are excluded from these relevance averages and counted separately.
- `candidate_recall_at_3` uses the first three IDs from delivered supported results followed by related metadata. It describes available investigation context, not resolution acceptance or an ungated raw ranking.
- One warmup per query/mode, then five sequential timed searches. Development has 80 warm samples/mode; regression and release have 60. Median and nearest-lower-rank p95 cover retriever execution, excluding cold load, API and browser time. No sustained load or concurrency guarantee.
- Revised clause encoding adds CPU cost. Before/after latency, including each mode's median/p95, is in `release-results.json`, `release-regression-results.json`, and `release-development-results.json`. The final regression/release latency rerun occurred after browser tests/server cleanup, with the same frozen policy/cases. No idle-machine or production-SLA claim.

Final frozen release latency (baseline → revised, milliseconds; median / p95): keyword **0.344 / 0.891 → 0.378 / 0.588**; semantic **15.700 / 21.930 → 20.696 / 25.942**; hybrid **16.675 / 26.485 → 17.852 / 24.720**. Differences at this scale include host scheduling noise; p95 is not guaranteed to improve or worsen consistently. Related-only keyword results do less evidence verification and are not equivalent functionality to supported semantic/hybrid results.

## Reproduce safely

From repository root after model provisioning (choose the matching installed interpreter):

```powershell
$env:SOLARI_OFFLINE = '1'
./.venv310/Scripts/python.exe -m evaluation.compare_revision --split development
./.venv310/Scripts/python.exe -m evaluation.compare_revision --split regression
./.venv310/Scripts/python.exe -m evaluation.compare_revision --split release
```

On Launchpad use `./.venv/Scripts/python.exe` after its README setup. Reruns update only `release-*.json`; original and intermediate results are preserved. Rerunning release is repeatability/regression checking, not a newly untouched test. Legacy `evaluation.run` defaults to a new output and rejects original artifact paths. All AI-authored labels and their strict issue-equivalence choices still need independent support-agent review.
