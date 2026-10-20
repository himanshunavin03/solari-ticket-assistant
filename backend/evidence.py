"""Small, model-independent acceptance policy; no product or ticket-specific rules."""
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

POLICY_VERSION = 'informal-precedent-v6'
CONTEXT_SIMILARITY = 0.65
CLAUSE_COVERAGE = 0.45
MAX_CLAUSES = 8


def split_clauses(text: str) -> list[str]:
    # Common English coordination/contrast markers, not domain-specific phrases.
    # A period within an identifier/version is not a sentence boundary.
    parts = re.split(r'[!?;]+\s*|\.(?=\s|$)|(?<![\w.-])(?:even though|but|although|however|whereas|yet|and)(?![\w.-])', text, flags=re.I)
    return [part.strip() for part in parts if any(char.isalnum() for char in part)]


def query_evidence_text(text: str) -> str:
    """Remove polite request framing only; retain its object and all issue wording.

    For scoring queries, never historical/displayed text. Negated requests do not
    match; e.g. 'please do not check' remains intact. Objects after 'this/that'
    survive, including unfamiliar names, technical identifiers and failure text.
    """
    framing = (r"(?<![\w.-])(?:please|pls|(?:can|could|would)\s+you)\s+"
        r"(?:help(?:\s+me)?|assist(?:\s+me)?|check|validate|investigate|review|look\s+into)"
        r"(?![\w.-])(?:\s+(?:this|that|it)(?![\w.-]))?")
    return re.sub(r'\s+', ' ', re.sub(framing, ' ', text, flags=re.I)).strip()


def content_tokens(text: str) -> set[str]:
    # Filter function words only for lexical coverage, never for displayed text or embeddings.
    # Keep negation and contractions; unknown tokens must not disappear from the denominator.
    stop = ENGLISH_STOP_WORDS - {'no','not','never','cannot','without','nor'}
    return {token for token in re.findall(r"(?u)\b\w+(?:['’.-]\w+)*\b",text.lower()) if token not in stop}


def keyword_clause_coverage(parts: list[str], historical_parts: list[str], idf: dict[str,float]) -> float:
    if not parts or not historical_parts:
        return 0.0
    unknown_weight = max(idf.values(), default=1.0) + 1.0
    historical = [content_tokens(part) for part in historical_parts]
    coverage = []
    for part in parts:
        tokens = content_tokens(part)
        denominator = sum(idf.get(token, unknown_weight) for token in tokens)
        best = max((sum(idf.get(token, unknown_weight) for token in tokens & candidate)
            / denominator if denominator else 0.0) for candidate in historical)
        coverage.append(best)
    return min(coverage)


def technical_identifiers(text: str) -> set[str]:
    # Generic numeric/error identifiers; no product names, IDs, or status-code allowlist.
    return set(re.findall(r'\b[\w.-]*\d{3,}[\w.-]*\b', text.lower()))


def evidence_level(keyword: float, semantic: float | None, coverage: float | None,
                   complete_context: bool = True, identifier_coverage: float | None = None,
                   lexical_coverage: float | None = None, short_context: bool = False) -> tuple[str, str]:
    if (complete_context and semantic is None and keyword >= 0.25
            and lexical_coverage is not None and lexical_coverage >= 0.50):
        return 'precedent', 'Relevant keyword precedent for agent review; applicability is unverified.'
    if (complete_context and semantic is not None and coverage is not None
            and semantic >= CONTEXT_SIMILARITY and coverage >= CLAUSE_COVERAGE):
        return 'precedent', 'Historical issue and retained clauses are similar; applicability is unverified.'
    if (complete_context and semantic is not None and semantic >= 0.60
            and identifier_coverage is not None and identifier_coverage >= 0.60):
        return 'precedent', 'Shared technical identifier and similar symptom clause; applicability is unverified.'
    # Short requests lack the detail of a whole historical ticket. Require the
    # stronger .65 alignment for EVERY clause plus independent lexical overlap;
    # do not make keyword similarity an alternative to semantic evidence.
    if (complete_context and short_context and keyword >= 0.25
            and semantic is not None and semantic >= 0.60
            and coverage is not None and coverage >= CONTEXT_SIMILARITY
            and lexical_coverage is not None and lexical_coverage >= 0.50):
        return 'precedent', 'Short issue has strong clause alignment and lexical corroboration; applicability is unverified.'
    if keyword >= 0.25 or (semantic is not None and semantic >= 0.50):
        return 'related', 'Weak or conflicting related history; insufficient clause relevance to show its resolution.'
    return 'none', 'Insufficient related history.'
