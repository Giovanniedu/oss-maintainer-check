# Contributing

Thanks for considering a contribution. Small, focused changes and clear bug reports are welcome.

## Before opening an issue

Check whether the issue already exists. For a bug, include the command you ran, Python version, operating system, expected behavior, actual behavior, and a minimal example directory. Never include access tokens, private source code, or other secrets in a public issue.

## Development setup

- Python 3.10 or later
- Git
- `pytest` for the test suite

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
```

## Pull requests

Open a focused pull request with a concise description of the problem and solution. Add or update tests for behavior changes, update documentation when needed, and make sure CI passes. By submitting a contribution, you agree that it may be distributed under this repository's MIT license.

## Project principles

- Keep checks transparent, local, and deterministic.
- Do not make network requests or upload repository contents.
- Avoid implying a checklist score proves quality, security, popularity, or eligibility for funding.
- Prefer actionable recommendations and explain limitations.
