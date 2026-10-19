import pytest
from backend.evidence import evidence_level, split_clauses, technical_identifiers


def test_keyword_topic_alone_never_endorses_resolution():
    assert evidence_level(.99,None,None)[0]=='related'
    assert evidence_level(.99,.90,.20)[0]=='related'


@pytest.mark.parametrize('semantic,coverage,expected',[(.65,.45,'precedent'),(.649,.9,'related'),(.9,.449,'related'),(.01,.01,'none')])
def test_deterministic_coverage_boundaries(semantic,coverage,expected):
    assert evidence_level(0,semantic,coverage)[0]==expected


def test_identifier_requires_context_and_aligned_clause():
    assert evidence_level(.9,.60,.1,identifier_coverage=.65)[0]=='precedent'
    assert evidence_level(.9,.59,.1,identifier_coverage=.99)[0]=='related'
    assert evidence_level(.9,.9,.1,identifier_coverage=.599)[0]=='related'
    assert evidence_level(.9,.9,.1,False,identifier_coverage=.99)[0]=='related'


def test_context_cap_cannot_be_silently_truncated_into_support():
    assert evidence_level(.9,.99,.99,complete_context=False)[0]=='related'


def test_generic_clauses_and_identifier_extraction():
    assert split_clauses('The operation was requested successfully but the confirmation never reached us.') == [
        'The operation was requested successfully','the confirmation never reached us']
    assert technical_identifiers('HTTP 418 and ERR-12345 on version 12')=={'418','err-12345'}
    assert split_clauses('email missing')==['email missing']
