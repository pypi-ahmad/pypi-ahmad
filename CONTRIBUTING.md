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
- Maintain project descriptions and contact links directly in `README.md`.
- `profile-3d-contrib/` and `profile-stats/` contain generated profile assets
  published to `main` by GitHub Actions. Contribution arcade animations are
  published to `output`. The statistics workflow also refreshes dashboard exports.
- Change the relevant source configuration or workflow instead of manually
  editing generated assets. Do not merge the generated `cards`, `generated`,
  or `output` branches into `main`; `cards` is retained as historical output.
- Do not add local analysis caches, dashboard output, credentials, tokens, or
  other sensitive workspace data unless a maintainer explicitly requests it.

## Portfolio dashboard export

`scripts/generate_github_stats.py` also writes the public, schema-versioned
`profile-stats/dashboard.json` consumed by the portfolio. The existing scheduled
profile workflow publishes it with the SVG assets. Use `--dashboard-only` to
refresh JSON without rewriting SVGs:

```powershell
uv run --no-project python scripts/generate_github_stats.py --dashboard-only
uv run --no-project python -m unittest discover -s tests -v
```

Use authenticated `gh` or the generator's existing configured token support.
Never put credentials or raw API responses into this public export. Its allowlist
excludes private repository identities; aggregate profile contribution counts
may include private activity. Validation precedes atomic replacement, so failed
collection leaves the prior JSON intact. Copy a reviewed export to the portfolio's
`public/data/github.json` to refresh its offline fallback. Publication requires
separate approval.

The additive schema-v1 discovery collections include public repository metadata,
published release records/assets, and public external merged pull requests.
`scripts/discovery_export.py` collects and validates them, reusing the advanced
collector's release requests. Forks and archives are available to the explorer;
release history excludes forks and drafts. Collection failures stop the new
export rather than publishing an incomplete history as complete. Older snapshots
without these fields remain readable by the portfolio.

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
