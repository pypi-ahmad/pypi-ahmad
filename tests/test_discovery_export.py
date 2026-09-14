import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from discovery_export import collect_discovery, public_url, release_records, validate_discovery


def repository(name="project", **extra):
    return {"name": name, "full_name": f"pypi-ahmad/{name}", "owner": {"login": "pypi-ahmad"},
            "private": False, "html_url": f"https://github.com/pypi-ahmad/{name}", "description": None,
            "language": "Python", "topics": ["ai"], "stargazers_count": 2, "fork": False,
            "archived": False, "created_at": "2024-01-01T00:00:00Z", "pushed_at": None, **extra}


def release(**extra):
    return {"id": 1, "name": "Release one", "tag_name": "v1", "html_url": "https://github.com/pypi-ahmad/project/releases/tag/v1",
            "published_at": "2024-01-01T00:00:00Z", "body": "Notes", "draft": False, "prerelease": False,
            "assets": [{"name": "file.zip", "browser_download_url": "https://github.com/pypi-ahmad/project/releases/download/v1/file.zip", "size": 10, "download_count": 3}], **extra}


class Client:
    def __init__(self):
        self.requests = []

    def rest(self, path, **params):
        self.requests.append((path, params))
        if path.startswith("/users/"):
            if params["page"] == 1:
                return [repository(f"p{i}", fork=True) for i in range(98)] + [repository("secret", private=True), repository("project", archived=True)]
            return [repository("other", owner={"login": "someone-else"})]
        return [release(), release(id=2, draft=True)]

    def graphql(self, query, **params):
        repo = {"nameWithOwner": "external/project", "owner": {"login": "external"}, "isPrivate": False}
        item = {"repository": repo, "number": 1, "title": "Improve tests", "bodyText": "Verified change", "url": "https://github.com/external/project/pull/1", "mergedAt": "2024-01-01T00:00:00Z"}
        if params.get("after"):
            return {"user": {"pullRequests": {"nodes": [item], "pageInfo": {"hasNextPage": False, "endCursor": None}}}}
        private = copy.deepcopy(item)
        private["repository"]["isPrivate"] = True
        own = copy.deepcopy(item)
        own["repository"]["owner"]["login"] = "pypi-ahmad"
        return {"user": {"pullRequests": {"nodes": [private, own], "pageInfo": {"hasNextPage": True, "endCursor": "next"}}}}


class DiscoveryTests(unittest.TestCase):
    def test_public_allowlist_pagination_archives_and_external_filter(self):
        client = Client()
        data = collect_discovery(client, "pypi-ahmad")
        self.assertEqual(len(data["repositories"]), 99)
        self.assertEqual(len(data["releases"]), 1)
        self.assertEqual(len(data["externalPullRequests"]), 1)
        self.assertEqual(data["externalPullRequests"][0]["repository"], "external/project")
        self.assertNotIn("private", data["repositories"][0])
        self.assertFalse(any("secret" in r["name"] for r in data["repositories"]))
        self.assertEqual(data["discoveryCoverage"]["releases"], "complete")

    def test_release_requests_are_reused_and_notes_bounded(self):
        client = Client()
        a = release_records(client, "pypi-ahmad", "project")
        self.assertIs(a, release_records(client, "pypi-ahmad", "project"))
        self.assertEqual(len(client.requests), 1)
        self.assertEqual(a[0]["assets"][0]["downloads"], 3)

    def test_release_pagination_and_failure_are_not_hidden(self):
        class Pages(Client):
            def rest(self, path, **params):
                return [release(id=i) for i in range(100)] if params["page"] == 1 else [release(id=101)]
        self.assertEqual(len(release_records(Pages(), "pypi-ahmad", "project")), 101)
        class Failure(Client):
            def rest(self, path, **params):
                raise RuntimeError("collection failed")
        with self.assertRaises(RuntimeError):
            collect_discovery(Failure(), "pypi-ahmad")

    def test_url_validation(self):
        for url in ["javascript:bad", "http://github.com/x", "https://github.com.evil/x", "https://user@github.com/x"]:
            with self.assertRaises(ValueError):
                public_url(url)

    def test_validation_rejects_bad_counts_dates_and_duplicate_records(self):
        data = collect_discovery(Client(), "pypi-ahmad")
        validate_discovery(data)
        for field, value in [("stars", -1), ("createdAt", "not-a-date")]:
            bad = copy.deepcopy(data)
            bad["repositories"][0][field] = value
            with self.assertRaises(ValueError):
                validate_discovery(bad)
        data["repositories"].append(data["repositories"][0])
        with self.assertRaises(ValueError):
            validate_discovery(data)
