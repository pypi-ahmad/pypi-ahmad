# Contributing

Thank you for your interest in contributing.

## Getting Started

1. Open an issue for bugs, improvements, or proposals before large changes.
2. Fork the repository and create a focused branch from `main`.
3. Keep changes scoped to one logical objective.
4. Update documentation alongside behavior changes.

## Repository layout

- `README.md` is the public profile. Featured work leads with Grounded Document Parser.
- `docs/sanitized-outcomes.md` records employer-internal results with confidentiality boundaries.
- `.github/pinned_repos.txt` drives the card generator. Keep that list in the same order as Featured Work.
- `profile-3d-contrib/` holds the 3D contribution SVGs committed on `main`.
- `.codegraph/`, `.firecrawl/`, `.ua/`, and `graphify-out/` are tracked analysis artifacts. Do not add `.ua/dashboard.stdout.log` or other files that contain tokens.
- Remote branches `cards`, `generated`, and `output` are orphan image branches. Do not merge them into `main`.

## Releases

Releases use calendar-date tags, matching [CHANGELOG.md](CHANGELOG.md). The current release is [2026-08-13](https://github.com/pypi-ahmad/pypi-ahmad/releases/tag/2026-08-13).

## Pull Request Guidelines

- Use clear commit messages that describe intent.
- Keep pull requests reviewable and avoid unrelated refactors.
- Include context in the PR description: problem, approach, and validation.
- Confirm no secrets, tokens, or credentials are included in commits.

## Validation Checklist

Before opening a pull request, verify:

- [ ] Changes are limited to the intended scope.
- [ ] Documentation is updated where needed.
- [ ] Relevant checks pass locally.
- [ ] No sensitive data is present in diffs.

## Reporting

- Bugs and feature requests: <https://github.com/pypi-ahmad/pypi-ahmad/issues>
- Security vulnerabilities: see [SECURITY.md](SECURITY.md)

## Code of Conduct

By participating, you agree to follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
