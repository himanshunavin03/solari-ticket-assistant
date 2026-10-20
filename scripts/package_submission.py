"""Explicit, reproducible submission allowlist. Uses only the Python standard library."""
import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    'README.md', 'SOLUTION_DESIGN.md', 'requirements.txt', 'requirements-resolved.txt',
    'requirements-py310-resolved.txt', 'pytest.ini', '.gitignore',
    'backend/__init__.py', 'backend/app.py', 'backend/evidence.py', 'backend/retrieval.py',
    'frontend/package.json', 'frontend/package-lock.json', 'frontend/angular.json',
    'frontend/tsconfig.json', 'frontend/proxy.json', 'frontend/playwright.config.ts',
    'frontend/src/main.ts', 'frontend/src/index.html', 'frontend/src/app.html', 'frontend/src/styles.css',
    'frontend/e2e/smoke.spec.ts',
    'tests/test_api.py', 'tests/test_evaluation.py', 'tests/test_evidence.py',
    'tests/test_focused_corrections.py', 'tests/test_informal.py', 'tests/test_integration.py',
    'tests/test_retrieval.py', 'tests/test_packaging.py',
    'scripts/__init__.py', 'scripts/bootstrap-node.ps1', 'scripts/download_model.py',
    'scripts/prefetch-model.ps1', 'scripts/preflight.py', 'scripts/preflight.ps1',
    'scripts/inspect_data.py', 'scripts/package_submission.py', 'scripts/verify_samples.py',
    'docs/LAUNCHPAD_RUNBOOK.md', 'docs/SUBMISSION_VALIDATION.md', 'docs/SUBMISSION_CONTENTS.md',
    'evaluation/__init__.py', 'evaluation/README.md', 'evaluation/SAMPLE_TICKET_RESULTS.md',
    'evaluation/sample-ticket-results.json', 'evaluation/review_informal.py',
    'evaluation/informal-cases.json', 'evaluation/informal-freeze.json',
    'evaluation/informal-baseline-results.json', 'evaluation/informal-revised-results.json',
    'evaluation/baseline_v5/__init__.py', 'evaluation/baseline_v5/evidence.py',
    'evaluation/baseline_v5/retrieval.py', 'evaluation/metrics.py',
    'evaluation/cases.json', 'evaluation/release-cases.json', 'evaluation/precedent-cases.json',
    'evaluation/data-quality-report.json',
    # These legacy files are necessary for shipped preservation/refusal tests.
    'evaluation/run.py', 'evaluation/results.json', 'evaluation/review_precedents.py',
    'evaluation/precedent-regression-results.json',
    'case-study-1-support-ticket-similarity/case-study-brief.md',
    'case-study-1-support-ticket-similarity/starter_kit/data/tickets.json',
    'case-study-1-support-ticket-similarity/starter_kit/data/new_tickets_example.json',
)
OPTIONAL_PDF = 'docs/SOLUTION_DESIGN.pdf'


def submission_paths(root=ROOT):
    root=Path(root).resolve()
    names=list(FILES)
    if (root/OPTIONAL_PDF).is_file(): names.append(OPTIONAL_PDF)
    if len(names)!=len(set(names)): raise RuntimeError('Duplicate allowlist member')
    for name in names:
        path=root/name
        if not path.is_file(): raise RuntimeError(f'Missing required submission file: {name}')
        if not path.resolve().is_relative_to(root): raise RuntimeError(f'File escapes project root: {name}')
    return sorted(names)


def package(root=ROOT):
    root=Path(root).resolve()
    names=submission_paths(root)
    output=root/'artifacts'; output.mkdir(exist_ok=True)
    archive=output/'solari-ticket-assistant.zip'
    manifest={}
    with ZipFile(archive,'w',ZIP_DEFLATED) as z:
        for name in names:
            data=(root/name).read_bytes()
            info=ZipInfo(name,date_time=(2026,10,17,0,0,0)); info.compress_type=ZIP_DEFLATED
            info.external_attr=0o644 << 16; z.writestr(info,data)
            manifest[name]=hashlib.sha256(data).hexdigest()
    with ZipFile(archive) as z:
        if z.testzip() is not None or sorted(z.namelist())!=names:
            raise RuntimeError('ZIP CRC or membership verification failed')
        if any(hashlib.sha256(z.read(n)).hexdigest()!=digest for n,digest in manifest.items()):
            raise RuntimeError('ZIP/source SHA256 mismatch')
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    (output/'included-files.txt').write_text('\n'.join(names)+'\n',encoding='utf-8')
    print(f'Verified {len(names)} files: {archive} ({archive.stat().st_size} bytes)')
    if OPTIONAL_PDF not in names:
        print(f'PDF not supplied: add the reviewed final PDF at {OPTIONAL_PDF}, then regenerate.')
    return archive


if __name__ == '__main__': package()
