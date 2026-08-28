#!/usr/bin/env python3
"""Generate advanced GitHub profile statistics as dependency-free SVG panels."""

from __future__ import annotations

import argparse
import html
import http.client
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

API = "https://api.github.com"
GRAPHQL = f"{API}/graphql"


@dataclass(frozen=True)
class Theme:
    name: str
    background: str
    panel: str
    border: str
    title: str
    text: str
    muted: str
    accent: str
    green: str
    red: str


THEMES = (
    Theme("dark", "#0d1117", "#161b22", "#30363d", "#f0f6fc", "#c9d1d9", "#8b949e", "#58a6ff", "#3fb950", "#f85149"),
    Theme("light", "#ffffff", "#f6f8fa", "#d0d7de", "#1f2328", "#24292f", "#57606a", "#0969da", "#1a7f37", "#cf222e"),
)


class ApiError(RuntimeError):
    def __init__(self, status: int, url: str, message: str) -> None:
        super().__init__(f"GitHub API {status} for {url}: {message}")
        self.status = status


class GitHubClient:
    def __init__(self, token: str, retries: int = 4) -> None:
        self.token = token
        self.retries = retries

    def request(
        self,
        url: str,
        *,
        method: str = "GET",
        payload: dict[str, Any] | None = None,
        accept: str = "application/vnd.github+json",
    ) -> Any:
        body = json.dumps(payload).encode() if payload is not None else None
        headers = {
            "Accept": accept,
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "User-Agent": "pypi-ahmad-profile-statistics/1.0",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        last_error: Exception | None = None
        for attempt in range(self.retries):
            try:
                request = urllib.request.Request(url, data=body, headers=headers, method=method)
                with urllib.request.urlopen(request, timeout=30) as response:
                    raw = response.read()
                    if response.status == 202:
                        raise ApiError(202, url, "statistics are still being generated")
                    return json.loads(raw) if raw else None
            except urllib.error.HTTPError as error:
                message = error.read().decode("utf-8", errors="replace")[:300]
                last_error = ApiError(error.code, url, message)
                if error.code not in {202, 429, 500, 502, 503, 504}:
                    raise last_error
            except (urllib.error.URLError, TimeoutError, http.client.IncompleteRead, http.client.RemoteDisconnected, ApiError) as error:
                last_error = error
                if isinstance(error, ApiError) and error.status != 202:
                    raise
            if attempt + 1 < self.retries:
                time.sleep(2**attempt)
        assert last_error is not None
        raise last_error

    def graphql(self, query: str, **variables: Any) -> dict[str, Any]:
        response = self.request(GRAPHQL, method="POST", payload={"query": query, "variables": variables})
        if response.get("errors"):
            raise RuntimeError(f"GitHub GraphQL error: {response['errors']}")
        return response["data"]

    def rest(self, path: str, **params: Any) -> Any:
        query = urllib.parse.urlencode(params)
        return self.request(f"{API}{path}{'?' + query if query else ''}")


USER_QUERY = """
query($login: String!) {
  user(login: $login) {
    id createdAt
    pullRequests { totalCount }
    mergedPullRequests: pullRequests(states: MERGED) { totalCount }
    openIssues: issues(states: OPEN) { totalCount }
    closedIssues: issues(states: CLOSED) { totalCount }
    repositoriesContributedTo(
      first: 5, includeUserRepositories: false,
      contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, PULL_REQUEST_REVIEW, REPOSITORY],
      orderBy: {field: UPDATED_AT, direction: DESC}
    ) { totalCount nodes { nameWithOwner } }
  }
}
"""

REPOSITORIES_QUERY = """
query($login: String!, $after: String) {
  user(login: $login) {
    repositories(
      first: 100, after: $after, privacy: PUBLIC, ownerAffiliations: OWNER,
      isFork: false, isArchived: false, orderBy: {field: UPDATED_AT, direction: DESC}
    ) {
      pageInfo { hasNextPage endCursor }
      nodes {
        name nameWithOwner pushedAt forkCount stargazerCount
        watchers { totalCount }
        languages(first: 8, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
        stargazers(first: 100, orderBy: {field: STARRED_AT, direction: ASC}) {
          pageInfo { hasNextPage endCursor }
          edges { starredAt }
        }
      }
    }
  }
}
"""

STARGAZERS_QUERY = """
query($owner: String!, $name: String!, $after: String!) {
  repository(owner: $owner, name: $name) {
    stargazers(first: 100, after: $after, orderBy: {field: STARRED_AT, direction: ASC}) {
      pageInfo { hasNextPage endCursor }
      edges { starredAt }
    }
  }
}
"""

REVIEWS_QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) { totalPullRequestReviewContributions }
  }
}
"""

RECENT_QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!, $since: GitTimestamp!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      commitContributionsByRepository(maxRepositories: 100) {
        contributions { totalCount }
        repository {
          nameWithOwner
          languages(first: 8, orderBy: {field: SIZE, direction: DESC}) {
            edges { size node { name color } }
          }
          defaultBranchRef {
            target {
              ... on Commit {
                history(first: 100, since: $since, author: {id: "USER_ID"}) {
                  nodes { committedDate }
                }
              }
            }
          }
        }
      }
    }
  }
}
"""


