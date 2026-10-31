"""Command-line interface for OSS Maintainer Check."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .checks import Report, inspect_repository


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="oss-maintainer-check",
        description="Audit basic open-source repository maintenance files locally.",
    )
    parser.add_argument("path", nargs="?", default=".", help="repository directory (default: current directory)")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="output format")
    parser.add_argument(
        "--fail-below", type=int, default=None, metavar="0-100",
        help="exit with status 1 when the score is below this threshold",
    )
    return parser


def render_text(report: Report) -> str:
    lines = [
        f"OSS Maintainer Check — {report.root}",
        f"Score: {report.score}/100 ({report.passed}/{report.total} checks passed)",
        "",
    ]
    for check in report.checks:
        marker = "PASS" if check.passed else "TODO"
        evidence = f" — {check.evidence}" if check.evidence else ""
        lines.append(f"[{marker}] {check.title}{evidence}")
        if not check.passed:
            lines.append(f"       {check.recommendation}")
    lines += ["", "Note: this is a file-presence checklist, not a quality, security, or popularity assessment."]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.fail_below is not None and not 0 <= args.fail_below <= 100:
        _parser().error("--fail-below must be between 0 and 100")

    try:
        report = inspect_repository(Path(args.path))
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(render_text(report))

    if args.fail_below is not None and report.score < args.fail_below:
        return 1
    return 0
