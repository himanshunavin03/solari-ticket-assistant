import pytest
from backend.retrieval import ROOT
from evaluation.run import run
from evaluation.metrics import metrics


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


def test_shipped_v5_snapshot_matches_recorded_baseline():
    import json
    import hashlib
    freeze=json.loads((ROOT/'evaluation/informal-freeze.json').read_text(encoding='utf-8'))
    for name in ['evidence.py','retrieval.py']:
        text=(ROOT/'evaluation/baseline_v5'/name).read_text(encoding='utf-8')
        if name=='retrieval.py':
            text=text.replace('from evaluation.baseline_v5.evidence import','from backend.evidence import')
            text=text.replace('ROOT = Path(__file__).resolve().parents[2]','ROOT = Path(__file__).resolve().parents[1]')
        assert hashlib.sha256(text.encode('utf-8')).hexdigest()==freeze['baseline_code_sha256'][name]
