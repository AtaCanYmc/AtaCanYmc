# Contributing Guidelines

Thank you for your interest in contributing to this repository.

## Scope of Contributions

This repository serves as the personal GitHub profile portfolio and automation engine for `@AtaCanYmc`. Contributions are primarily accepted for:

- Bug fixes in `.github/scripts/update_latest_projects.py`
- Enhancements to GitHub Actions workflow stability
- Improvements to documentation hygiene and cross-platform compatibility

## Pull Request Workflow

1. Fork the repository and create a descriptive feature branch:
   ```bash
   git checkout -b fix/workflow-syntax
   ```
2. Commit your changes following [Conventional Commits](https://www.conventionalcommits.org/):
   - `fix: resolve pagination edge case in repo fetching`
   - `chore: update github action versions`
   - `docs: fix formatting in documentation files`
3. Verify your changes locally before submitting a pull request:
   ```bash
   python3 -m py_compile .github/scripts/update_latest_projects.py
   ```
4. Submit your pull request targeting `main`.
