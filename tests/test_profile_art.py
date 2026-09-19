"""Checks for bounded, escaped card text and accessible profile artwork."""

import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from generate_profile_art import workshop
from generate_repo_cards import FEATURED, THEMES, RepoInfo, _render_svg, _wrap


class ProfileArtTests(unittest.TestCase):
    def test_card_text_is_escaped_and_bounded_in_both_themes(self):
        for name in ("short", "a" * 140, 'tools-<&>"'):
            info = RepoInfo("someone", name, 'Read <data> & compare "results" ' * 20,
                            12, 3, "Python", "2026-09-20T12:00:00Z", "https://example.com")
            for theme in THEMES:
                with self.subTest(name=name, theme=theme.name):
                    root = ET.fromstring(_render_svg(info, theme))
                    texts = root.findall(".//{http://www.w3.org/2000/svg}text")
                    titles = [text.text for text in texts if text.get("font-size") == "24"]
                    descriptions = [text.text for text in texts if text.get("font-size") == "18"]
                    self.assertLessEqual(len(titles), 2)
                    self.assertTrue(all(len(line) <= 25 for line in titles))
                    self.assertLessEqual(len(descriptions), 3)
                    self.assertTrue(all(len(line) <= 36 for line in descriptions))
                    self.assertIn("★ 12", ET.tostring(root, encoding="unicode"))
                    self.assertIn("Updated 2026-09-20", ET.tostring(root, encoding="unicode"))

    def test_featured_covers_do_not_freeze_live_counts(self):
        for name, (title, _, description, _) in FEATURED.items():
            info = RepoInfo("pypi-ahmad", name, description, 999, 888, "Python", "2026-09-20", "")
            for theme in THEMES:
                svg = _render_svg(info, theme, show_metrics=False)
                root = ET.fromstring(svg)
                self.assertEqual(root.find("{http://www.w3.org/2000/svg}title").text, title)
                self.assertIn("INDEPENDENT PROJECT", svg)
                self.assertNotIn("999", svg)
                self.assertNotIn("2026-09-20", svg)

    def test_curated_copy_is_scoped_to_the_profile_owner(self):
        info = RepoInfo("another-owner", "video-summarizer", "Another implementation.", 0, 0, "", "", "")
        svg = _render_svg(info, THEMES[0])
        self.assertIn("Another implementation.", svg)
        self.assertNotIn("04 / MULTIMODAL", svg)

    def test_workshop_has_static_and_reduced_motion_versions(self):
        for theme in THEMES:
            for animated in (True, False):
                svg = workshop(theme, animated=animated)
                root = ET.fromstring(svg)
                self.assertEqual(root.get("viewBox"), "0 0 960 260")
                self.assertIsNotNone(root.find("{http://www.w3.org/2000/svg}title"))
                self.assertIsNotNone(root.find("{http://www.w3.org/2000/svg}desc"))
                if animated:
                    self.assertIn("12s linear infinite", svg)
                    self.assertIn("prefers-reduced-motion: reduce", svg)
                else:
                    self.assertNotIn("@keyframes", svg)
                    self.assertNotIn("animation:", svg)


if __name__ == "__main__":
    unittest.main()
