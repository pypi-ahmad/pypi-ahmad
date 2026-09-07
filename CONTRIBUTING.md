# Contributing

Thank you for helping improve this profile repository. Contributions are
welcome when they are focused and easy to review.

## Make a Contribution

1. For a substantial change, open an
   [issue](https://github.com/pypi-ahmad/pypi-ahmad/issues) first to describe
   the problem or proposal.
2. Fork the repository and create a focused branch from `main`.
3. Keep the pull request to one logical objective and update related
   documentation when behavior or public information changes.
4. In the pull request description, state the problem, approach, and validation
   performed.

## Repository-specific guidance

- `README.md` is the public profile; keep claims accurate and suitable for a
  public audience.
- `docs/sanitized-outcomes.md` records employer-internal results with explicit
  confidentiality boundaries.
- `.github/pinned_repos.txt` is the source list for generated repository cards.
- `profile-3d-contrib/` and `profile-stats/` contain generated profile assets
  published to `main` by GitHub Actions. Repository cards are published to
  `cards`, and animations are published to `output`.
- Change the relevant source configuration or workflow instead of manually
  editing generated assets. Do not merge the generator-managed `cards`,
  `generated`, or `output` branches into `main`.
- Do not add local analysis caches, dashboard output, credentials, tokens, or
  other sensitive workspace data unless a maintainer explicitly requests it.

## Releases

Releases use calendar-date tags, as recorded in [CHANGELOG.md](CHANGELOG.md).
The latest released version is
[2026-08-13](https://github.com/pypi-ahmad/pypi-ahmad/releases/tag/2026-08-13).

## Pull Request Guidelines

- Use clear commit messages that describe intent.
- Keep pull requests reviewable and avoid unrelated refactors.
- Confirm no secrets, tokens, or credentials are included in commits.

## Validation Checklist

Before opening a pull request, verify:

- [ ] Changes are limited to the intended scope.
- [ ] Documentation is updated where needed.
- [ ] Relevant checks pass locally.
- [ ] No sensitive data is present in diffs.

## Reporting

- Bugs and feature requests: <https://github.com/pypi-ahmad/pypi-ahmad/issues>
- Security vulnerabilities: follow [SECURITY.md](SECURITY.md); do not report
  them in a public issue.
- Conduct concerns: follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Code of Conduct

By participating, you agree to follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
