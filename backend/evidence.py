"""Small, model-independent acceptance policy; no product or ticket-specific rules."""
import re

POLICY_VERSION = 'clause-coverage-v4'
CONTEXT_SIMILARITY = 0.65
CLAUSE_COVERAGE = 0.45
MAX_CLAUSES = 8


def split_clauses(text: str) -> list[str]:
    # Common English coordination/contrast markers, not domain-specific phrases.
    parts = re.split(r'[.!?;]+\s*|\b(?:even though|but|although|however|whereas|yet|and)\b', text, flags=re.I)
    return [part.strip() for part in parts if len(re.findall(r'\b\w+\b', part)) >= 4] or [text.strip()]


def technical_identifiers(text: str) -> set[str]:
    # Generic numeric/error identifiers; no product names, IDs, or status-code allowlist.
    return set(re.findall(r'\b[\w.-]*\d{3,}[\w.-]*\b', text.lower()))


def evidence_level(keyword: float, semantic: float | None, coverage: float | None,
                   complete_context: bool = True, identifier_coverage: float | None = None) -> tuple[str, str]:
    if (complete_context and semantic is not None and coverage is not None
            and semantic >= CONTEXT_SIMILARITY and coverage >= CLAUSE_COVERAGE):
        return 'supported', 'Overall issue similarity and each retained description clause have historical support.'
    if (complete_context and semantic is not None and semantic >= 0.60
            and identifier_coverage is not None and identifier_coverage >= 0.60):
        return 'supported', 'A shared technical identifier and its symptom clause corroborate the overall issue; other context still needs review.'
    if keyword >= 0.25 or (semantic is not None and semantic >= 0.50):
        return 'related', ('Lexical context only; symptom coverage was not checked.' if semantic is None else
            'Potentially related topic; insufficient coverage to present its resolution as supported evidence.')
    return 'none', 'Insufficient related history.'
