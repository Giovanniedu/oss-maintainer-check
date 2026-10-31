"""Repository hygiene checks used by OSS Maintainer Check.

This module only reads the local filesystem. It does not make network requests.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Check:
    """One transparent, file-presence-based repository check."""

    id: str
    title: str
    passed: bool
    weight: int
    severity: str
    recommendation: str
    evidence: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class Report:
    """Result of running all checks against a repository directory."""

    root: str
    score: int
    checks: tuple[Check, ...]

    @property
    def passed(self) -> int:
        return sum(check.passed for check in self.checks)

    @property
    def total(self) -> int:
        return len(self.checks)

    @property
    def recommendations(self) -> list[Check]:
        return [check for check in self.checks if not check.passed]

    def to_dict(self) -> dict[str, object]:
        return {
            "root": self.root,
            "score": self.score,
            "passed": self.passed,
            "total": self.total,
            "checks": [check.to_dict() for check in self.checks],
        }


def _has_any_file(root: Path, candidates: tuple[str, ...]) -> str | None:
    for candidate in candidates:
        if (root / candidate).is_file():
            return candidate
    return None


def _has_file_in(root: Path, directory: str, suffixes: tuple[str, ...]) -> str | None:
    folder = root / directory
    if not folder.is_dir():
        return None
    files = sorted(
        path for path in folder.rglob("*")
        if path.is_file() and path.suffix.lower() in suffixes
    )
    return str(files[0].relative_to(root)) if files else None


def inspect_repository(root: str | Path) -> Report:
    """Inspect a repository using transparent file-presence checks only."""
    path = Path(root).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Repository path does not exist: {path}")
    if not path.is_dir():
        raise NotADirectoryError(f"Repository path is not a directory: {path}")

    checks: list[Check] = []

    def add(
        check_id: str,
        title: str,
        weight: int,
        severity: str,
        candidates: tuple[str, ...] | None,
        recommendation: str,
        folder: str | None = None,
        suffixes: tuple[str, ...] = (".md", ".yml", ".yaml"),
    ) -> None:
        evidence = (
            _has_file_in(path, folder, suffixes) if folder
            else _has_any_file(path, candidates or ())
        )
        checks.append(Check(
            id=check_id,
            title=title,
            passed=evidence is not None,
            weight=weight,
            severity=severity,
            recommendation=recommendation,
            evidence=evidence or "",
        ))

    add("readme", "Project overview (README)", 20, "high",
        ("README.md", "README.rst", "README.txt", "README"),
        "Add a README explaining the problem, installation, usage, and project status.")
    add("license", "Open-source license", 20, "high",
        ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"),
        "Choose and include a license that clearly grants users the rights you intend.")
    add("contributing", "Contribution guide", 15, "medium",
        ("CONTRIBUTING.md", ".github/CONTRIBUTING.md"),
        "Document how to report bugs, propose changes, and run checks locally.")
    add("code_of_conduct", "Code of conduct", 10, "medium",
        ("CODE_OF_CONDUCT.md", ".github/CODE_OF_CONDUCT.md"),
        "Publish expectations for respectful participation and a reporting route.")
    add("security", "Security reporting policy", 10, "medium",
        ("SECURITY.md", ".github/SECURITY.md"),
        "Explain how to report vulnerabilities privately and what response to expect.")
    add("issue_templates", "Issue templates", 10, "medium", None,
        "Add issue templates so reports include reproducible details.",
        folder=".github/ISSUE_TEMPLATE", suffixes=(".md", ".yml", ".yaml"))
    add("pull_request_template", "Pull request template", 5, "low",
        (".github/PULL_REQUEST_TEMPLATE.md", "PULL_REQUEST_TEMPLATE.md"),
        "Add a short checklist to guide useful, reviewable pull requests.")
    add("ci", "Continuous integration workflow", 10, "medium", None,
        "Run tests and quality checks automatically on pull requests.",
        folder=".github/workflows", suffixes=(".yml", ".yaml"))

    earned = sum(check.weight for check in checks if check.passed)
    return Report(root=str(path), score=earned, checks=tuple(checks))
