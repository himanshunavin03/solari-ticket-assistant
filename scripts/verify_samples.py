"""Verify unchanged supplied examples through a running API and record real responses."""
import argparse
import hashlib
import json
import platform
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from backend.retrieval import ROOT, DATA, MODEL_ID, MODEL_REVISION
from backend.evidence import POLICY_VERSION


def verify(base_url, output=None):
    with urlopen(base_url+'/api/health', timeout=15) as response:
        health=json.load(response)
    if (health['status']!='ready' or set(health['capabilities'])!={'keyword','semantic','hybrid'}
            or health['model_revision']!=MODEL_REVISION or health['model_id']!=MODEL_ID):
        raise RuntimeError('Real pinned model and all three capabilities required')
    examples=json.loads((DATA/'new_tickets_example.json').read_text(encoding='utf-8'))['new_tickets']
    history={t['ticket_id']:t for t in json.loads((DATA/'tickets.json').read_text(encoding='utf-8'))['tickets']}
    rows=[]
    expected={'NT-1':[], 'NT-2':['T-1201'], 'NT-3':['T-1303'], 'NT-4':[]}
    failures=[]
    for ticket in examples:
        for mode in ['keyword','semantic','hybrid']:
            body={'subject':ticket['subject'],'description':ticket['description'],'mode':mode,'top_k':3}
            request=Request(base_url+'/api/search',data=json.dumps(body).encode('utf-8'),headers={'Content-Type':'application/json'})
            with urlopen(request,timeout=30) as response:
                result=json.load(response)
            if result['policy_version']!=POLICY_VERSION:
                raise RuntimeError('API is running a different policy; restart it before recording results')
            for match in result['matches']:
                assert match['ticket']['resolution_notes']==history[match['ticket']['ticket_id']]['resolution_notes']
                assert match['applicability']=='unverified'
            ids=[m['ticket']['ticket_id'] for m in result['matches']]
            if mode=='hybrid' and ids!=expected[ticket['ticket_id']]:
                failures.append({'id':ticket['ticket_id'],'expected':expected[ticket['ticket_id']],'actual':ids})
            rows.append({'id':ticket['ticket_id'],'input':body,'response':result})
    report={'timestamp':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),'health':health,
        'policy':POLICY_VERSION,'sample_sha256':hashlib.sha256((DATA/'new_tickets_example.json').read_bytes()).hexdigest(),
        'rows':rows,'hybrid_expectation_failures':failures}
    if output:
        output=ROOT/'evaluation'/output
        if output.name!=str(output.relative_to(ROOT/'evaluation')) or output.exists():
            raise ValueError('Choose a new filename within evaluation; existing reports are preserved')
        output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'requests':len(rows),'hybrid_expectation_failures':failures},indent=2))
    if failures: raise RuntimeError('Sample behavior differs; inspect the recorded report')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--base-url',default='http://127.0.0.1:8000')
    parser.add_argument('--output',help='New JSON filename in evaluation; omit to check without writing')
    args=parser.parse_args(); verify(args.base_url.rstrip('/'),args.output)
