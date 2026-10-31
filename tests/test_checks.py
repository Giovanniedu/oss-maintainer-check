import json
from pathlib import Path

import pytest

from oss_maintainer_check.checks import inspect_repository
from oss_maintainer_check.cli import main


def test_empty_repository_gets_zero_and_eight_recommendations(tmp_path: Path) -> None:
    report = inspect_repository(tmp_path)
    assert report.score == 0
    assert report.total == 8
    assert len(report.recommendations) == 8


def test_complete_repository_scores_one_hundred(tmp_path: Path) -> None:
    for filename in (
        "README.md", "LICENSE", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md",
        "SECURITY.md", ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/ISSUE_TEMPLATE/bug.yml", ".github/workflows/test.yml",
    ):
        path = tmp_path / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("placeholder\n", encoding="utf-8")

    report = inspect_repository(tmp_path)
    assert report.score == 100
    assert report.passed == report.total == 8
    assert report.recommendations == []


def test_alternative_license_and_nested_workflow_are_detected(tmp_path: Path) -> None:
    (tmp_path / "COPYING").write_text("license", encoding="utf-8")
    workflow = tmp_path / ".github/workflows/ci/check.yaml"
    workflow.parent.mkdir(parents=True)
    workflow.write_text("name: CI", encoding="utf-8")

    report = inspect_repository(tmp_path)
    by_id = {check.id: check for check in report.checks}
    assert by_id["license"].passed
    assert by_id["ci"].passed


def test_non_directory_path_is_rejected(tmp_path: Path) -> None:
    file_path = tmp_path / "not-a-folder"
    file_path.write_text("x", encoding="utf-8")
    with pytest.raises(NotADirectoryError):
        inspect_repository(file_path)


def test_json_output_and_fail_threshold(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(tmp_path), "--format", "json", "--fail-below", "50"]) == 1
    output = json.loads(capsys.readouterr().out)
    assert output["score"] == 0
    assert output["total"] == 8


def test_missing_path_returns_error(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    missing = tmp_path / "does-not-exist"
    assert main([str(missing)]) == 2
    assert "error:" in capsys.readouterr().err
