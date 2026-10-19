"""Development diagnostics only; never opens the frozen fresh partition."""
import json
import numpy as np
from backend.retrieval import ROOT, Retriever

r = Retriever()
assert r.model is not None, r.semantic_failure
cases = json.loads((ROOT/'evaluation/revision-cases.json').read_text())['development']
descriptions = r.model.encode([t.description for t in r.tickets], normalize_embeddings=True)
subjects = r.model.encode([t.subject for t in r.tickets], normalize_embeddings=True)
rows=[]
for case in cases:
    text=case['subject']+'\n'+case['description']
    k=(r.matrix @ r.vectorizer.transform([text]).T).toarray().ravel()
    full, desc, subject = r.model.encode([text,case['description'],case['subject']],normalize_embeddings=True)
    s=r.embeddings @ full; d=descriptions @ desc
    u=subjects @ subject
    ids=sorted(range(len(k)),key=lambda i:-s[i])[:3]
    row={'id':case['id'],'expected':case['relevant_ids'],'top':[{'id':r.tickets[i].ticket_id,'k':round(float(k[i]),3),'s':round(float(s[i]),3),'description':round(float(d[i]),3),'subject':round(float(u[i]),3)} for i in ids]}
    rows.append(row)
(ROOT/'evaluation/revision-development-evidence.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
print(json.dumps(rows,indent=2))
