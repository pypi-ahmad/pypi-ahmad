from __future__ import annotations

import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import generate_repo_cards as cards


class RepoCardTests(unittest.TestCase):
    def test_partial_fetch_failure_keeps_existing_card(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            repos_file = root / "repos.txt"
            out_dir = root / "cards"
            repos_file.write_text("owner/good\nowner/failing\n", encoding="utf-8")
            out_dir.mkdir()
            for theme in cards.THEMES:
                (out_dir / f"failing.{theme.suffix}.svg").write_text("stale", encoding="utf-8")

            def fetch_repo(owner: str, repo: str, **_: object) -> cards.RepoInfo:
                if repo == "failing":
                    raise RuntimeError("HTTP Error 504: Gateway Time-out")
                return cards.RepoInfo(
                    owner,
                    repo,
                    "description",
                    1,
                    2,
                    "Python",
                    "2026-08-18",
                    "https://example.com",
                )

            argv = ["generate_repo_cards.py", "--repos-file", str(repos_file), "--out-dir", str(out_dir)]
            with patch.object(sys, "argv", argv), patch.object(cards, "_fetch_repo", side_effect=fetch_repo):
                self.assertEqual(cards.main(), 0)

            for theme in cards.THEMES:
                stale_card = out_dir / f"failing.{theme.suffix}.svg"
                self.assertEqual(stale_card.read_text(encoding="utf-8"), "stale")
                self.assertIn("<svg", (out_dir / f"good.{theme.suffix}.svg").read_text(encoding="utf-8"))

    def test_all_fetches_failing_returns_failure(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            repos_file = root / "repos.txt"
            repos_file.write_text("owner/failing\n", encoding="utf-8")
            argv = ["generate_repo_cards.py", "--repos-file", str(repos_file), "--out-dir", str(root / "cards")]

            with (
                patch.object(sys, "argv", argv),
                patch.object(cards, "_fetch_repo", side_effect=RuntimeError("HTTP Error 504: Gateway Time-out")),
                self.assertRaises(SystemExit),
            ):
                cards.main()


if __name__ == "__main__":
    unittest.main()
