import os
import pytest
from backend.retrieval import Retriever, SearchRequest


@pytest.mark.integration
def test_real_model_and_offline_cache(monkeypatch):
    monkeypatch.setenv('SOLARI_OFFLINE', '1')
    r = Retriever()
    assert r.model is not None, r.semantic_failure
    for mode in ['semantic', 'hybrid']:
        response = r.search(SearchRequest(subject='Billed twice', description='Two identical charges on my card for the same subscription month', mode=mode))
        assert response.matches[0].ticket.ticket_id == 'T-1303'
        assert not response.degraded
    assert r.embeddings.shape == (40, 384)


@pytest.fixture(scope='module')
def real_model():
    os.environ['SOLARI_OFFLINE']='1'
    r=Retriever()
    assert r.model is not None, r.semantic_failure
    return r


@pytest.mark.integration
def test_issue_level_no_match_without_leaking_related_resolutions(real_model):
    import json
    from backend.retrieval import DATA
    examples=json.loads((DATA/'new_tickets_example.json').read_text())['new_tickets']
    for example in [examples[0],examples[3]]:
        response=real_model.search(SearchRequest(subject=example['subject'],description=example['description'],mode='hybrid'))
        assert response.outcome=='related_history_only'
        assert not response.matches
        assert response.related_history
        assert all('resolution_notes' not in m.ticket.model_dump() for m in response.related_history)


@pytest.mark.integration
@pytest.mark.parametrize('mode',['semantic','hybrid'])
def test_actual_model_429_with_unchanged_usage(real_model,mode):
    response=real_model.search(SearchRequest(subject='429 errors on integration',
        description='Normal integration traffic is now being rejected with HTTP 429 even though usage did not increase.',mode=mode))
    assert response.matches[0].ticket.ticket_id=='T-1702'
    assert response.matches[0].identifier_coverage is not None


@pytest.mark.integration
@pytest.mark.parametrize('index,expected',[(0,[]),(1,['T-1201']),(2,['T-1303']),(3,[])])
def test_all_supplied_hybrid_examples_through_api(real_model,index,expected):
    import json
    from fastapi.testclient import TestClient
    from backend.app import create_app
    from backend.retrieval import DATA
    ticket=json.loads((DATA/'new_tickets_example.json').read_text(encoding='utf-8'))['new_tickets'][index]
    with TestClient(create_app(real_model)) as client:
        response=client.post('/api/search',json={'subject':ticket['subject'],'description':ticket['description'],'mode':'hybrid'})
        assert response.status_code==200
        matches=response.json()['matches']
        assert [m['ticket']['ticket_id'] for m in matches]==expected
        originals={t.ticket_id:t.resolution_notes for t in real_model.tickets}
        for match in matches:
            assert match['applicability']=='unverified'
            assert match['ticket']['resolution_notes']==originals[match['ticket']['ticket_id']]
