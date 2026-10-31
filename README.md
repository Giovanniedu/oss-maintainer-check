# OSS Maintainer Check

A small, dependency-free command-line checklist for repository maintainers. It checks whether common project-maintenance files exist and gives actionable next steps. It works on a local directory and makes no network requests.

> **Alpha notice:** this project is a new starter tool. It does not claim production adoption, popularity, or eligibility for any grant or program.

## What it checks

The tool looks for a README (20 points), an open-source license (20), contribution guidance (15), a code of conduct (10), a security policy (10), issue templates (10), a pull-request template (5), and at least one GitHub Actions workflow (10). A passing check means only that a matching file exists; the tool does not judge whether the file is complete, accurate, enforced, or legally appropriate. The score is a checklist aid, not a quality, security, or popularity rating.

## Install and run

Requires Python 3.10 or later. Install from a checkout:

```bash
python -m pip install .
oss-maintainer-check /path/to/repository
```

Or run without installing:

```bash
python -m oss_maintainer_check /path/to/repository
```

Get machine-readable output or use a score threshold in CI:

```bash
oss-maintainer-check . --format json
oss-maintainer-check . --fail-below 70
```

The command exits with status `1` when a requested threshold is not met, and `2` when the supplied path is invalid. Without `--fail-below`, a completed inspection exits with status `0`.

## Example

```text
OSS Maintainer Check — /work/my-project
Score: 75/100 (6/8 checks passed)

[PASS] Project overview (README) — README.md
[PASS] Open-source license — LICENSE
[TODO] Contribution guide
       Document how to report bugs, propose changes, and run checks locally.
```

## Development

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
```

See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. The project is licensed under the MIT License; see [LICENSE](LICENSE).

## Scope and privacy

The program reads file names in the directory you specify. It does not access Git history, inspect file contents for secrets, contact GitHub, upload repository data, or modify files. Run it only on repositories you own or are authorized to inspect. Avoid including private repository details in public issue reports.

## Español

OSS Maintainer Check es una lista de verificación sencilla para personas que mantienen repositorios. Comprueba localmente si existen archivos habituales —como README, licencia, guía de contribución, política de seguridad, plantillas y CI— y propone acciones. No hace solicitudes de red ni modifica el repositorio.

La puntuación solo indica presencia de archivos: **no** evalúa su calidad, seguridad, popularidad ni el cumplimiento de requisitos de un programa. El proyecto es nuevo y no afirma tener adopción ni historial de mantenimiento. Consulta arriba las instrucciones de instalación y uso.
