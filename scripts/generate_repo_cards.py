#!/usr/bin/env python3
"""
Generate light/dark SVG "repo cards" for a GitHub profile README.

We generate SVGs locally from GitHub repository metadata (REST API), then a
GitHub Actions workflow commits the SVGs to a dedicated branch. The profile
README embeds those SVGs via raw.githubusercontent.com so it stays fast and
reliable (no live dependency on third-party card services).
"""

from __future__ import annotations

import argparse
import html
import json
import os
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path


REPO_API = "https://api.github.com/repos"


@dataclass(frozen=True)
class Theme:
    name: str
    suffix: str
    bg: str
    bg2: str
    border: str
    title: str
    text: str
    muted: str
    accent: str


THEMES: list[Theme] = [
    Theme(
        name="dark",
        suffix="dark",
        bg="#0D1117",
        bg2="#0B1220",
        border="#1F2937",
        title="#E2E8F0",
        text="#94A3B8",
        muted="#64748B",
        accent="#38BDF8",
    ),
    Theme(
        name="light",
        suffix="light",
        bg="#FFFFFF",
        bg2="#F8FAFC",
        border="#E2E8F0",
        title="#0F172A",
        text="#334155",
        muted="#64748B",
        accent="#2563EB",
    ),
]


def _read_repo_list(path: Path, default_owner: str) -> list[tuple[str, str]]:
    repos: list[tuple[str, str]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "/" in line:
            owner, repo = line.split("/", 1)
        else:
            owner, repo = default_owner, line
        repos.append((owner.strip(), repo.strip()))
    if not repos:
        raise ValueError(f"No repositories found in {path}")
    return repos


def _fetch(url: str, headers: dict[str, str], timeout_s: int, retries: int, retry_sleep_s: float) -> bytes:
    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "pypi-ahmad-profile-cards/1.0",
                    **headers,
                },
            )
            with urllib.request.urlopen(req, timeout=timeout_s) as resp:
                body = resp.read()
            return body
        except Exception as e:  # noqa: BLE001 - surface final error after retries
            last_err = e
            if attempt < retries:
                time.sleep(retry_sleep_s)
    assert last_err is not None
    raise RuntimeError(f"Failed to fetch after {retries} attempts: {last_err}") from last_err


@dataclass(frozen=True)
class RepoInfo:
    owner: str
    name: str
    description: str
    stars: int
    forks: int
    language: str
    updated_at: str
    url: str


def _repo_url(owner: str, repo: str) -> str:
    return f"{REPO_API}/{urllib.parse.quote(owner)}/{urllib.parse.quote(repo)}"


