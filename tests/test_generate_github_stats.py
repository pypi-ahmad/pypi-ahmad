from __future__ import annotations

import sys
import unittest
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import generate_github_stats as stats


class FakeGraphQLClient:
    def __init__(self) -> None:
        self.repository_page = 0

    def graphql(self, query: str, **variables):
        if query == stats.REPOSITORIES_QUERY:
            self.repository_page += 1
            name = f"repo-{self.repository_page}"
            return {
                "user": {
                    "repositories": {
                        "pageInfo": {
                            "hasNextPage": self.repository_page == 1,
                            "endCursor": f"page-{self.repository_page}",
                        },
                        "nodes": [
                            {
                                "name": name,
                                "nameWithOwner": f"owner/{name}",
                                "stargazers": {
                                    "pageInfo": {"hasNextPage": self.repository_page == 1, "endCursor": "star-page"},
                                    "edges": [{"starredAt": "2024-01-01T00:00:00Z"}],
                                },
                            }
                        ],
                    }
                }
            }
        if query == stats.STARGAZERS_QUERY:
            return {
                "repository": {
                    "stargazers": {
                        "pageInfo": {"hasNextPage": False, "endCursor": None},
                        "edges": [{"starredAt": "2024-02-01T00:00:00Z"}],
                    }
                }
            }
        raise AssertionError("unexpected query")


class FakeRecentClient:
    def graphql(self, query: str, **variables):
        self.query = query
        return {
            "user": {
                "contributionsCollection": {
                    "commitContributionsByRepository": [
                        {
                            "contributions": {"totalCount": 4},
                            "repository": {
                                "languages": {
                                    "edges": [
                                        {"size": 75, "node": {"name": "Python"}},
                                        {"size": 25, "node": {"name": "HTML"}},
                                    ]
                                },
                                "defaultBranchRef": {
                                    "target": {
                                        "history": {
                                            "nodes": [
                                                {"committedDate": "2026-08-10T18:30:00Z"},
                                                {"committedDate": "2026-08-11T06:30:00Z"},
                                            ]
                                        }
                                    }
                                },
                            },
                        }
                    ]
                }
            }
        }


class FakeReleaseClient:
    def rest(self, path: str, **params):
        return [
            {"draft": False, "assets": [{"download_count": 3}, {"download_count": 2}]},
            {"draft": True, "assets": [{"download_count": 99}]},
        ]


class GitHubStatsTests(unittest.TestCase):
    def test_repository_and_stargazer_pagination(self) -> None:
        repositories = stats._load_repositories(FakeGraphQLClient(), "owner")

        self.assertEqual([repo["name"] for repo in repositories], ["repo-1", "repo-2"])
        self.assertEqual(len(repositories[0]["stargazers"]["edges"]), 2)

    def test_monthly_star_series_is_cumulative(self) -> None:
        repositories = [
            {
                "stargazers": {
                    "edges": [
                        {"starredAt": "2024-01-05T00:00:00Z"},
                        {"starredAt": "2024-03-05T00:00:00Z"},
                    ]
                }
            }
        ]

        series = stats._monthly_star_series(
            repositories,
            "2024-01-01T00:00:00Z",
            datetime(2024, 3, 20, tzinfo=timezone.utc),
        )

        self.assertEqual(series, [("2024-01", 1), ("2024-02", 1), ("2024-03", 2)])

    def test_recent_language_weighting_and_local_commit_buckets(self) -> None:
        client = FakeRecentClient()

        languages, weekdays, hours = stats._recent_activity(
            client,
            "owner",
            "USER_123",
            datetime(2026, 8, 14, tzinfo=timezone.utc),
            30,
            "Asia/Kolkata",
        )

        self.assertEqual(languages, Counter({"Python": 3.0, "HTML": 1.0}))
        self.assertEqual(weekdays, Counter({1: 2}))
        self.assertEqual(hours, Counter({0: 1, 12: 1}))
        self.assertIn('author: {id: "USER_123"}', client.query)

    def test_release_totals_exclude_drafts(self) -> None:
        self.assertEqual(stats._published_releases(FakeReleaseClient(), "owner", "repo"), (1, 5))

    def test_percent_handles_empty_denominator(self) -> None:
        self.assertEqual(stats._percent(1, 0), 0)
        self.assertEqual(stats._percent(3, 4), 75)

    def test_all_rendered_panels_are_valid_xml_and_escape_api_text(self) -> None:
        metrics = {
            "generated_at": datetime(2026, 8, 14, tzinfo=timezone.utc),
            "login": "owner",
            "recent_days": 30,
            "timezone": "Asia/Kolkata",
            "repositories": 2,
            "stars": 2,
            "star_series": [("2026-07", 1), ("2026-08", 2)],
            "forks": 1,
            "watchers": 1,
            "reviews": 4,
            "pull_requests": 5,
            "merged_pull_requests": 4,
            "open_issues": 1,
            "closed_issues": 2,
            "external_total": 1,
            "external_recent": ["other/a&b"],
            "active_repositories": [("repo<one>", "2026-08-14")],
            "languages": [("Python", 3.0)],
            "weekdays": Counter({0: 1}),
            "hours": Counter({10: 1}),
            "lines_added": 10,
            "lines_removed": 2,
            "lines_coverage": 2,
            "releases": 1,
            "downloads": 5,
            "release_coverage": 2,
            "views": 20,
            "clones": 3,
            "traffic_coverage": 2,
            "referrers": [("example.com?a=1&b=2", 3)],
        }

        rendered = stats.render_all(metrics)

        self.assertEqual(len(rendered), 6)
        for svg in rendered.values():
            ET.fromstring(svg)
        self.assertIn("other/a&amp;b", rendered["reach.dark.svg"])
        self.assertIn("repo&lt;one&gt;", rendered["coding.light.svg"])


if __name__ == "__main__":
    unittest.main()
