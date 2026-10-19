import json
import numpy as np
import pytest
from pydantic import ValidationError
from backend.retrieval import (DATA, Retriever, SearchRequest, load_tickets, cache_key,
    reciprocal_rank_fusion, stable_order)


@pytest.fixture
def keyword():
    return Retriever(semantic=False)


def request(subject='Charged twice for the same billing cycle', description='Two identical monthly charges on card statement', **kwargs):
    return SearchRequest(subject=subject, description=description, **kwargs)


def test_valid_data_and_keyword_match(keyword):
    assert len(keyword.tickets) == 40
    response = keyword.search(request(mode='keyword'))
    assert response.matches[0].ticket.ticket_id == 'T-1303'
    assert response.outcome == 'historical_precedents'
    assert response.matches[0].applicability == 'unverified'
    assert response.degraded


@pytest.mark.parametrize('mutation', ['duplicate', 'missing', 'wrong_type', 'blank', 'empty', 'shape'])
def test_invalid_data(tmp_path, mutation):
    raw = json.loads((DATA / 'tickets.json').read_text())
    if mutation == 'duplicate': raw['tickets'].append(raw['tickets'][0])
    if mutation == 'missing': del raw['tickets'][0]['resolution_notes']
    if mutation == 'wrong_type': raw['tickets'][0]['tags'] = 'not a list'
    if mutation == 'blank': raw['tickets'][0]['ticket_id'] = ' '
    if mutation == 'empty': raw['tickets'] = []
    if mutation == 'shape': raw = []
    path = tmp_path / 'tickets.json'
    path.write_text(json.dumps(raw))
    with pytest.raises(ValueError, match='Invalid historical dataset'):
        load_tickets(path)


@pytest.mark.parametrize('kwargs', [dict(subject=' '), dict(description='\n'), dict(top_k=0), dict(top_k=11),
    dict(top_k=True), dict(mode='bad'), dict(subject='x'*301), dict(description='x'*10001), dict(subject=4)])
def test_invalid_request(kwargs):
    values = dict(subject='Subject', description='Description') | kwargs
    with pytest.raises(ValidationError): SearchRequest(**values)


def test_oov_and_no_match(keyword):
    for text in ('zqxwvv qqqzz', 'My aquarium filter has broken and fish need feeding'):
        response = keyword.search(request(subject=text, description=text, mode='keyword'))
        assert response.outcome == 'no_relevant_history'
        assert response.matches == []


def test_ties_and_rrf(keyword):
    zeros = np.zeros(40)
    assert [keyword.tickets[i].ticket_id for i in stable_order(zeros, keyword.tickets)] == sorted(t.ticket_id for t in keyword.tickets)
    assert np.all(reciprocal_rank_fusion(zeros, None, keyword.tickets) == 0)
    a = np.zeros(40); a[2] = .8; a[3] = .7
    b = np.zeros(40); b[3] = .9; b[2] = .8
    fused = reciprocal_rank_fusion(a, b, keyword.tickets)
    assert fused[2] == fused[3] == pytest.approx(1/61 + 1/62)
    assert fused[0] == 0


def test_keyword_identifiers_and_top_k(keyword):
    assert '429' in keyword.vectorizer.vocabulary_
    result = keyword.search(request(subject='API returns 429 rate limit', description='Integration started receiving 429 errors', mode='keyword', top_k=1))
    assert len(result.matches) == 1
    assert result.matches[0].ticket.ticket_id == 'T-1702'


def test_unavailable_capabilities(keyword):
    assert keyword.capabilities == ['keyword']
    for mode in ['semantic', 'hybrid']:
        with pytest.raises(RuntimeError): keyword.search(request(mode=mode))


class FakeModel:
    """For cache behavior only; this is not semantic integration evidence."""
    def __init__(self): self.calls = 0
    def encode(self, texts, **kwargs):
        self.calls += 1
        return np.tile([1., 0., 0.], (len(texts), 1))


def test_cache_reuse_invalidation_and_corruption(tmp_path):
    a = FakeModel(); Retriever(model=a, cache_dir=tmp_path)
    assert a.calls == 1
    b = FakeModel(); Retriever(model=b, cache_dir=tmp_path)
    assert b.calls == 0
    cache = next(tmp_path.glob('*.npy')); cache.write_bytes(b'broken')
    c = FakeModel(); Retriever(model=c, cache_dir=tmp_path)
    assert c.calls == 1
    data = (DATA / 'tickets.json').read_bytes()
    keys = {cache_key(data), cache_key(data+b' '), cache_key(data, revision='other'),
        cache_key(data, model_id='other'), cache_key(data, preprocessing='v2')}
    assert len(keys) == 5
    changed = tmp_path / 'changed.json'
    changed.write_bytes(data + b' ')
    d = FakeModel(); Retriever(path=changed, model=d, cache_dir=tmp_path)
    assert d.calls == 1
    assert len(list(tmp_path.glob('*.npy'))) == 2


def test_model_initialization_failure_keeps_keyword(tmp_path):
    class Broken:
        def encode(self, *args, **kwargs): raise OSError('unavailable')
    r = Retriever(model=Broken(), cache_dir=tmp_path)
    assert r.model is None and r.semantic_failure
    assert r.search(request(mode='keyword')).matches
