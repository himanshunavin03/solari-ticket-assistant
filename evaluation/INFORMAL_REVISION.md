# Informal-request correction (v5 → v6)

## Reproduction and exact rule

Actual cached pinned MiniLM, Windows Python 3.11.9, CPU: subject `i charged twice`, description `i charged twice please validate this transaction` retrieves T-1303 but v5 withholds its notes.

| Feature | Original v5 | Revised v6 |
| --- | --- | --- |
| Keyword similarity | .262235 | .262235 |
| Whole-ticket semantic similarity | .559230 | .642657 |
| Minimum query-clause alignment | .606230 | .723596 |
| Lexical clause coverage | Not used in hybrid | .666667 |
| Outcome | Related history only | Historical precedent, applicability unverified |

The failed original requirement was **overall semantic >=.65**, not clause coverage (which passed >=.45). There was no shared technical identifier for the alternate >=.60 identifier route. Keyword similarity alone could not approve notes. The generic fallback reason mentions clause relevance but is not a reliable diagnosis of which gate failed; inspect all scores/rules.

Exploration also found that removing the request phrase alone is insufficient: repeating only the short symptom scores .649089 against the whole ticket, still below .65. The symptom itself aligns .706571 with the historical subject. This motivates clause-based corroboration for short requests rather than a global cutoff decrease.

## Small policy change, unchanged result meaning

`query_evidence_text` removes English polite request framing (`please`/`pls` or `can/could/would you`, followed by check/validate/investigate/review/help/assist/look into). It retains the object, identifiers, unfamiliar names, symptoms and negation; for example the reported description becomes `i charged twice transaction`. Negated instructions such as `please do not validate` remain intact. Only query scoring changes; stored/displayed data and original notes are unchanged. This is a limited English pattern, not general grammar correction or contradiction detection.

Existing whole-ticket .65/clause .45 and corroborated-identifier .60 rules remain unchanged. A **new conjunctive short-context route** requires 2–12 distinct meaningful query tokens, complete context, keyword >=.25, whole-ticket semantic >=.60, **every retained description clause >=.65**, and every clause's IDF-weighted lexical coverage >=.50. It cannot use keyword similarity as an OR alternative. Raw and normalized clause counts enforce the existing eight-clause limit. Objects/unknown tokens remain in the lexical denominator. Keyword-only uses its existing .25/.50 policy on the same cleaned query. Policy/cache version is `informal-precedent-v6`; model, dependencies and runtimes unchanged.

All notes remain **unverified historical precedent for agent review**, not verified root cause or confirmed resolution applicability. No product names, ticket IDs, billing vocabulary or reported query literals occur in the policy.

## Comparable actual-model before/after

`informal-cases.json` froze 18 exposed cases (8 positive / 10 confusing negative) before policy implementation; `informal-freeze.json` records time, case hash and original source hashes. These are AI-authored synthetic diagnostic labels, not independent or untouched tests. Three earlier inspected splits are also exposed regression. Identical displayed-precedent definitions, inputs and pinned model are used in `informal-baseline-results.json` and `informal-revised-results.json`. Earlier evaluation files remain untouched. The first v6 run is retained separately; a diff review corrected accidental Unicode encoding in the curly-apostrophe tokenizer, and final source/case hashes were verified. There was no relevance-threshold retuning after results.

| Informal set | Recall@3 / MRR before → after | Positive abstentions | Negatives displaying notes |
| --- | --- | --- | --- |
| Keyword | .250 → .375 | 6/8 → 5/8 | 0/10 → 0/10 |
| Semantic | .625 → .875 | 3/8 → 1/8 | 0/10 → 0/10 |
| Hybrid | .625 → .875 | 3/8 → 1/8 | 0/10 → 0/10 |

The reported case and bare informal symptom gain notes in semantic/hybrid; the other five previously correct informal positives remain correct. No irrelevant extras on informal positives. Refund-status, negated duplicate charge, phone charging, legitimate separate purchases, unfamiliar integration, missing reset email, contradictory short failure, vague help, negated 429 and parcel negatives withhold notes.

**Remaining failure:** `api 429` / `integration keeps returning HTTP 429 please investigate` remains related-only, missing expected T-1702. No further tuning was done to remove it. Existing explicit HTTP 429 control still passes. Earlier original (8/4), previous-release (8/4) and targeted (4/3) relevance/error metrics are unchanged across all modes: semantic/hybrid Recall@3/MRR1.0; keyword .25/.375/.5 respectively. Zero negative note presentations there does not imply perfect precision: the known short login-failure query still displays irrelevant T-1004 alongside correct T-1001. MiniLM/lexical agreement cannot prove negation or mechanism equivalence. Small synthetic negatives cannot bound production false-match rates; broadening short-request eligibility may increase unseen false matches.

Latency samples and runtime/source/data provenance are in the reports. Some evaluation phases overlapped separate compatibility tests and running dev servers; timings are not controlled speed comparisons, throughput or SLA evidence.

## Actual checks and reproduction commands

Before behavior change: 10 targeted tests failed. Final full backend suite: **75 passed on Python 3.11.9 and 75 on 3.10.11**, including actual model, deterministic boundaries, generic request preservation, Unicode negation, confusing negatives, Snowflake/missing-email and billing/429 controls. One nonfatal Starlette/AnyIO warning each. No Launchpad3.10.0 claim. Prior browser results remain historical; this backend-only correction did not rerun browser automation. The restarted live API and Angular proxy returned the revised reported match and all capabilities ready.

```powershell
$env:SOLARI_OFFLINE = '1'
./.venv/Scripts/python.exe -m pytest -q
./.venv/Scripts/python.exe -m evaluation.review_informal --output "informal-check-$(Get-Date -Format yyyyMMdd-HHmmss)-results.json"
```

The evaluator verifies frozen case bytes and refuses existing output paths. `evaluation.review_precedents` refuses v6 so it cannot overwrite the preserved v5 report. All cases are exposed regressions on rerun. No new dependencies, runtime changes, commit or push.
