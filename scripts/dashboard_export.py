"""Public, versioned portfolio data; intentionally excludes raw API responses."""

from __future__ import annotations

import json
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

PROFILE_QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
    contributionsCollection {
      totalCommitContributions
      contributionCalendar { totalContributions }
    }
  }
}
"""
CALENDAR_QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        weeks { contributionDays { date contributionCount contributionLevel } }
      }
    }
  }
}
"""
LANGUAGES_QUERY = """
query($login: String!, $after: String) {
  user(login: $login) {
    repositories(first: 100, after: $after, privacy: PUBLIC,
      ownerAffiliations: OWNER, isFork: false, isArchived: false) {
      pageInfo { hasNextPage endCursor }
      nodes { languages(first: 100) { pageInfo { hasNextPage } edges { size node { name } } } }
    }
  }
}
"""
LEVELS = {name: index for index, name in enumerate((
    "NONE", "FIRST_QUARTILE", "SECOND_QUARTILE", "THIRD_QUARTILE", "FOURTH_QUARTILE"
))}


def streaks(days: list[dict], today: str) -> dict:
    """Use calendar dates, including gaps; allow the current day to be unfinished."""
    counts = {item["date"]: item["count"] for item in days if item["date"] <= today}
    longest = running = 0
    previous = None
    for stamp in sorted(counts):
        current_date = date.fromisoformat(stamp)
        if previous is not None and current_date != previous + timedelta(days=1):
            running = 0
        running = running + 1 if counts[stamp] > 0 else 0
        longest = max(longest, running)
        previous = current_date
    cursor = date.fromisoformat(today)
    if counts.get(cursor.isoformat(), 0) == 0:
        cursor -= timedelta(days=1)
    current = 0
    while counts.get(cursor.isoformat(), 0) > 0:
        current += 1
        cursor -= timedelta(days=1)
    return {"current": current, "longest": longest, "asOf": today}


def collect_dashboard(client, metrics: dict, *, include_discovery=False) -> dict:
    login, now = metrics["login"], metrics["generated_at"]
    profile = client.graphql(PROFILE_QUERY, login=login)["user"]
    created = date.fromisoformat(profile["createdAt"][:10])
    years = []
    for year in range(created.year, now.year + 1):
        start = max(datetime(year, 1, 1, tzinfo=timezone.utc), datetime.fromisoformat(profile["createdAt"].replace("Z", "+00:00")))
        end = min(datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc), now)
        calendar = client.graphql(CALENDAR_QUERY, login=login, **{
            "from": start.isoformat(), "to": end.isoformat()
        })["user"]["contributionsCollection"]["contributionCalendar"]
        days = [{"date": day["date"], "count": day["contributionCount"],
                 "level": LEVELS[day["contributionLevel"]]}
                for week in calendar["weeks"] for day in week["contributionDays"]
                if day["date"].startswith(str(year)) and created.isoformat() <= day["date"] <= now.date().isoformat()]
        years.append({"year": year, "days": days, "total": sum(day["count"] for day in days)})

    language_bytes = Counter()
    after = None
    while True:
        connection = client.graphql(LANGUAGES_QUERY, login=login, after=after)["user"]["repositories"]
        for repo in connection["nodes"]:
            if repo["languages"]["pageInfo"]["hasNextPage"]:
                raise ValueError("Repository language coverage exceeds the export limit")
            for edge in repo["languages"]["edges"]:
                language_bytes[edge["node"]["name"]] += edge["size"]
        if not connection["pageInfo"]["hasNextPage"]:
            break
        after = connection["pageInfo"]["endCursor"]

    def covered(key, coverage):
        return metrics[key] if metrics[coverage] else None

    all_days = [day for year in years for day in year["days"]]
    result = {
        "schemaVersion": 1, "login": login, "generatedAt": now.isoformat(),
        "scope": "Repository metrics cover public, owned, non-fork, non-archived repositories. Contribution totals are GitHub profile aggregates and may include private contribution counts; private repository identities are never exported.",
        "summary": {
            "stars": metrics["stars"], "repositories": metrics["repositories"],
            "contributions": profile["contributionsCollection"]["contributionCalendar"]["totalContributions"],
            "commits": profile["contributionsCollection"]["totalCommitContributions"],
            "pullRequests": metrics["pull_requests"],
            "issues": metrics["open_issues"] + metrics["closed_issues"],
            "streak": streaks(all_days, now.date().isoformat()),
            "languages": [{"name": name, "bytes": value} for name, value in language_bytes.most_common()],
        },
        "reach": {key: metrics[key] for key in (
            "forks", "watchers", "reviews", "pull_requests", "merged_pull_requests",
            "open_issues", "closed_issues", "external_total", "external_recent", "star_series")},
        "coding": {
            "recentDays": metrics["recent_days"], "timezone": metrics["timezone"],
            "linesAdded": covered("lines_added", "lines_coverage"),
            "linesRemoved": covered("lines_removed", "lines_coverage"),
            "coverage": metrics["lines_coverage"], "repositories": metrics["repositories"],
            "activeRepositories": metrics["active_repositories"], "languages": metrics["languages"],
            "weekdays": [metrics["weekdays"].get(i, 0) for i in range(7)],
            "hours": [metrics["hours"].get(i, 0) for i in range(24)],
            "method": "Recent languages are estimated from repository language bytes weighted by attributed commits. Commit habits sample up to 100 default-branch commits per repository in the recent window, across up to 100 repositories.",
        },
        "distribution": {
            "releases": covered("releases", "release_coverage"),
            "downloads": covered("downloads", "release_coverage"),
            "views": covered("views", "traffic_coverage"),
            "clones": covered("clones", "traffic_coverage"),
            "releaseCoverage": metrics["release_coverage"], "trafficCoverage": metrics["traffic_coverage"],
            "repositories": metrics["repositories"], "referrers": metrics["referrers"], "trafficDays": 14,
        },
        "years": years,
    }
    if include_discovery:
        from discovery_export import collect_discovery
        result.update(collect_discovery(client, login))
    validate_dashboard(result)
    return result


def validate_dashboard(data: dict) -> None:
    from discovery_export import validate_discovery
    validate_discovery(data)
    if data.get("schemaVersion") != 1 or not data.get("years"):
        raise ValueError("Missing dashboard version or history")
    datetime.fromisoformat(data["generatedAt"])
    seen = set()
    for year in data["years"]:
        for day in year["days"]:
            stamp = date.fromisoformat(day["date"])
            if stamp.year != year["year"] or stamp in seen or type(day["count"]) is not int or day["count"] < 0 or day["level"] not in range(5):
                raise ValueError("Invalid contribution day")
            seen.add(stamp)
        if year["total"] != sum(day["count"] for day in year["days"]):
            raise ValueError("Contribution total mismatch")
    # NaN is not JSON and must never silently reach the browser.
    json.dumps(data, allow_nan=False)


def write_dashboard(path: Path, data: dict) -> None:
    validate_dashboard(data)
    content = json.dumps(data, ensure_ascii=False, allow_nan=False, separators=(",", ":")) + "\n"
    temporary = path.with_suffix(".json.tmp")
    try:
        temporary.write_text(content, encoding="utf-8")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)
