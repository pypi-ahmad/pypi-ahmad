#!/usr/bin/env python3
"""
Generate light/dark SVG "repo cards" for a GitHub profile README.

This script downloads SVGs from github-readme-stats "pin" cards and writes them
to an output directory. A GitHub Actions workflow can commit these SVGs to a
dedicated branch so the README can embed them via raw.githubusercontent.com.
"""

from __future__ import annotations

import argparse
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path


PIN_API = "https://github-readme-stats.vercel.app/api/pin/"


@dataclass(frozen=True)
class Theme:
    name: str
    suffix: str
    params: dict[str, str]


THEMES: list[Theme] = [
    Theme(
        name="dark",
        suffix="dark",
        params={
            # Use explicit colors for consistent polish (theme is still used for layout defaults).
            "theme": "radical",
            "hide_border": "true",
            "bg_color": "0D1117",
            "title_color": "E2E8F0",
            "text_color": "94A3B8",
            "icon_color": "38BDF8",
        },
    ),
    Theme(
        name="light",
        suffix="light",
        params={
            "theme": "default",
            "hide_border": "true",
            "bg_color": "FFFFFF",
            "title_color": "0F172A",
            "text_color": "334155",
            "icon_color": "2563EB",
        },
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


def _fetch(url: str, timeout_s: int, retries: int, retry_sleep_s: float) -> bytes:
    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    # A plain UA improves compatibility with some edge WAF rules.
                    "User-Agent": "pypi-ahmad-profile-cards/1.0",
                    "Accept": "image/svg+xml,text/plain;q=0.9,*/*;q=0.8",
                },
            )
            with urllib.request.urlopen(req, timeout=timeout_s) as resp:
                body = resp.read()
            if b"<svg" not in body[:2000]:
                raise ValueError("Response does not look like SVG.")
            return body
        except Exception as e:  # noqa: BLE001 - surface final error after retries
            last_err = e
            if attempt < retries:
                time.sleep(retry_sleep_s)
    assert last_err is not None
    raise RuntimeError(f"Failed to fetch after {retries} attempts: {last_err}") from last_err


def _build_pin_url(owner: str, repo: str, extra_params: dict[str, str]) -> str:
    params = {"username": owner, "repo": repo, "cache_seconds": "86400"}
    params.update(extra_params)
    return f"{PIN_API}?{urllib.parse.urlencode(params)}"


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

    for owner, repo in repos:
        for theme in THEMES:
            url = _build_pin_url(owner=owner, repo=repo, extra_params=theme.params)
            svg = _fetch(
                url,
                timeout_s=args.timeout_s,
                retries=args.retries,
                retry_sleep_s=args.retry_sleep_s,
            )
            out_path = out_dir / f"{repo}.{theme.suffix}.svg"
            out_path.write_bytes(svg)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

