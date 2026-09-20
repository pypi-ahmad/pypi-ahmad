#!/usr/bin/env python3
"""
Generate light/dark SVG repo cards from GitHub repository metadata.

A GitHub Actions workflow publishes the SVGs to the orphan `cards` branch.
`.github/pinned_repos.txt` lists featured repositories in README order.
The README uses these cards alongside repository-local illustrated project covers.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import sys
import textwrap
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
    system: str
    live: str
    attention: str


THEMES: list[Theme] = [
    Theme(
        name="dark",
        suffix="dark",
        bg="#0C0C0D",
        bg2="#151517",
        border="#343438",
        title="#F4F1EA",
        text="#C9C5BD",
        muted="#96928A",
        accent="#FF5A5F",
        system="#B8BCC4",
        live="#5FD38D",
        attention="#F2B84B",
    ),
    Theme(
        name="light",
        suffix="light",
        bg="#F2EFE8",
        bg2="#FFFEFA",
        border="#D2CEC5",
        title="#171719",
        text="#3F3E42",
        muted="#66635E",
        accent="#B4232F",
        system="#565A62",
        live="#18794E",
        attention="#8A4F00",
    ),
]

# Curated copy from https://pypi-ahmad.github.io/projects, separate from live metrics.
FEATURED = {
    "Agentic-Document-Extraction": (
        "Paperplane", "01 / DOCUMENT AI",
        "Parse documents into grounded Markdown, JSON, and review artifacts.", "document",
        ("Document", "OCR", "Extraction", "Evaluation"),
    ),
    "lora-qlora-fine-tuning-app": (
        "LoRA Fine-tune Studio", "02 / MODEL TRAINING",
        "Prepare datasets, train local adapters, and compare them with base models.", "training",
        ("Dataset", "Prepare", "Train", "Compare"),
    ),
    "self-improving-prompt-optimizer": (
        "Prompt optimizer", "03 / EVALUATION",
        "Compare prompt candidates against a fixed benchmark with visible trade-offs.", "evaluation",
        ("Prompt", "Generate", "Evaluate", "Select"),
    ),
    "video-summarizer": (
        "Video Summarizer", "04 / MULTIMODAL",
        "Reuse video evidence for retrieval, answers, and generated documents.", "video",
        ("Video", "Evidence", "Retrieval", "Answer"),
    ),
}


def _motif(kind: str, accent: str) -> str:
    """Small original line illustrations, contained in a 64-pixel square."""
    shapes = {
        "document": '<path d="M14 8h25l12 12v37H14z M39 8v14h12 M23 32h19 M23 40h19 M23 48h12"/>',
        "training": '<rect x="17" y="17" width="30" height="30" rx="7"/><path d="M25 4v13m14-13v13M25 47v13m14-13v13M4 25h13M4 39h13m30-14h13M47 39h13 M25 33l5 5 10-13"/>',
        "evaluation": '<path d="M8 13h48M8 32h48M8 51h48"/><circle cx="22" cy="13" r="5"/><circle cx="43" cy="32" r="5"/><circle cx="30" cy="51" r="5"/>',
        "video": '<rect x="5" y="10" width="54" height="42" rx="9"/><path d="M26 22l16 9-16 9z"/>',
    }
    return f'<g fill="none" stroke="{accent}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">{shapes.get(kind, shapes["document"])}</g>'


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
                time.sleep(retry_sleep_s * (2 ** (attempt - 1)))
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
    """Bound both line count and unbroken repository names."""
    return textwrap.wrap(
        text, width=max_chars, max_lines=max_lines, placeholder="…",
        break_long_words=True, break_on_hyphens=True,
    )


def _esc(s: str) -> str:
    return html.escape(s, quote=True)


def _render_svg(info: RepoInfo, theme: Theme, *, show_metrics: bool = True) -> str:
    featured = FEATURED.get(info.name) if info.owner == "pypi-ahmad" else None
    title, category, desc, kind, _ = featured or (
        info.name, "PUBLIC REPOSITORY", info.description or "Repository details and source code.", "document", ()
    )
    title_lines = _wrap(title, max_chars=25, max_lines=2)
    desc_lines = _wrap(desc, max_chars=36, max_lines=3)
    title_svg = "".join(
        f'<text x="24" y="{109 + i * 28}" font-size="24" font-weight="700" fill="{theme.title}">{_esc(line)}</text>'
        for i, line in enumerate(title_lines)
    )
    description_svg = "".join(
        f'<text x="24" y="{167 + i * 27}" font-size="18" fill="{theme.text}">{_esc(line)}</text>'
        for i, line in enumerate(desc_lines)
    )
    if show_metrics:
        meta = f"★ {info.stars}   ⑂ {info.forks}   {info.language}"
        updated = f"Updated {info.updated_at[:10]}" if info.updated_at else ""
    else:
        meta, updated = "INDEPENDENT PROJECT", "OPEN REPOSITORY ↗"
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="420" height="280" viewBox="0 0 420 280" role="img" aria-label="{_esc(title)}">
  <title>{_esc(title)}</title>
  <desc>{_esc(desc)}</desc>
  <defs>
    <linearGradient id="bg" x2="1" y2="1">
      <stop stop-color="{theme.bg}"/><stop offset="1" stop-color="{theme.bg2}"/>
    </linearGradient>
  </defs>
  <rect x="1" y="1" width="418" height="278" rx="9" fill="url(#bg)" stroke="{theme.border}"/>
  <path d="M10 1H410" stroke="{theme.accent}" stroke-width="3" stroke-linecap="round"/>
  <path d="M24 66h270" stroke="{theme.border}"/>
  <g transform="translate(330 19) scale(.8)">{_motif(kind, theme.system)}</g>
  <g font-family="Segoe UI,Arial,sans-serif">
    <text x="24" y="40" font-family="Cascadia Code,Cascadia Mono,Consolas,monospace" font-size="13" font-weight="600" letter-spacing="1.1" fill="{theme.accent}">{_esc(category)}</text>
    {title_svg}
    {description_svg}
    <path d="M24 235h372" stroke="{theme.border}"/>
    <text x="24" y="260" font-family="Cascadia Code,Cascadia Mono,Consolas,monospace" font-size="12" fill="{theme.muted}">{_esc(meta)}</text>
    <text x="396" y="260" text-anchor="end" font-family="Cascadia Code,Cascadia Mono,Consolas,monospace" font-size="12" fill="{theme.muted}">{_esc(updated)}</text>
  </g>
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

    failures: list[str] = []
    for owner, repo in repos:
        try:
            info = _fetch_repo(
                owner=owner,
                repo=repo,
                token=token,
                timeout_s=args.timeout_s,
                retries=args.retries,
                retry_sleep_s=args.retry_sleep_s,
            )
        except Exception as e:  # noqa: BLE001 - keep generating other cards
            print(f"warning: skipping {owner}/{repo}: {e}", file=sys.stderr)
            failures.append(f"{owner}/{repo}")
            continue
        for theme in THEMES:
            svg = _render_svg(info, theme).encode("utf-8")
            out_path = out_dir / f"{repo}.{theme.suffix}.svg"
            out_path.write_bytes(svg)

    if failures and len(failures) == len(repos):
        raise SystemExit(f"Failed to fetch all repos: {', '.join(failures)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
