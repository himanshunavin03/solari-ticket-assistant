import pytest
from backend.retrieval import ROOT
from evaluation.run import run
from evaluation.compare_revision import metrics


def test_original_results_cannot_be_overwritten():
    original=ROOT/'evaluation/results.json'
    before=original.read_bytes()
    with pytest.raises(ValueError,match='preserved'):
        run('held_out',original)
    assert original.read_bytes()==before


def test_metrics_keep_related_context_out_of_supported_recall():
    rows=[{'expected':['A','B'],'returned':['A'],'candidates':['A','B']},
        {'expected':['C'],'returned':[],'candidates':['C']},
        {'expected':[],'returned':['Z'],'candidates':['Z']}]
    result=metrics(rows,[1,2,3,4,5])
    assert result['recall_at_3']==.25
    assert result['mrr']==.5
    assert result['precision_at_3']==pytest.approx(1/6)
    assert result['candidate_recall_at_3']==1
    assert result['false_acceptances']==1 and result['false_rejections']==1
