import pytest
from fastapi.testclient import TestClient
from backend.app import create_app
from backend.retrieval import Retriever


@pytest.fixture
def client():
    with TestClient(create_app(Retriever(semantic=False))) as c: yield c


def test_health_and_examples(client):
    assert client.get('/api/health').json()['capabilities'] == ['keyword']
    assert client.get('/api/health').json()['status'] == 'degraded'
    assert len(client.get('/api/examples').json()['new_tickets']) == 4


def test_search_contract(client):
    response = client.post('/api/search', json={'subject':'Duplicate charges', 'description':'Two identical monthly charges', 'mode':'keyword'})
    assert response.status_code == 200
    result = response.json()
    assert result['active_mode'] == 'keyword' and result['degraded']
    assert result['outcome'] == 'historical_precedents'
    assert result['matches'][0]['semantic_score'] is None
    assert result['matches'][0]['ticket']['resolution_notes']
    assert result['matches'][0]['applicability'] == 'unverified'


@pytest.mark.parametrize('patch', [{'subject':' '}, {'top_k':11}, {'mode':'invalid'}, {'description':None}])
def test_validation(client, patch):
    response = client.post('/api/search', json={'subject':'Test','description':'private-ticket-marker'} | patch)
    assert response.status_code == 422
    assert response.json()['error']['code'] == 'invalid_input'
    assert 'private-ticket-marker' not in response.text
    assert 'input' not in response.json()['error']


def test_unavailable_not_no_match(client):
    response = client.post('/api/search', json={'subject':'Test','description':'Test','mode':'hybrid'})
    assert response.status_code == 503
    assert response.json()['error']['code'] == 'capability_unavailable'


def test_no_match_is_success(client):
    response = client.post('/api/search', json={'subject':'zqxwvv', 'description':'qqqzz', 'mode':'keyword'})
    assert response.status_code == 200
    assert response.json()['outcome'] == 'no_relevant_history'
    assert response.json()['matches'] == []


def test_cors(client):
    response = client.options('/api/search', headers={'Origin':'https://untrusted.example','Access-Control-Request-Method':'POST'})
    assert response.status_code == 400
    assert 'access-control-allow-origin' not in response.headers


def test_inference_failure_is_safe():
    retriever = Retriever(semantic=False)
    def broken(*args): raise ValueError('private ticket text must not escape')
    retriever.search = broken
    with TestClient(create_app(retriever), raise_server_exceptions=False) as c:
        response = c.post('/api/search', json={'subject':'Test', 'description':'Test', 'mode':'keyword'})
        assert response.status_code == 503
        assert 'private' not in response.text
