"""Current regression metrics for displayed unverified precedent, not root-cause verification."""
import hashlib
import importlib.metadata
import json
import os
import platform
import statistics
import time
from collections import Counter
from pathlib import Path
from datetime import datetime, timezone
from backend.retrieval import ROOT, DATA, Retriever, SearchRequest, MODEL_ID, MODEL_REVISION
from backend.evidence import POLICY_VERSION


def run(output):
    if Path(output).name != output or not output.startswith('informal-') or not output.endswith('-results.json'):
        raise ValueError('Use an informal-*-results.json filename')
    output=ROOT/'evaluation'/output
    if output.exists():
        raise ValueError('Use a new output filename; never overwrite preserved results')
    freeze=json.loads((ROOT/'evaluation/informal-freeze.json').read_text(encoding='utf-8'))
    if hashlib.sha256((ROOT/'evaluation/informal-cases.json').read_bytes()).hexdigest()!=freeze['cases_sha256']:
        raise ValueError('Frozen informal case hash mismatch')
    sources={'original_exposed':('cases.json','held_out'), 'previous_release_now_exposed':('release-cases.json','fresh'),
        'targeted_exposed':('precedent-cases.json','cases'), 'informal_exposed':('informal-cases.json','cases')}
    retriever=Retriever()
    if retriever.model is None: raise RuntimeError('Actual pinned model required for semantic/hybrid regression')
    report={'timestamp':datetime.now(timezone.utc).isoformat(),'policy':POLICY_VERSION,
        'result_semantics':'historical-precedent-v1',
        'warning':'Metrics measure displayed historical resolution relevance for review, never verified root cause. All cases exposed; not directly equivalent to earlier supported-resolution metrics.',
        'model':MODEL_ID,'revision':MODEL_REVISION,'dataset_sha256':hashlib.sha256((DATA/'tickets.json').read_bytes()).hexdigest(),
        'code_sha256':{name:hashlib.sha256((ROOT/'backend'/name).read_bytes()).hexdigest() for name in ['evidence.py','retrieval.py']},
        'hardware':{'python':platform.python_version(),'os':platform.platform(),'cpu':platform.processor(),'logical_cpus':os.cpu_count(),'torch_threads':4},
        'versions':{n:importlib.metadata.version(n) for n in ['numpy','scikit-learn','sentence-transformers','transformers','torch']},'splits':{}}
    for split,(filename,key) in sources.items():
        path=ROOT/'evaluation'/filename
        cases=json.loads(path.read_text(encoding='utf-8'))[key]
        modes={}
        for mode in ['keyword','semantic','hybrid']:
            rows=[]; samples=[]
            for c in cases:
                q=SearchRequest(subject=c['subject'],description=c['description'],mode=mode)
                retriever.search(q)
                for _ in range(5):
                    start=time.perf_counter(); result=retriever.search(q); samples.append((time.perf_counter()-start)*1000)
                ids=[m.ticket.ticket_id for m in result.matches]
                related=[m.ticket.ticket_id for m in result.related_history]
                rows.append({'id':c['id'],'expected':c['relevant_ids'],'displayed_precedents':ids,'related_metadata':related,
                    'outcome':result.outcome,'applicability':'unverified',
                    'scores':[{'id':m.ticket.ticket_id,'keyword':m.keyword_score,'semantic':m.semantic_score,
                        'clause_coverage':m.clause_coverage,'lexical_clause_coverage':m.lexical_clause_coverage} for m in result.matches]})
            positives=[r for r in rows if r['expected']]; negatives=[r for r in rows if not r['expected']]
            metrics={'positive_count':len(positives),'negative_count':len(negatives),
                'irrelevant_precedent_presentations':sum(bool(r['displayed_precedents']) for r in negatives),
                'positive_precedent_abstentions':sum(not r['displayed_precedents'] for r in positives),
                'positive_with_irrelevant_precedents':sum(bool(set(r['displayed_precedents'])-set(r['expected'])) for r in positives),
                'precedent_precision_at_3':statistics.mean(len(set(r['displayed_precedents'])&set(r['expected']))/3 for r in positives),
                'precedent_recall_at_3':statistics.mean(len(set(r['displayed_precedents'])&set(r['expected']))/len(r['expected']) for r in positives),
                'precedent_mrr':statistics.mean(next((1/i for i,tid in enumerate(r['displayed_precedents'],1) if tid in r['expected']),0) for r in positives),
                'outcomes':dict(Counter(r['outcome'] for r in rows)),
                'warm_latency_ms':{'median':statistics.median(samples),'p95':sorted(samples)[int(.95*(len(samples)-1))],'samples':len(samples)}}
            modes[mode]={'metrics':metrics,'cases':rows}
        report['splits'][split]={'cases_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'modes':modes}
    output.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({s:{m:v['metrics'] for m,v in r['modes'].items()} for s,r in report['splits'].items()},indent=2))


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True)
    run(parser.parse_args().output)