def _fetch_repo(owner: str, repo: str, token: str | None, timeout_s: int, retries: int, retry_sleep_s: float) -> RepoInfo:
    headers = {
        "Accept": "application/vnd.github+json",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    raw = _fetch(
        _repo_url(owner, repo),
        headers=headers,
        timeout_s=timeout_s,
        retries=retries,
        retry_sleep_s=retry_sleep_s,
    )
    data = json.loads(raw.decode("utf-8"))
    return RepoInfo(
        owner=owner,
        name=repo,
        description=(data.get("description") or "").strip(),
        stars=int(data.get("stargazers_count") or 0),
        forks=int(data.get("forks_count") or 0),
        language=(data.get("language") or "—").strip(),
        updated_at=str(data.get("pushed_at") or data.get("updated_at") or ""),
        url=str(data.get("html_url") or f"https://github.com/{owner}/{repo}"),
    )


def _wrap(text: str, max_chars: int, max_lines: int) -> list[str]:
    words = [w for w in text.split() if w]
    lines: list[str] = []
    cur: list[str] = []
    cur_len = 0
    for w in words:
        add = len(w) + (1 if cur else 0)
        if cur and cur_len + add > max_chars:
            lines.append(" ".join(cur))
            cur = [w]
            cur_len = len(w)
            if len(lines) >= max_lines:
                break
        else:
            cur.append(w)
            cur_len += add

    if len(lines) < max_lines and cur:
        lines.append(" ".join(cur))

    if len(lines) > max_lines:
        lines = lines[:max_lines]

    # Ellipsize if truncated.
    joined = " ".join(words)
    if joined and " ".join(lines) != joined:
        if lines:
            lines[-1] = (lines[-1][: max(0, max_chars - 1)] + "…").rstrip()
    return lines


def _esc(s: str) -> str:
    return html.escape(s, quote=True)


def _render_svg(info: RepoInfo, theme: Theme) -> str:
    width = 520
    height = 140
    pad = 16

    title = info.name
    desc = info.description or " "
    desc_lines = _wrap(desc, max_chars=56, max_lines=2)

    meta = f"★ {info.stars}   ⑂ {info.forks}   {info.language}"
    updated = info.updated_at[:10] if info.updated_at else ""

    # A small "glow" on the accent dot looks nicer than flat icons.
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{_esc(title)}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{theme.bg}"/>
      <stop offset="1" stop-color="{theme.bg2}"/>
    </linearGradient>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000000" flood-opacity="0.18"/>
    </filter>
  </defs>

  <rect x="0.5" y="0.5" rx="16" ry="16" width="{width-1}" height="{height-1}" fill="url(#bg)" stroke="{theme.border}" filter="url(#shadow)"/>

  <circle cx="{pad+8}" cy="{pad+10}" r="5.5" fill="{theme.accent}" opacity="0.95"/>
  <text x="{pad+22}" y="{pad+16}" fill="{theme.title}" font-size="18" font-weight="700"
        font-family="ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, Helvetica, Arial">
    {_esc(title)}
  </text>

  <text x="{pad}" y="{pad+44}" fill="{theme.text}" font-size="13.5"
        font-family="ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, Helvetica, Arial">
    {_esc(desc_lines[0] if len(desc_lines) > 0 else "")}
  </text>
  <text x="{pad}" y="{pad+64}" fill="{theme.text}" font-size="13.5"
        font-family="ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, Helvetica, Arial">
    {_esc(desc_lines[1] if len(desc_lines) > 1 else "")}
  </text>

  <text x="{pad}" y="{height-pad}" fill="{theme.muted}" font-size="12.5"
        font-family="ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, Helvetica, Arial">
    {_esc(meta)}
  </text>

  <text x="{width-pad}" y="{height-pad}" text-anchor="end" fill="{theme.muted}" font-size="12.5"
        font-family="ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, Helvetica, Arial">
    {_esc(updated)}
  </text>
</svg>
"""


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--owner", default=None, help="Default repo owner for bare repo names.")
    p.add_argument(
        "--repos-file",
        default=".github/pinned_repos.txt",
        help="Path to a newline-delimited list of repos to render.",
    )
    p.add_argument("--out-dir", default="cards", help="Directory to write SVGs into.")
    p.add_argument("--timeout-s", type=int, default=20, help="HTTP timeout in seconds.")
    p.add_argument("--retries", type=int, default=4, help="Number of download retries per card.")
    p.add_argument("--retry-sleep-s", type=float, default=1.5, help="Sleep between retries.")
    args = p.parse_args()

    default_owner = args.owner or (Path.home().name or "pypi-ahmad")
    repos_file = Path(args.repos_file)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    repos = _read_repo_list(repos_file, default_owner=default_owner)
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

    for owner, repo in repos:
        info = _fetch_repo(
            owner=owner,
            repo=repo,
            token=token,
            timeout_s=args.timeout_s,
            retries=args.retries,
            retry_sleep_s=args.retry_sleep_s,
        )
        for theme in THEMES:
            svg = _render_svg(info, theme).encode("utf-8")
            out_path = out_dir / f"{repo}.{theme.suffix}.svg"
            out_path.write_bytes(svg)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
