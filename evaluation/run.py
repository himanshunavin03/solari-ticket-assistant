"""Reproduce gated retrieval metrics; never tunes on held-out examples."""
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
from backend.retrieval import (ROOT, DATA, MODEL_ID, MODEL_REVISION, KEYWORD_THRESHOLD,
    SEMANTIC_THRESHOLD, Retriever, SearchRequest)
from backend.evidence import POLICY_VERSION, CONTEXT_SIMILARITY, CLAUSE_COVERAGE


def run(split, output):
    preserved = ['results.json','development-results.json','development-initial-results.json','development-evidence.json']
    if output.resolve() in {(ROOT/'evaluation'/name).resolve() for name in preserved}:
        raise ValueError('Original evaluation artifacts are preserved. Choose a new output path or use evaluation.compare_revision.')
    cases_path = ROOT / 'evaluation/cases.json'
    cases = json.loads(cases_path.read_text(encoding='utf-8'))[split]
    retriever = Retriever()
    report = {'timestamp':datetime.now(timezone.utc).isoformat(), 'split':'exposed_regression' if split=='held_out' else split,
        'hardware':{'os':platform.platform(), 'cpu':platform.processor(), 'logical_cpus':os.cpu_count(),
            'python':platform.python_version(), 'torch_threads':4},
        'versions':{name:importlib.metadata.version(name) for name in ['numpy','scikit-learn','sentence-transformers','torch','transformers']},
        'model':MODEL_ID, 'revision':MODEL_REVISION, 'dataset_sha256':hashlib.sha256((DATA/'tickets.json').read_bytes()).hexdigest(),
        'cases_sha256':hashlib.sha256(cases_path.read_bytes()).hexdigest(),
        'policy':{'version':POLICY_VERSION,'context':CONTEXT_SIMILARITY,'clause_coverage':CLAUSE_COVERAGE,'keyword':'related metadata only'}, 'modes':{}}
    for mode in ['keyword', 'semantic', 'hybrid']:
        if mode not in retriever.capabilities:
            report['modes'][mode] = {'status':'unavailable', 'reason':retriever.semantic_failure}
            continue
        rows = []; latencies = []
        # One warmup per query/mode followed by 5 measured warm repetitions.
        for case in cases:
            request = SearchRequest(subject=case['subject'], description=case['description'], mode=mode)
            retriever.search(request)
            for _ in range(5):
                start = time.perf_counter(); result = retriever.search(request)
                latencies.append((time.perf_counter()-start)*1000)
            ids = [m.ticket.ticket_id for m in result.matches]
            relevant = set(case['relevant_ids']); hits = len(set(ids) & relevant)
            rows.append({'id':case['id'], 'expected':sorted(relevant), 'returned':ids,
                'outcome':result.outcome, 'precision_at_3':hits/3 if relevant else None,
                'recall_at_3':hits/len(relevant) if relevant else None,
                'reciprocal_rank':next((1/r for r, tid in enumerate(ids,1) if tid in relevant),0) if relevant else None,
                'scores':[{'id':m.ticket.ticket_id,'keyword':m.keyword_score,'semantic':m.semantic_score,'fusion':m.fusion_score} for m in result.matches]})
        positives = [r for r in rows if r['expected']]; negatives = [r for r in rows if not r['expected']]
        report['modes'][mode] = {'status':'measured',
            'precision_at_3':statistics.mean(r['precision_at_3'] for r in positives),
            'recall_at_3':statistics.mean(r['recall_at_3'] for r in positives),
            'mrr':statistics.mean(r['reciprocal_rank'] for r in positives),
            'no_match_correct_rejections':sum(r['outcome']=='no_reliable_match' for r in negatives),
            'no_match_false_acceptances':sum(r['outcome']=='matches' for r in negatives),
            'no_match_count':len(negatives),
            'positive_false_rejections':sum(r['outcome']=='no_reliable_match' for r in positives),
            'positive_count':len(positives),
            'warm_latency_ms':{'median':statistics.median(latencies), 'p95':float(sorted(latencies)[int(.95*(len(latencies)-1))]), 'sample_count':len(latencies)},
            'cases':rows}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({m:{k:v for k,v in r.items() if k!='cases'} for m,r in report['modes'].items()}, indent=2))


if __name__ == '__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--split', choices=['development','held_out'], default='held_out')
    parser.add_argument('--output',type=Path,default=ROOT/'evaluation/current-results.json')
    args=parser.parse_args(); run(args.split,args.output)