def _iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _percent(part: int, total: int) -> float:
    return 0.0 if total == 0 else 100 * part / total


def _timezone(timezone_name: str):
    try:
        return ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError:
        if timezone_name == "Asia/Kolkata":
            return timezone(timedelta(hours=5, minutes=30), name=timezone_name)
        raise


def _load_repositories(client: GitHubClient, login: str) -> list[dict[str, Any]]:
    repositories: list[dict[str, Any]] = []
    after = None
    while True:
        connection = client.graphql(REPOSITORIES_QUERY, login=login, after=after)["user"]["repositories"]
        repositories.extend(connection["nodes"])
        if not connection["pageInfo"]["hasNextPage"]:
            break
        after = connection["pageInfo"]["endCursor"]

    for repository in repositories:
        connection = repository["stargazers"]
        while connection["pageInfo"]["hasNextPage"]:
            owner, name = repository["nameWithOwner"].split("/", 1)
            connection = client.graphql(
                STARGAZERS_QUERY,
                owner=owner,
                name=name,
                after=connection["pageInfo"]["endCursor"],
            )["repository"]["stargazers"]
            repository["stargazers"]["edges"].extend(connection["edges"])
    return repositories


def _lifetime_reviews(client: GitHubClient, login: str, created_at: str, now: datetime) -> int:
    start = _parse_time(created_at)
    total = 0
    while start < now:
        next_start = min(start + timedelta(days=365), now)
        end = next_start - timedelta(milliseconds=1) if next_start < now else now
        data = client.graphql(REVIEWS_QUERY, login=login, **{"from": _iso(start), "to": _iso(end)})
        total += data["user"]["contributionsCollection"]["totalPullRequestReviewContributions"]
        start = next_start
    return total


def _recent_activity(
    client: GitHubClient,
    login: str,
    user_id: str,
    now: datetime,
    days: int,
    timezone_name: str,
) -> tuple[Counter[str], Counter[int], Counter[int]]:
    start = now - timedelta(days=days)
    query = RECENT_QUERY.replace("USER_ID", user_id)
    groups = client.graphql(query, login=login, **{"from": _iso(start), "to": _iso(now), "since": _iso(start)})["user"]["contributionsCollection"]["commitContributionsByRepository"]
    languages: Counter[str] = Counter()
    weekdays: Counter[int] = Counter()
    hours: Counter[int] = Counter()
    local_zone = _timezone(timezone_name)
    for group in groups:
        edges = group["repository"]["languages"]["edges"]
        size = sum(edge["size"] for edge in edges) or 1
        commits = group["contributions"]["totalCount"]
        for edge in edges:
            languages[edge["node"]["name"]] += commits * edge["size"] / size
        history = (((group["repository"].get("defaultBranchRef") or {}).get("target") or {}).get("history") or {})
        for commit in history.get("nodes", []):
            local = _parse_time(commit["committedDate"]).astimezone(local_zone)
            weekdays[local.weekday()] += 1
            hours[local.hour] += 1
    return languages, weekdays, hours


def _published_releases(client: GitHubClient, owner: str, name: str) -> tuple[int, int]:
    releases = downloads = page = 0
    while True:
        page += 1
        batch = client.rest(f"/repos/{owner}/{name}/releases", per_page=100, page=page)
        public = [release for release in batch if not release.get("draft")]
        releases += len(public)
        downloads += sum(asset.get("download_count", 0) for release in public for asset in release.get("assets", []))
        if len(batch) < 100:
            return releases, downloads


