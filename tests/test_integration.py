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
