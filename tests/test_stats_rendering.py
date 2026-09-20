"""Regression checks for bounded labels in the retained statistics panels."""

import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from generate_github_stats import THEMES, _bars, _label, render_all
from test_dashboard_export import metrics

SVG = "{http://www.w3.org/2000/svg}"


class StatsRenderingTests(unittest.TestCase):
    def test_short_labels_remain_intact_and_special_characters_are_escaped(self):
        for theme in THEMES:
            for value in ("Python", "A&B <C>", ""):
                root = ET.fromstring(_label(28, 220, value, 302, theme))
                self.assertEqual(root.find("title").text or "", value)
                self.assertEqual(root.find("text").text or "", value)
                self.assertEqual(root.get("overflow"), "hidden")

    def test_long_labels_keep_full_title_and_stay_inside_their_column(self):
        value = "W" * 200 + "<&>"
        for theme in THEMES:
            for width in (97, 302, 414):
                root = ET.fromstring(_label(570, 306, value, width, theme))
                self.assertEqual(root.get("width"), str(width))
                self.assertEqual(root.get("overflow"), "hidden")
                self.assertEqual(root.find("title").text, value)
                visible = root.find("text").text
                self.assertTrue(visible.endswith("…"))
                self.assertLess(len(visible), len(value))

    def test_labels_do_not_overlap_or_change_bar_geometry(self):
        for theme in THEMES:
            root = ET.fromstring("<g>" + "".join(_bars(
                [("com.linkedin.android" * 5, 10), ("Python", 5)],
                28, 212, 520, theme,
            )) + "</g>")
            for label in root.findall("svg"):
                self.assertLess(int(label.get("x")) + int(label.get("width")), 133)
            bars = root.findall("rect")
            self.assertEqual([bar.get("width") for bar in bars], ["520", "520.0", "520", "260.0"])
            self.assertTrue(all(bar.get("x") == "133" for bar in bars))
            self.assertEqual([bar.get("y") for bar in bars], ["212", "212", "239", "239"])

    def test_panels_handle_empty_data_and_long_repository_names(self):
        for populated in (False, True):
            data = metrics()
            if populated:
                data["external_recent"] = ["owner/" + "W" * 200]
                data["active_repositories"] = [("repo<&>" * 40, "2026-09-20")]
                data["languages"] = [("Custom language " * 20, 10)]
                data["referrers"] = [("com.linkedin.android", 10)]
            rendered = render_all(data)
            self.assertEqual(len(rendered), 6)
            for filename, svg in rendered.items():
                root = ET.fromstring(svg)
                self.assertEqual(root.get("width"), "900")
                self.assertNotIn("nan", svg.lower())
                self.assertIn("Generated 2024-03-01 12:00 UTC", svg)
                for label in root.findall(f"{SVG}svg"):
                    self.assertEqual(label.get("overflow"), "hidden")
                    self.assertLessEqual(int(label.get("x")) + int(label.get("width")), 872)


if __name__ == "__main__":
    unittest.main()