def _repo_extras(client: GitHubClient, login: str, repository: dict[str, Any]) -> dict[str, Any]:
    name = repository["name"]
    result: dict[str, Any] = {"name": name, "lines": None, "release": None, "traffic": None, "referrers": []}
    try:
        contributors = client.rest(f"/repos/{login}/{name}/stats/contributors") or []
        contributor = next((item for item in contributors if (item.get("author") or {}).get("login", "").lower() == login.lower()), None)
        weeks = contributor.get("weeks", []) if contributor else []
        result["lines"] = (sum(week.get("a", 0) for week in weeks), sum(abs(week.get("d", 0)) for week in weeks))
    except ApiError as error:
        if error.status in {401, 429}:
            raise
    try:
        result["release"] = _published_releases(client, login, name)
    except ApiError as error:
        if error.status in {401, 429}:
            raise
    try:
        views = client.rest(f"/repos/{login}/{name}/traffic/views")
        clones = client.rest(f"/repos/{login}/{name}/traffic/clones")
        result["referrers"] = client.rest(f"/repos/{login}/{name}/traffic/popular/referrers") or []
        result["traffic"] = (views["count"], clones["count"])
    except ApiError as error:
        if error.status in {401, 429}:
            raise
    return result


def _load_extras(client: GitHubClient, login: str, repositories: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(_repo_extras, client, login, repository): repository["name"] for repository in repositories}
        for future in as_completed(futures):
            results.append(future.result())
    return sorted(results, key=lambda item: item["name"].lower())


def _monthly_star_series(repositories: list[dict[str, Any]], created_at: str, now: datetime) -> list[tuple[str, int]]:
    start = _parse_time(created_at)
    month = datetime(start.year, start.month, 1, tzinfo=timezone.utc)
    last = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
    gained = Counter(
        _parse_time(edge["starredAt"]).strftime("%Y-%m")
        for repository in repositories
        for edge in repository["stargazers"]["edges"]
    )
    series: list[tuple[str, int]] = []
    total = 0
    while month <= last:
        key = month.strftime("%Y-%m")
        total += gained[key]
        series.append((key, total))
        month = datetime(month.year + (month.month == 12), month.month % 12 + 1, 1, tzinfo=timezone.utc)
    return series


def collect_metrics(
    client: GitHubClient,
    login: str,
    recent_days: int,
    timezone_name: str,
    now: datetime | None = None,
) -> dict[str, Any]:
    now = now or datetime.now(timezone.utc)
    user = client.graphql(USER_QUERY, login=login)["user"]
    repositories = _load_repositories(client, login)
    reviews = _lifetime_reviews(client, login, user["createdAt"], now)
    languages, weekdays, hours = _recent_activity(client, login, user["id"], now, recent_days, timezone_name)
    extras = _load_extras(client, login, repositories)

    line_results = [item["lines"] for item in extras if item["lines"] is not None]
    release_results = [item["release"] for item in extras if item["release"] is not None]
    traffic_results = [item["traffic"] for item in extras if item["traffic"] is not None]
    referrers: Counter[str] = Counter()
    for item in extras:
        referrers.update({entry["referrer"]: entry["count"] for entry in item["referrers"]})

    cutoff = now - timedelta(days=recent_days)
    active = [repository for repository in repositories if repository.get("pushedAt") and _parse_time(repository["pushedAt"]) >= cutoff]
    return {
        "generated_at": now,
        "login": login,
        "recent_days": recent_days,
        "timezone": timezone_name,
        "repositories": len(repositories),
        "stars": sum(repository["stargazerCount"] for repository in repositories),
        "star_series": _monthly_star_series(repositories, user["createdAt"], now),
        "forks": sum(repository["forkCount"] for repository in repositories),
        "watchers": sum(repository["watchers"]["totalCount"] for repository in repositories),
        "reviews": reviews,
        "pull_requests": user["pullRequests"]["totalCount"],
        "merged_pull_requests": user["mergedPullRequests"]["totalCount"],
        "open_issues": user["openIssues"]["totalCount"],
        "closed_issues": user["closedIssues"]["totalCount"],
        "external_total": user["repositoriesContributedTo"]["totalCount"],
        "external_recent": [node["nameWithOwner"] for node in user["repositoriesContributedTo"]["nodes"]],
        "active_repositories": [(repository["name"], repository["pushedAt"][:10]) for repository in active[:5]],
        "languages": languages.most_common(5),
        "weekdays": weekdays,
        "hours": hours,
        "lines_added": sum(value[0] for value in line_results),
        "lines_removed": sum(value[1] for value in line_results),
        "lines_coverage": len(line_results),
        "releases": sum(value[0] for value in release_results),
        "downloads": sum(value[1] for value in release_results),
        "release_coverage": len(release_results),
        "views": sum(value[0] for value in traffic_results),
        "clones": sum(value[1] for value in traffic_results),
        "traffic_coverage": len(traffic_results),
        "referrers": referrers.most_common(5),
    }


