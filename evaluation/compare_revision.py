"""Measured reviewed baseline versus revised policy; preserves original result files."""
import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path
from backend import retrieval as revised
from evaluation import frozen_reviewed_retrieval as baseline

ROOT = revised.ROOT


def text_sha(path):
    # Git may convert LF to CRLF on Windows checkout; preserve content provenance.
    return hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()


def metrics(rows, samples):
    positives=[r for r in rows if r['expected']]; negatives=[r for r in rows if not r['expected']]
    return {'positive_count':len(positives),'negative_count':len(negatives),
        'false_acceptances':sum(bool(r['returned']) for r in negatives),
        'false_rejections':sum(not r['returned'] for r in positives),
        'wrong_resolution_on_positive':sum(bool(set(r['returned'])-set(r['expected'])) for r in positives),
        'recall_at_3':statistics.mean(len(set(r['returned'])&set(r['expected']))/len(r['expected']) for r in positives),
        'mrr':statistics.mean(next((1/i for i,tid in enumerate(r['returned'],1) if tid in r['expected']),0) for r in positives),
        'precision_at_3':statistics.mean(len(set(r['returned'])&set(r['expected']))/3 for r in positives),
        'candidate_recall_at_3':statistics.mean(len(set(r['candidates'])&set(r['expected']))/len(r['expected']) for r in positives),
        'warm_latency_ms':{'median':statistics.median(samples),'p95':sorted(samples)[int(.95*(len(samples)-1))],'sample_count':len(samples)}}


def run(split, repetitions=5):
    case_path=ROOT/'evaluation/revision-cases.json'
    freeze=json.loads((ROOT/'evaluation/revision-freeze.json').read_text())
    if text_sha(case_path)!=freeze['cases_sha256']:
        raise RuntimeError('Frozen cases changed; do not silently reuse evaluation claims')
    cases=(json.loads((ROOT/'evaluation/cases.json').read_text())['held_out'] if split=='regression'
        else json.loads((ROOT/'evaluation/release-cases.json').read_text())['fresh'] if split=='release'
        else json.loads((ROOT/'evaluation/final-cases.json').read_text())['fresh'] if split=='final'
        else json.loads(case_path.read_text())[split])
    report={'timestamp':datetime.now(timezone.utc).isoformat(),'split':split,
        'reviewed_commit':'0dbf77d1e9e8ceac1b9130a66c7049f34fbce6f7',
        'cases_sha256':freeze['cases_sha256'],'policy_sha256':text_sha(ROOT/'backend/evidence.py'),
        'hardware':{'os':platform.platform(),'cpu':platform.processor(),'logical_cpus':os.cpu_count(),'python':platform.python_version(),'torch_threads':4},
        'versions':{n:importlib.metadata.version(n) for n in ['numpy','scikit-learn','sentence-transformers','torch','transformers']},
        'model':revised.MODEL_ID,'revision':revised.MODEL_REVISION,'policies':{}}
    report['dataset_sha256']=hashlib.sha256((revised.DATA/'tickets.json').read_bytes()).hexdigest()
    report['baseline_source_sha256']=text_sha(ROOT/'evaluation/frozen_reviewed_retrieval.py')
    if report['baseline_source_sha256']!=freeze['reviewed_baseline_sha256']:
        raise RuntimeError('Reviewed baseline source changed')
    if split=='regression':
        report['cases_sha256']=text_sha(ROOT/'evaluation/cases.json')
    if split=='fresh':
        raise RuntimeError('First fresh set is now exposed and its original result file is preserved. Use final for frozen final cases.')
    if split=='release':
        final_freeze=json.loads((ROOT/'evaluation/release-freeze.json').read_text())
        if (report['policy_sha256']!=final_freeze['policy_sha256'] or text_sha(ROOT/'evaluation/release-cases.json')!=final_freeze['cases_sha256']
                or text_sha(ROOT/'backend/retrieval.py')!=final_freeze['retrieval_sha256']):
            raise RuntimeError('Release cases/policy differ from freeze; comparison is no longer fresh')
        report['cases_sha256']=final_freeze['cases_sha256']
    for name,module in [('baseline',baseline),('revised',revised)]:
        r=module.Retriever()
        if r.model is None: raise RuntimeError(f'{name}: real model required, not available')
        report['policies'][name]={}
        for mode in ['keyword','semantic','hybrid']:
            rows=[]; samples=[]
            for case in cases:
                q=module.SearchRequest(subject=case['subject'],description=case['description'],mode=mode)
                r.search(q)
                for _ in range(repetitions):
                    start=time.perf_counter(); response=r.search(q); samples.append((time.perf_counter()-start)*1000)
                returned=[m.ticket.ticket_id for m in response.matches]
                related=[m.ticket.ticket_id for m in getattr(response,'related_history',[])]
                rows.append({'id':case['id'],'expected':case['relevant_ids'],'returned':returned,'related':related,
                    'candidates':(returned+related)[:3], 'outcome':response.outcome})
            report['policies'][name][mode]={'metrics':metrics(rows,samples),'cases':rows}
    output=ROOT/('evaluation/release-results.json' if split=='release' else f'evaluation/release-{split}-results.json')
    output.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({p:{m:v['metrics'] for m,v in modes.items()} for p,modes in report['policies'].items()},indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--split',choices=['development','regression','release'],required=True)
    args=parser.parse_args(); run(args.split)
