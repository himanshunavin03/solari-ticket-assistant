"""Small, model-independent acceptance policy; no product or ticket-specific rules."""
import re

POLICY_VERSION = 'clause-coverage-v2'
CONTEXT_SIMILARITY = 0.65
CLAUSE_COVERAGE = 0.45
MAX_CLAUSES = 8


def split_clauses(text: str) -> list[str]:
    # Common English coordination/contrast markers, not domain-specific phrases.
    parts = re.split(r'[.!?;]+\s*|\b(?:even though|but|although|however|whereas|yet|and)\b', text, flags=re.I)
    return [part.strip() for part in parts if len(re.findall(r'\b\w+\b', part)) >= 4] or [text.strip()]


def evidence_level(keyword: float, semantic: float | None, coverage: float | None,
                   complete_context: bool = True) -> tuple[str, str]:
    if (complete_context and semantic is not None and coverage is not None
            and semantic >= CONTEXT_SIMILARITY and coverage >= CLAUSE_COVERAGE):
        return 'supported', 'Overall issue similarity and each retained description clause have historical support.'
    if keyword >= 0.25 or (semantic is not None and semantic >= 0.50):
        return 'related', ('Lexical context only; symptom coverage was not checked.' if semantic is None else
            'Potentially related topic; insufficient coverage to present its resolution as supported evidence.')
    return 'none', 'Insufficient related history.'
