"""Legacy metric definitions retained for denominator/provenance tests."""
import statistics


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

