"""Strict validation and non-destructive duplicate-content inspection."""
import hashlib
import json
from backend.retrieval import DATA, ROOT, load_tickets, duplicate_content_groups


def main():
    path=DATA/'tickets.json'; tickets=load_tickets(path)
    report={'dataset_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'record_count':len(tickets),
        'duplicate_content_groups':duplicate_content_groups(tickets),
        'inspection_normalization':'Whitespace collapse and casefold of subject+description only; no punctuation/negation removal.',
        'action':'Report only. Repeated incidents remain separate with original text and IDs; nothing deleted or imputed.'}
    (ROOT/'evaluation/data-quality-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__': main()