def _number(value: float) -> str:
    return f"{value:,.0f}"


def _text(x: int, y: int, value: str, theme: Theme, *, size: int = 15, weight: int = 400, color: str | None = None, anchor: str = "start") -> str:
    return f'<text x="{x}" y="{y}" fill="{color or theme.text}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" font-family="Segoe UI,Arial,sans-serif">{html.escape(value)}</text>'


def _header(title: str, subtitle: str, theme: Theme, height: int) -> list[str]:
    return [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" viewBox="0 0 900 {height}" role="img" aria-label="{html.escape(title)}">',
        f'<rect x="0.5" y="0.5" width="899" height="{height - 1}" rx="12" fill="{theme.background}" stroke="{theme.border}"/>',
        _text(28, 38, title, theme, size=22, weight=700, color=theme.title),
        _text(28, 62, subtitle, theme, size=13, color=theme.muted),
    ]


def _metric(x: int, y: int, label: str, value: str, theme: Theme) -> list[str]:
    return [
        f'<rect x="{x}" y="{y}" width="190" height="70" rx="9" fill="{theme.panel}" stroke="{theme.border}"/>',
        _text(x + 14, y + 27, label, theme, size=13, color=theme.muted),
        _text(x + 14, y + 55, value, theme, size=21, weight=700, color=theme.title),
    ]


def _footer(metrics: dict[str, Any], theme: Theme, height: int, coverage: str = "") -> str:
    stamp = metrics["generated_at"].strftime("%Y-%m-%d %H:%M UTC")
    scope = f'{metrics["repositories"]} public owned repositories'
    suffix = f" · {coverage}" if coverage else ""
    return _text(28, height - 18, f"Generated {stamp} · {scope}{suffix}", theme, size=12, color=theme.muted)


def _sparkline(series: list[tuple[str, int]], x: int, y: int, width: int, height: int, theme: Theme) -> str:
    values = [value for _, value in series] or [0]
    maximum = max(values) or 1
    points = []
    for index, value in enumerate(values):
        px = x + (width * index / max(1, len(values) - 1))
        py = y + height - (height * value / maximum)
        points.append(f"{px:.1f},{py:.1f}")
    return f'<polyline points="{" ".join(points)}" fill="none" stroke="{theme.accent}" stroke-width="3" stroke-linejoin="round"/>'


def render_reach(metrics: dict[str, Any], theme: Theme) -> str:
    height = 510
    parts = _header("Reach and collaboration", "Lifetime profile metrics and star growth", theme, height)
    values = [
        (28, 84, "Stars", _number(metrics["stars"])),
        (234, 84, "Forks", _number(metrics["forks"])),
        (440, 84, "Watchers", _number(metrics["watchers"])),
        (646, 84, "PR reviews", _number(metrics["reviews"])),
        (28, 166, "PRs merged", f'{metrics["merged_pull_requests"]}/{metrics["pull_requests"]} ({_percent(metrics["merged_pull_requests"], metrics["pull_requests"]):.0f}%)'),
        (234, 166, "Issues open / closed", f'{metrics["open_issues"]} / {metrics["closed_issues"]}'),
        (440, 166, "External repositories", _number(metrics["external_total"])),
    ]
    for value in values:
        parts.extend(_metric(*value, theme))
    parts.extend([
        _text(28, 276, "Stars gained over time", theme, size=16, weight=600, color=theme.title),
        f'<rect x="28" y="292" width="520" height="120" rx="8" fill="{theme.panel}" stroke="{theme.border}"/>',
        _sparkline(metrics["star_series"], 44, 310, 488, 82, theme),
        _text(570, 276, "Recent external contributions", theme, size=16, weight=600, color=theme.title),
    ])
    names = metrics["external_recent"] or ["No external repositories found"]
    for index, name in enumerate(names[:5]):
        parts.append(_text(570, 306 + index * 25, name, theme, size=13))
    parts.extend([_footer(metrics, theme, height), "</svg>"])
    return "\n".join(parts)


def _bars(values: list[tuple[str, float]], x: int, y: int, width: int, theme: Theme, color: str | None = None) -> list[str]:
    maximum = max((value for _, value in values), default=1) or 1
    parts: list[str] = []
    for index, (label, value) in enumerate(values):
        row = y + index * 27
        parts.append(_text(x, row + 13, label, theme, size=12))
        parts.append(f'<rect x="{x + 105}" y="{row}" width="{width}" height="14" rx="4" fill="{theme.panel}"/>')
        parts.append(f'<rect x="{x + 105}" y="{row}" width="{width * value / maximum:.1f}" height="14" rx="4" fill="{color or theme.accent}"/>')
    return parts


