# Demonstration guide

1. Follow README setup, pre-download the model, and run the backend and frontend. Confirm `/api/health` reports all three capabilities.
2. Select the duplicate-charge example. Show the historical ticket ID, original resolution, tags, and expandable description. Explain that the agent still checks customer context before applying the fix.
3. Compare keyword, semantic, and hybrid using the same query. Open technical details to explain cosine versus RRF values; none is percentage accuracy.
4. Select the supplied Snowflake example. Hybrid incorrectly suggests the HubSpot authentication ticket: disclose this false acceptance, then switch to semantic mode, which abstains. For a straightforward no-match UI demonstration, enter “Office delivery” / “A parcel containing a desk lamp was delivered to the wrong building.” Explain why a superficially similar integration ticket is not enough evidence and why thresholds need better representative development data.
5. Clear the form and search blank input to show validation. Discuss unavailable-backend and explicit keyword-only states. Browser tests exercise failure and stale-request behavior.
6. Walk through `SOLUTION_DESIGN.md` and `evaluation/README.md`. Highlight measured errors, strict relevance labels, the small sample, and production gaps.

Likely questions:

- **Why embeddings for 40 tickets?** TF-IDF is the baseline; pretrained embeddings test the value of paraphrase retrieval without training. The measured comparison determines whether the complexity pays off.
- **Why no generated answers?** Original resolutions provide auditable precedent and avoid inventing fixes.
- **Why RRF?** Cosines from different representations are not on a common calibrated scale. Fusion combines ranks, retaining component evidence for inspection.
- **What if the model is unavailable?** Readiness reports keyword-only and semantic/hybrid requests fail explicitly. Agents can choose keyword.
- **What if volume/history grows?** Measure realistic concurrency/history, use access-filtered indexing and background index refresh, then choose persistent/vector retrieval only if needed.
- **How safe is this?** Local prototype with synthetic data; no customer authentication, tenant isolation, production security certification, or scale claim.
- **How trustworthy are the labels?** They were authored with AI assistance after inspecting supplied tickets; not independently reviewed by support agents. Strict issue-level labels expose confusing near matches.
- **What would you do next?** Gather representative agent labels and feedback; improve abstention; test permissions and realistic load.
