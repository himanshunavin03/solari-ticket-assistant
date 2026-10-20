"""Historical evaluator retained as a safe refusal: result semantics have changed."""
import argparse
from pathlib import Path
from backend.retrieval import ROOT


def run(split, output):
    preserved = ['results.json','development-results.json','development-initial-results.json','development-evidence.json']
    if output.resolve() in {(ROOT/'evaluation'/name).resolve() for name in preserved}:
        raise ValueError('Original evaluation artifacts are preserved. Use evaluation.review_informal with a new output path.')
    raise RuntimeError('Historical evaluator uses obsolete supported-resolution semantics. Use python -m evaluation.review_informal with a new output path.')


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--split',choices=['development','held_out'],default='held_out')
    parser.add_argument('--output',type=Path,default=ROOT/'evaluation/current-results.json')
    args=parser.parse_args()
    run(args.split,args.output)