def render_coding(metrics: dict[str, Any], theme: Theme) -> str:
    height = 620
    days = metrics["recent_days"]
    parts = _header("Code and activity", f"Lifetime code totals; recent metrics cover {days} days", theme, height)
    parts.extend(_metric(28, 84, "Lines added", _number(metrics["lines_added"]), theme))
    parts.extend(_metric(234, 84, "Lines removed", _number(metrics["lines_removed"]), theme))
    parts.append(_text(28, 190, "Recently active repositories", theme, size=16, weight=600, color=theme.title))
    active = metrics["active_repositories"] or [("No pushes in recent window", "")]
    for index, (name, date) in enumerate(active):
        parts.append(_text(28, 220 + index * 25, f"{name}  {date}".rstrip(), theme, size=13))
    parts.append(_text(470, 190, "Recently used languages", theme, size=16, weight=600, color=theme.title))
    language_values = [(name, value) for name, value in metrics["languages"]] or [("No recent commits", 0)]
    parts.extend(_bars(language_values, 470, 210, 260, theme))
    parts.append(_text(28, 372, f'Commit habits ({metrics["timezone"]})', theme, size=16, weight=600, color=theme.title))
    weekday_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    parts.extend(_bars([(name, metrics["weekdays"].get(index, 0)) for index, name in enumerate(weekday_names)], 28, 396, 250, theme, theme.green))
    hour_values = [(f"{hour:02d}", metrics["hours"].get(hour, 0)) for hour in range(24)]
    maximum = max((value for _, value in hour_values), default=1) or 1
    for index, (label, value) in enumerate(hour_values):
        x = 450 + index * 17
        bar_height = 110 * value / maximum
        parts.append(f'<rect x="{x}" y="{536 - bar_height:.1f}" width="11" height="{bar_height:.1f}" fill="{theme.accent}"/>')
        if index % 3 == 0:
            parts.append(_text(x + 5, 554, label, theme, size=9, color=theme.muted, anchor="middle"))
    coverage = f'line coverage {metrics["lines_coverage"]}/{metrics["repositories"]}'
    parts.extend([_footer(metrics, theme, height, coverage), "</svg>"])
    return "\n".join(parts)


def render_distribution(metrics: dict[str, Any], theme: Theme) -> str:
    height = 400
    parts = _header("Distribution and repository traffic", "Published releases; GitHub traffic covers the last 14 days", theme, height)
    parts.extend(_metric(28, 84, "Published releases", _number(metrics["releases"]), theme))
    parts.extend(_metric(234, 84, "Asset downloads", _number(metrics["downloads"]), theme))
    parts.extend(_metric(440, 84, "Repository views", _number(metrics["views"]), theme))
    parts.extend(_metric(646, 84, "Repository clones", _number(metrics["clones"]), theme))
    parts.append(_text(28, 190, "Popular referrers", theme, size=16, weight=600, color=theme.title))
    referrers = [(name, count) for name, count in metrics["referrers"]] or [("No referral data", 0)]
    parts.extend(_bars(referrers, 28, 212, 520, theme, theme.green))
    coverage = f'traffic coverage {metrics["traffic_coverage"]}/{metrics["repositories"]}; release coverage {metrics["release_coverage"]}/{metrics["repositories"]}'
    parts.extend([_footer(metrics, theme, height, coverage), "</svg>"])
    return "\n".join(parts)


def render_all(metrics: dict[str, Any]) -> dict[str, str]:
    output: dict[str, str] = {}
    for theme in THEMES:
        output[f"reach.{theme.name}.svg"] = render_reach(metrics, theme)
        output[f"coding.{theme.name}.svg"] = render_coding(metrics, theme)
        output[f"distribution.{theme.name}.svg"] = render_distribution(metrics, theme)
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", default="pypi-ahmad")
    parser.add_argument("--out-dir", default="profile-stats")
    parser.add_argument("--recent-days", type=int, default=30)
    parser.add_argument("--timezone", default="Asia/Kolkata")
    args = parser.parse_args()
    if args.recent_days < 1:
        parser.error("--recent-days must be positive")

    token = os.environ.get("METRICS_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        parser.error("METRICS_TOKEN or GH_TOKEN is required")

    metrics = collect_metrics(GitHubClient(token), args.user, args.recent_days, args.timezone)
    rendered = render_all(metrics)
    output = Path(args.out_dir)
    output.mkdir(parents=True, exist_ok=True)
    for filename, content in rendered.items():
        (output / filename).write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
