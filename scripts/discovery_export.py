"""Allowlisted public discovery records for the portfolio's focused views."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from urllib.parse import urlsplit


def public_url(value):
    parsed = urlsplit(value or "")
    if parsed.scheme != "https" or parsed.hostname != "github.com" or parsed.username or parsed.password:
        raise ValueError("Expected a public GitHub HTTPS link")
    return value


def validate_discovery(data):
    def strings(item, names):
        if not all(isinstance(item.get(name), str) for name in names):
            raise ValueError("Invalid public text field")

    def number(value):
        if type(value) is not int or value < 0:
            raise ValueError("Invalid public count")

    for key in ("repositories", "releases", "externalPullRequests"):
        if key not in data:
            continue
        if not isinstance(data[key], list):
            raise ValueError("Invalid public collection")
        seen = set()
        for item in data[key]:
            public_url(item["url"])
            if item["url"] in seen:
                raise ValueError("Duplicate public record")
            seen.add(item["url"])
            if key == "repositories":
                strings(item, ("name", "fullName", "description", "language"))
                if not isinstance(item["topics"], list) or not all(isinstance(t, str) for t in item["topics"]) or type(item["fork"]) is not bool or type(item["archived"]) is not bool:
                    raise ValueError("Invalid repository metadata")
                number(item["stars"])
                datetime.fromisoformat(item["createdAt"].replace("Z", "+00:00"))
                if item["pushedAt"] is not None:
                    datetime.fromisoformat(item["pushedAt"].replace("Z", "+00:00"))
            elif key == "releases":
                strings(item, ("repository", "title", "tag", "notes"))
                number(item["id"])
                datetime.fromisoformat(item["publishedAt"].replace("Z", "+00:00"))
                if type(item["prerelease"]) is not bool or not isinstance(item["assets"], list):
                    raise ValueError("Invalid release metadata")
                for asset in item["assets"]:
                    strings(asset, ("name",))
                    public_url(asset["url"])
                    number(asset["size"])
                    number(asset["downloads"])
            else:
                strings(item, ("repository", "title", "description"))
                number(item["number"])
                datetime.fromisoformat(item["mergedAt"].replace("Z", "+00:00"))


def release_records(client, owner, name):
    cache = getattr(client, "dashboard_release_cache", None)
    if cache is None:
        cache = client.dashboard_release_cache = {}
    key = f"{owner}/{name}"
    if key in cache:
        return cache[key]
    records, page = [], 1
    while True:
        batch = client.rest(f"/repos/{key}/releases", per_page=100, page=page)
        for item in batch:
            if item.get("draft"):
                continue
            records.append({
                "id": item["id"], "repository": key,
                "title": item.get("name") or item["tag_name"], "tag": item["tag_name"],
                "url": public_url(item["html_url"]), "publishedAt": item["published_at"],
                "prerelease": bool(item.get("prerelease")),
                "notes": (item.get("body") or "").strip()[:600],
                "assets": [{"name": asset["name"], "url": public_url(asset["browser_download_url"]),
                            "size": asset["size"], "downloads": asset.get("download_count", 0)}
                           for asset in item.get("assets", [])],
            })
        if len(batch) < 100:
            cache[key] = records
            return records
        page += 1


PULL_REQUESTS = """
query($login: String!, $after: String) {
  user(login: $login) {
    pullRequests(first: 100, after: $after, states: MERGED,
      orderBy: {field: UPDATED_AT, direction: DESC}) {
      pageInfo { hasNextPage endCursor }
      nodes { number title bodyText url mergedAt
        repository { nameWithOwner isPrivate owner { login } } }
    }
  }
}
"""


def collect_discovery(client, login):
    repositories, page = [], 1
    while True:
        batch = client.rest(f"/users/{login}/repos", type="owner", per_page=100, page=page)
        for item in batch:
            if item.get("private") or item["owner"]["login"].lower() != login.lower():
                continue
            repositories.append({
                "name": item["name"], "fullName": item["full_name"],
                "url": public_url(item["html_url"]), "description": item.get("description") or "",
                "language": item.get("language") or "", "topics": item.get("topics") or [],
                "stars": item["stargazers_count"], "fork": bool(item["fork"]),
                "archived": bool(item["archived"]), "createdAt": item["created_at"],
                "pushedAt": item.get("pushed_at"),
            })
        if len(batch) < 100:
            break
        page += 1
    originals = [repo for repo in repositories if not repo["fork"]]
    # Fail the export rather than label a partially collected release year complete.
    with ThreadPoolExecutor(max_workers=6) as executor:
        batches = list(executor.map(lambda repo: release_records(client, login, repo["name"]), originals))
    releases = sorted((item for batch in batches for item in batch), key=lambda item: item["publishedAt"], reverse=True)
    contributions, after = [], None
    while True:
        connection = client.graphql(PULL_REQUESTS, login=login, after=after)["user"]["pullRequests"]
        for item in connection["nodes"]:
            repo = item["repository"]
            if repo["isPrivate"] or repo["owner"]["login"].lower() == login.lower():
                continue
            contributions.append({"number": item["number"], "title": item["title"],
                                  "repository": repo["nameWithOwner"], "url": public_url(item["url"]),
                                  "mergedAt": item["mergedAt"], "description": item["bodyText"].strip()[:400]})
        if not connection["pageInfo"]["hasNextPage"]:
            break
        after = connection["pageInfo"]["endCursor"]
    return {
        "repositories": sorted(repositories, key=lambda repo: repo["fullName"].lower()),
        "releases": releases,
        "externalPullRequests": sorted(contributions, key=lambda item: item["mergedAt"], reverse=True),
        "discoveryCoverage": {"repositories": "complete", "releases": "complete", "externalPullRequests": "complete",
                              "scope": "Currently public owned repositories. Release and creation history includes archived originals, excludes forks, and cannot include deleted or private repositories."},
    }
