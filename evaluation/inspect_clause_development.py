"""Probe generic clause coverage on development and already-exposed regression only."""
import json
import re
import numpy as np
from backend.retrieval import ROOT, Retriever


def clauses(text):
    pieces=re.split(r'[.!?;]+\s*|\b(?:but|although|however|whereas|yet|and)\b',text,flags=re.I)
    return [p.strip() for p in pieces if len(re.findall(r'\b\w+\b',p))>=4] or [text]


r=Retriever(); assert r.model is not None
cases=json.loads((ROOT/'evaluation/revision-cases.json').read_text())['development']
exposed=json.loads((ROOT/'evaluation/cases.json').read_text())['held_out']
cases += [c for c in exposed if not c['relevant_ids'] and c['id']!='test-aquarium' and c['id']!='test-mobile']
history=[clauses(t.description) for t in r.tickets]
vectors=[r.model.encode(parts,normalize_embeddings=True) for parts in history]
rows=[]
for c in cases:
    text=c['subject']+'\n'+c['description']; full=r.model.encode([text],normalize_embeddings=True)[0]
    sem=r.embeddings@full; parts=clauses(c['description']); q=r.model.encode(parts,normalize_embeddings=True)
    ids=sorted(range(len(sem)),key=lambda i:-sem[i])[:2]
    row={'id':c['id'],'expected':c['relevant_ids'],'clauses':parts,'top':[]}
    for i in ids:
        cover=(q@vectors[i].T).max(axis=1)
        row['top'].append({'id':r.tickets[i].ticket_id,'semantic':round(float(sem[i]),3),'coverage':[round(float(v),3) for v in cover]})
    rows.append(row)
(ROOT/'evaluation/revision-clause-development.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
print(json.dumps(rows,indent=2))
