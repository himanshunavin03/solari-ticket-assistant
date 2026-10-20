"""Informal query regression requirements, written before policy change."""
import pytest
from backend import evidence
from backend.retrieval import Retriever, SearchRequest


@pytest.mark.parametrize('source,expected',[
    ('still fails please investigate','still fails'),
    ('i charged twice please validate this transaction','i charged twice transaction'),
    ('can you check this email never arrives','email never arrives'),
    ('please help me access denied','access denied'),
    ('please check this ERR-12345.v2 is not working','ERR-12345.v2 is not working'),
    ('please do not validate this request','please do not validate this request'),
    ('not working','not working'),
    ('please help',''),
])
def test_request_framing_retains_objects_and_symptoms(source,expected):
    assert evidence.query_evidence_text(source)==expected


def test_short_route_requires_all_corroboration():
    def level(k=.3,s=.62,c=.7,lex=.6,short=True,complete=True):
        return evidence.evidence_level(k,s,c,complete_context=complete,
            lexical_coverage=lex,short_context=short)[0]
    assert level()=='precedent'
    for args in [dict(k=.249),dict(s=.599),dict(c=.649),dict(lex=.499),dict(short=False),dict(complete=False)]:
        assert level(**args)=='related'
    # The existing global threshold remains in force outside this narrow route.
    assert evidence.evidence_level(.9,.649,.9)[0]=='related'


@pytest.mark.integration
def test_actual_model_reported_informal_request(monkeypatch):
    monkeypatch.setenv('SOLARI_OFFLINE','1')
    r=Retriever(); assert r.model is not None,r.semantic_failure
    for mode in ['semantic','hybrid']:
        response=r.search(SearchRequest(subject='i charged twice',
            description='i charged twice please validate this transaction',mode=mode))
        assert [m.ticket.ticket_id for m in response.matches]==['T-1303']
        assert response.matches[0].applicability=='unverified'
        assert response.matches[0].ticket.resolution_notes==next(t.resolution_notes for t in r.tickets if t.ticket_id=='T-1303')


def test_curly_apostrophe_and_negation_survive():
    assert "isn’t" in evidence.content_tokens("please check this service isn’t working")


@pytest.mark.integration
def test_actual_model_informal_negative_regressions(monkeypatch):
    import json
    from backend.retrieval import ROOT
    monkeypatch.setenv('SOLARI_OFFLINE','1')
    r=Retriever(); assert r.model is not None,r.semantic_failure
    cases=json.loads((ROOT/'evaluation/informal-cases.json').read_text(encoding='utf-8'))['cases']
    for c in cases:
        if c['relevant_ids']:
            continue
        for mode in ['keyword','hybrid']:
            response=r.search(SearchRequest(subject=c['subject'],description=c['description'],mode=mode))
            assert not response.matches,(c['id'],mode,[m.ticket.ticket_id for m in response.matches])


def test_preserved_v5_report_refuses_new_policy():
    from evaluation.review_precedents import run
    with pytest.raises(RuntimeError,match='Preserved v5 report'):
        run()
