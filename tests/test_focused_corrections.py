"""Regression requirements authored before changing preprocessing or result behavior."""
import json
import pytest
from fastapi.testclient import TestClient
from backend.app import create_app
from backend.evidence import MAX_CLAUSES, split_clauses
from backend.retrieval import DATA, Retriever, SearchRequest, load_tickets


@pytest.mark.parametrize('symptom',['email never arrives','still fails','access denied','not working'])
def test_short_contrasting_failure_is_not_discarded(symptom):
    assert split_clauses('The customer completed the operation successfully but '+symptom+'.') == [
        'The customer completed the operation successfully',symptom]


@pytest.mark.parametrize('text',['','   ','... !!! ; :','() [] ---','___'])
def test_empty_and_punctuation_fragments_provide_no_evidence(text):
    assert split_clauses(text)==[]


def test_identifier_and_negation_preserved_in_scoring_clauses():
    for identifier in ['ERR-12345.v2','HTTP-429-and-retry']:
        assert split_clauses('Build '+identifier+' completed but access denied.') == [
            'Build '+identifier+' completed','access denied']


def test_short_clauses_count_toward_context_limit():
    text=' but '.join(['still fails']*(MAX_CLAUSES+1))
    assert len(split_clauses(text))==MAX_CLAUSES+1
    result=Retriever(semantic=False).search(SearchRequest(subject='Duplicate charges',
        description=' but '.join(['Two identical monthly charges']*(MAX_CLAUSES+1)),mode='keyword'))
    assert not result.matches


def test_degraded_keyword_precedent_has_original_notes_and_uncertainty():
    r=Retriever(semantic=False)
    with TestClient(create_app(r)) as client:
        response=client.post('/api/search',json={'subject':'Duplicate charges',
            'description':'Two identical monthly charges','mode':'keyword'})
        assert response.status_code==200
        body=response.json()
        assert body['outcome']=='historical_precedents'
        assert body['degraded'] and body['active_mode']=='keyword'
        match=body['matches'][0]
        original=next(t for t in r.tickets if t.ticket_id==match['ticket']['ticket_id'])
        assert original.ticket_id=='T-1303'
        assert match['ticket']['resolution_notes']==original.resolution_notes
        assert match['applicability']=='unverified'
        assert match['semantic_score'] is None
        assert 'unverified' in body['evidence_note'].lower()


def test_keyword_weak_failures_do_not_restore_topic_or_gate():
    r=Retriever(semantic=False)
    examples=json.loads((DATA/'new_tickets_example.json').read_text())['new_tickets']
    for example in (examples[0],examples[3]):
        response=r.search(SearchRequest(subject=example['subject'],description=example['description'],mode='keyword'))
        assert not response.matches
        assert response.outcome=='related_history_only'


@pytest.mark.integration
def test_real_model_short_contradiction_and_positive_controls(monkeypatch):
    monkeypatch.setenv('SOLARI_OFFLINE','1')
    r=Retriever()
    assert r.model is not None, r.semantic_failure
    response=r.search(SearchRequest(subject='Password reset issue',
        description='The customer completed the password reset successfully but email never arrives.',mode='hybrid'))
    assert not response.matches, 'Keeping the short clause must affect actual-model retrieval, not just token tests'
    capped=r.search(SearchRequest(subject='Duplicate charges',description=' but '.join(['still fails']*(MAX_CLAUSES+1)),mode='hybrid'))
    assert not capped.matches
    for mode in ['keyword','hybrid']:
        positive=r.search(SearchRequest(subject='Duplicate charges',description='Two identical monthly charges',mode=mode))
        assert positive.matches[0].ticket.ticket_id=='T-1303'
        assert positive.matches[0].applicability=='unverified'


def test_duplicate_content_is_reported_not_removed(tmp_path):
    from backend.retrieval import duplicate_content_groups
    raw=json.loads((DATA/'tickets.json').read_text())['tickets'][0]
    repeated=dict(raw,ticket_id='repeated-incident',description='  '+raw['description']+'  ')
    path=tmp_path/'tickets.json'; path.write_text(json.dumps({'tickets':[raw,repeated]}))
    tickets=load_tickets(path)
    assert len(tickets)==2
    assert duplicate_content_groups(tickets)==[[raw['ticket_id'],'repeated-incident']]
    assert tickets[1].description==repeated['description']


def test_duplicate_inspection_does_not_strip_negation(tmp_path):
    from backend.retrieval import duplicate_content_groups
    raw=json.loads((DATA/'tickets.json').read_text())['tickets'][0]
    a=dict(raw,description='Access is not denied')
    b=dict(raw,ticket_id='different-incident',description='Access is denied')
    path=tmp_path/'tickets.json'; path.write_text(json.dumps({'tickets':[a,b]}))
    assert duplicate_content_groups(load_tickets(path))==[]
