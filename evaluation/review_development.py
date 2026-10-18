"""Inspect development evidence only. Never use held-out cases to select gates."""
import json
from backend.retrieval import ROOT, Retriever, stable_order

r = Retriever()
if r.model is None:
    raise RuntimeError(r.semantic_failure)
cases = json.loads((ROOT/'evaluation/cases.json').read_text())['development']
rows = []
for case in cases:
    text = case['subject']+'\n'+case['description']
    keyword = (r.matrix @ r.vectorizer.transform([text]).T).toarray().ravel()
    semantic = r.embeddings @ r.model.encode([text], normalize_embeddings=True, convert_to_numpy=True)[0]
    row={'id':case['id'], 'expected':case['relevant_ids']}
    for name, scores in [('keyword',keyword),('semantic',semantic)]:
        row[name] = [{'id':r.tickets[i].ticket_id,'score':round(float(scores[i]),5)} for i in stable_order(scores,r.tickets)[:3]]
    rows.append(row)
(ROOT/'evaluation/development-evidence.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
print(json.dumps(rows,indent=2))
