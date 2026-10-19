"""Allowlisted reproducible ZIP, verified against source bytes after creation."""
import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo
from backend.retrieval import ROOT

DIRECTORIES = ['backend', 'tests', 'scripts', 'evaluation', 'docs', '.github', 'case-study-1-support-ticket-similarity']
ROOT_FILES = ['README.md', 'SOLUTION_DESIGN.md', 'AGENTS.md', 'PROJECT_STATUS.md', 'requirements.txt',
    'requirements-resolved.txt', 'requirements-py310-resolved.txt', 'pytest.ini', '.gitignore']
FRONTEND_FILES = ['package.json','package-lock.json','angular.json','tsconfig.json','proxy.json','playwright.config.ts']
SKIP = {'__MACOSX','__pycache__','.pytest_cache','node_modules','.angular','dist','.git','.venv','.cache'}


def package():
    paths = [ROOT/p for p in ROOT_FILES if (ROOT/p).is_file()]
    for folder in DIRECTORIES + ['frontend/src','frontend/e2e']:
        paths.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and not set(p.relative_to(ROOT).parts)&SKIP
            and p.suffix in {'.py','.json','.md','.txt','.ps1','.ts','.html','.css'})
    paths.extend(ROOT/'frontend'/p for p in FRONTEND_FILES)
    required = ['README.md','SOLUTION_DESIGN.md','frontend/package-lock.json','evaluation/results.json',
        'evaluation/release-results.json','evaluation/release-freeze.json','requirements-py310-resolved.txt','scripts/preflight.ps1',
        'evaluation/precedent-regression-results.json','evaluation/data-quality-report.json','docs/LAUNCHPAD_RUNBOOK.md',
        'case-study-1-support-ticket-similarity/starter_kit/data/tickets.json']
    names = {p.relative_to(ROOT).as_posix() for p in paths}
    if not set(required) <= names: raise RuntimeError('Missing required submission artifacts')
    output = ROOT/'artifacts'; output.mkdir(exist_ok=True)
    archive = output/'solari-ticket-assistant.zip'
    manifest = {}
    with ZipFile(archive,'w',ZIP_DEFLATED) as z:
        for path in sorted(set(paths)):
            name = path.relative_to(ROOT).as_posix(); data = path.read_bytes()
            info=ZipInfo(name, date_time=(2026,10,17,0,0,0)); info.compress_type=ZIP_DEFLATED
            info.external_attr=0o644 << 16; z.writestr(info,data)
            manifest[name] = hashlib.sha256(data).hexdigest()
    with ZipFile(archive) as z:
        assert z.testzip() is None
        assert set(z.namelist()) == set(manifest)
        assert all(not set(Path(n).parts)&SKIP for n in z.namelist())
        assert all(hashlib.sha256(z.read(n)).hexdigest()==digest for n,digest in manifest.items())
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(f'Verified {len(manifest)} files: {archive} ({archive.stat().st_size} bytes)')


if __name__ == '__main__': package()
