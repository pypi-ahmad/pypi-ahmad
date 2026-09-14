import json
import sys
import tempfile
import unittest
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from dashboard_export import collect_dashboard, streaks, validate_dashboard, write_dashboard


class Client:
    def __init__(self):
        self.language_calls = 0

    def graphql(self, query, **variables):
        if "createdAt" in query:
            return {"user": {"createdAt": "2024-02-28T00:00:00Z", "contributionsCollection": {
                "totalCommitContributions": 3, "contributionCalendar": {"totalContributions": 3}}}}
        if "weeks" in query:
            days = [{"date": date, "contributionCount": count, "contributionLevel": "FIRST_QUARTILE" if count else "NONE"}
                    for date, count in [("2024-02-28", 1), ("2024-02-29", 2), ("2024-03-01", 0)]]
            return {"user": {"contributionsCollection": {"contributionCalendar": {"weeks": [{"contributionDays": days}]}}}}
        self.language_calls += 1
        return {"user": {"repositories": {"pageInfo": {"hasNextPage": self.language_calls == 1, "endCursor": "next"},
            "nodes": [{"languages": {"pageInfo": {"hasNextPage": False}, "edges": [{"size": 100, "node": {"name": "Python"}}]}}]}}}


def metrics():
    data = {key: 0 for key in ("repositories", "stars", "forks", "watchers", "reviews", "pull_requests",
        "merged_pull_requests", "open_issues", "closed_issues", "external_total", "lines_added", "lines_removed",
        "lines_coverage", "releases", "downloads", "release_coverage", "views", "clones", "traffic_coverage")}
    data.update({"login": "pypi-ahmad", "generated_at": datetime(2024, 3, 1, 12, tzinfo=timezone.utc),
        "recent_days": 30, "timezone": "Asia/Kolkata", "weekdays": Counter(), "hours": Counter(),
        "star_series": [], "external_recent": [], "active_repositories": [], "languages": [], "referrers": [],
        "private_payload": "must not be exported"})
    return data


class DashboardTests(unittest.TestCase):
    def test_calendar_streaks_cross_leap_day_and_allow_today(self):
        days = [{"date": date, "count": 1} for date in ("2024-02-28", "2024-02-29")]
        self.assertEqual(streaks(days, "2024-03-01"), {"current": 2, "longest": 2, "asOf": "2024-03-01"})
        self.assertEqual(streaks(days, "2024-03-02")["current"], 0)

    def test_streak_gaps_and_year_boundary(self):
        days = [{"date": date, "count": 1} for date in ("2023-12-29", "2023-12-31", "2024-01-01")]
        self.assertEqual(streaks(days, "2024-01-01")["longest"], 2)
        self.assertEqual(streaks([], "2024-01-01")["current"], 0)

    def test_export_paginates_and_uses_allowlist_and_nulls(self):
        client = Client()
        data = collect_dashboard(client, metrics())
        self.assertEqual(client.language_calls, 2)
        self.assertEqual(data["summary"]["languages"], [{"name": "Python", "bytes": 200}])
        self.assertEqual(data["years"][0]["total"], 3)
        self.assertEqual(data["summary"]["streak"]["current"], 2)
        self.assertIsNone(data["distribution"]["views"])
        self.assertIsNone(data["coding"]["linesAdded"])
        self.assertNotIn("private_payload", json.dumps(data))

    def test_covered_zero_is_not_unavailable(self):
        source = metrics()
        source.update({"repositories": 1, "traffic_coverage": 1, "release_coverage": 1, "lines_coverage": 1})
        data = collect_dashboard(Client(), source)
        self.assertEqual(data["distribution"]["views"], 0)
        self.assertEqual(data["coding"]["linesAdded"], 0)

    def test_invalid_output_never_replaces_previous_snapshot(self):
        data = collect_dashboard(Client(), metrics())
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "dashboard.json"
            write_dashboard(path, data)
            before = path.read_bytes()
            data["years"][0]["days"].append(data["years"][0]["days"][0])
            with self.assertRaises(ValueError):
                write_dashboard(path, data)
            self.assertEqual(path.read_bytes(), before)
            self.assertFalse(path.with_suffix(".json.tmp").exists())

    def test_rejects_nonfinite_and_wrong_year_or_total(self):
        for mutate in (
            lambda data: data.update(schemaVersion=2),
            lambda data: data["summary"].update(stars=float("nan")),
            lambda data: data["years"][0].update(year=2025),
            lambda data: data["years"][0].update(total=999),
        ):
            data = collect_dashboard(Client(), metrics())
            mutate(data)
            with self.assertRaises(ValueError):
                validate_dashboard(data)


if __name__ == "__main__":
    unittest.main()
