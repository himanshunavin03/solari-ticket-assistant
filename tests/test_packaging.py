"""Submission must remain self-contained while excluding local/internal artifacts."""
import hashlib
import shutil
from zipfile import ZipFile
import pytest
from scripts.package_submission import ROOT, FILES, OPTIONAL_PDF, package, submission_paths


def test_explicit_submission_members_are_complete_and_focused():
    names=submission_paths()
    assert set(names)==set(FILES)|({OPTIONAL_PDF} if (ROOT/OPTIONAL_PDF).is_file() else set())
    assert {'tests/test_evaluation.py','evaluation/metrics.py','evaluation/results.json',
        'evaluation/review_precedents.py','evaluation/baseline_v5/retrieval.py'}<=set(names)
    assert not {'AGENTS.md','PROJECT_STATUS.md','.github/copilot-instructions.md',
        'docs/IMPLEMENTATION_REQUEST.md','docs/AI_ASSISTANCE.md','evaluation/compare_revision.py'} & set(names)


def test_package_is_reproducible_and_does_not_collect_extra_files(tmp_path):
    for name in submission_paths():
        target=tmp_path/name; target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/name,target)
    for name in ['AGENTS.md','PROJECT_STATUS.md','.env','debug.log','evaluation/unlisted-results.json']:
        target=tmp_path/name; target.parent.mkdir(parents=True,exist_ok=True);target.write_text('excluded sentinel')
    archive=package(tmp_path)
    first=hashlib.sha256(archive.read_bytes()).hexdigest()
    with ZipFile(archive) as z:
        assert z.testzip() is None
        assert set(z.namelist())==set(submission_paths())
        assert all(z.read(n)==(ROOT/n).read_bytes() for n in z.namelist())
    package(tmp_path)
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==first


def test_missing_required_member_fails_before_packaging(tmp_path):
    with pytest.raises(RuntimeError,match='Missing required submission file'):
        submission_paths(tmp_path)
