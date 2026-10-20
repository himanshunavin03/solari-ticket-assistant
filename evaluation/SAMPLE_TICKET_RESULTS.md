# Supplied sample-ticket results

Recorded: 2026-10-20T03:35:05.873917+00:00. Real pinned MiniLM, CPU; API ready with all three capabilities.
Model: `sentence-transformers/all-MiniLM-L6-v2@1110a243fdf4706b3f48f1d95db1a4f5529b4d41`; policy `informal-precedent-v6`.

Inputs below are copied unchanged from the supplied JSON. Every displayed resolution is original historical precedent; **applicability is unverified**, not confirmed root-cause agreement. Full responses: [sample-ticket-results.json](sample-ticket-results.json).

## NT-1

Subject:
```text
Can't log in, password reset email never arrives
```
Description:
```text
A customer requested a password reset an hour ago and says the email still hasn't shown up, even after checking spam.
```

| Mode | Outcome | Notes shown for | Related IDs (no notes) |
| --- | --- | --- | --- |
| keyword | related_history_only | None | T-1001 |
| semantic | related_history_only | None | T-1001, T-1004 |
| hybrid | related_history_only | None | T-1001, T-1004 |

| Mode | ID / disposition | Keyword | Semantic | Clause | Lexical clause | Identifier | RRF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| keyword | T-1001 (metadata only) | 0.336416 | — | — | — | — | — |
| semantic | T-1001 (metadata only) | 0.336416 | 0.711242 | 0.289482 | — | — | — |
| semantic | T-1004 (metadata only) | 0.077825 | 0.528224 | 0.189056 | — | — | — |
| hybrid | T-1001 (metadata only) | 0.336416 | 0.711242 | 0.289482 | — | — | — |
| hybrid | T-1004 (metadata only) | 0.077825 | 0.528224 | 0.189056 | — | — | — |

## NT-2

Subject:
```text
Chart shows nothing for the revenue tab
```
Description:
```text
The revenue tab on the main dashboard is completely empty for this customer, no bars, no error message, just white space.
```

| Mode | Outcome | Notes shown for | Related IDs (no notes) |
| --- | --- | --- | --- |
| keyword | related_history_only | None | T-1201 |
| semantic | historical_precedents | T-1201 | T-1101, T-1404 |
| hybrid | historical_precedents | T-1201 | T-1101, T-1404 |

| Mode | ID / disposition | Keyword | Semantic | Clause | Lexical clause | Identifier | RRF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| keyword | T-1201 (metadata only) | 0.402715 | — | — | — | — | — |
| semantic | T-1201 (notes, unverified) | 0.402715 | 0.865684 | 0.709735 | 0.431559 | — | — |
| semantic | T-1101 (metadata only) | 0.162405 | 0.587637 | 0.532027 | — | — | — |
| semantic | T-1404 (metadata only) | 0.127121 | 0.526418 | 0.486773 | — | — | — |
| hybrid | T-1201 (notes, unverified) | 0.402715 | 0.865684 | 0.709735 | 0.431559 | — | 0.032787 |
| hybrid | T-1101 (metadata only) | 0.162405 | 0.587637 | 0.532027 | — | — | — |
| hybrid | T-1404 (metadata only) | 0.127121 | 0.526418 | 0.486773 | — | — | — |

## NT-3

Subject:
```text
Getting charged twice this month
```
Description:
```text
Customer's card statement shows two charges for what should be a single monthly subscription payment.
```

| Mode | Outcome | Notes shown for | Related IDs (no notes) |
| --- | --- | --- | --- |
| keyword | historical_precedents | T-1303 | None |
| semantic | historical_precedents | T-1303 | None |
| hybrid | historical_precedents | T-1303 | None |

| Mode | ID / disposition | Keyword | Semantic | Clause | Lexical clause | Identifier | RRF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| keyword | T-1303 (notes, unverified) | 0.650908 | — | — | 0.534334 | — | — |
| semantic | T-1303 (notes, unverified) | 0.650908 | 0.895925 | 0.871612 | 0.534334 | — | — |
| hybrid | T-1303 (notes, unverified) | 0.650908 | 0.895925 | 0.871612 | 0.534334 | — | 0.032787 |

## NT-4

Subject:
```text
Our data warehouse integration with Snowflake is failing
```
Description:
```text
Customer set up a new integration to sync data into their Snowflake warehouse and it's failing with an unclear connection error. This is a newer integration type we haven't seen many tickets about yet.
```

| Mode | Outcome | Notes shown for | Related IDs (no notes) |
| --- | --- | --- | --- |
| keyword | related_history_only | None | T-1105 |
| semantic | related_history_only | None | T-1105 |
| hybrid | related_history_only | None | T-1105 |

| Mode | ID / disposition | Keyword | Semantic | Clause | Lexical clause | Identifier | RRF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| keyword | T-1105 (metadata only) | 0.342554 | — | — | — | — | — |
| semantic | T-1105 (metadata only) | 0.342554 | 0.485884 | 0.265046 | — | — | — |
| hybrid | T-1105 (metadata only) | 0.342554 | 0.485884 | 0.265046 | — | — | — |

## Original notes displayed

**T-1201** (applicability unverified):

A recent filter combination produced a zero-row result set, and the chart component didn't handle the empty-data case gracefully. Added an explicit 'no data for this range' state.

**T-1303** (applicability unverified):

A retry mechanism for a previously failed payment double-charged after the original payment actually succeeded on the processor's side. Refunded the duplicate charge and added idempotency keys to the retry logic.

## Interpretation and reproduction

NT-1 concerns missing reset email; password rejection (T-1001) and scheduled-report delivery (T-1403) are not forced into note-bearing results. NT-4 concerns an unfamiliar integration, so related HubSpot metadata is not resolution evidence. NT-2 keyword mode abstains: lexical clause coverage is .431559, below .50, although keyword similarity is .402715. Semantic/hybrid correctly show the empty-chart precedent. No thresholds were changed to obtain these outcomes.

A dash means the value is unavailable/not exposed for that mode or metadata-only candidate, not zero. In particular, related-history API entries do not expose lexical/identifier/RRF scores. These four known synthetic examples are regression demonstrations, not an independent accuracy estimate.

With the backend running from repository root:
```powershell
./.venv/Scripts/python.exe -m scripts.verify_samples
```

The command verifies real model readiness, original notes, unverified labels and expected hybrid IDs. To retain another full report, add `--output sample-check-UNIQUE.json`; existing reports are not overwritten.
