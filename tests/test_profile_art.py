"""Checks for bounded, escaped card text and accessible profile artwork."""

import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from generate_profile_art import SECTIONS, contact_aurora, section_divider, workshop
from generate_repo_cards import FEATURED, THEMES, RepoInfo, _render_svg, _wrap


class ProfileArtTests(unittest.TestCase):
    def test_every_major_section_has_a_themed_terminal_divider(self):
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")
        self.assertEqual(len(SECTIONS), 14)
        for name, (command, label) in SECTIONS.items():
            for theme in THEMES:
                with self.subTest(section=name, theme=theme.name):
                    svg = section_divider(theme, command, label)
                    node = ET.fromstring(svg)
                    self.assertEqual(node.get("viewBox"), "0 0 960 72")
                    self.assertIn(command, svg)
                    self.assertIn(label, svg)
                    self.assertIn("PowerShell", svg)
                    self.assertIn(r"PS C:\Users\Ahmad\profile&gt;", svg)
                    self.assertIn(f"assets/profile/section-{name}.{theme.suffix}.svg", readme)

    def test_header_ctas_are_local_accessible_svg_buttons(self):
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")
        expected = {
            "cta-portfolio.svg": ("View portfolio", "EXPLORE"),
            "cta-email.svg": ("Email Ahmad Mujtaba", "START A CONVERSATION"),
            "cta-linkedin.svg": ("Connect on LinkedIn", "PROFESSIONAL NETWORK"),
        }
        for filename, (title, eyebrow) in expected.items():
            with self.subTest(filename=filename):
                asset = root / "assets" / "profile" / filename
                svg = asset.read_text(encoding="utf-8")
                node = ET.fromstring(svg)
                self.assertEqual(node.get("viewBox"), "0 0 240 56")
                self.assertEqual(node.find("{http://www.w3.org/2000/svg}title").text, title)
                self.assertIn(eyebrow, svg)
                self.assertIn(f'assets/profile/{filename}', readme)
        self.assertNotIn("img.shields.io/badge/View%20portfolio", readme)
        for destination in (
            'href="https://pypi-ahmad.github.io/"',
            'href="mailto:ahmad.iiitk@gmail.com"',
            'href="https://www.linkedin.com/in/ahmad-mle/"',
        ):
            self.assertIn(destination, readme)

    def test_contact_directory_preserves_every_destination(self):
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")
        for theme in ("dark", "light"):
            banner = root / "assets" / "profile" / f"contact-aurora.{theme}.svg"
            svg = banner.read_text(encoding="utf-8")
            self.assertEqual(svg, contact_aurora(next(item for item in THEMES if item.name == theme)))
            node = ET.fromstring(svg)
            self.assertEqual(node.get("viewBox"), "0 0 960 160")
            self.assertEqual(node.find("{http://www.w3.org/2000/svg}title").text, "Let’s work together")
            self.assertIsNotNone(node.find("{http://www.w3.org/2000/svg}desc"))
            self.assertIn("LET’S WORK TOGETHER", svg)
            self.assertIn("PowerShell · Contact", svg)
            self.assertIn(f'assets/profile/contact-aurora.{theme}.svg', readme)
        self.assertNotIn("contact-divider.svg", readme)
        self.assertIn("DIRECT CHANNELS", readme)
        self.assertIn("ELSEWHERE", readme)
        for destination in (
            "mailto:ahmad.iiitk@gmail.com",
            "https://www.linkedin.com/in/ahmad-mle/",
            "https://wa.me/pypi_ahmad",
            "https://t.me/dataintuitionist",
            "https://pypi-ahmad.github.io/",
            "https://github.com/pypi-ahmad",
            "https://x.com/pypi_ahmad",
            "https://www.instagram.com/dataintuitionist/",
            "https://www.facebook.com/dataintuitionist/",
        ):
            self.assertIn(f'href="{destination}"', readme)

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
                self.assertIn("DATAINTUITIONIST IN", svg)
                self.assertIn("PowerShell · AI Workshop", svg)
                self.assertNotIn("AHMAD.M()", svg)
                if animated:
                    self.assertIn("12s linear infinite", svg)
                    self.assertIn("prefers-reduced-motion: reduce", svg)
                else:
                    self.assertNotIn("@keyframes", svg)
                    self.assertNotIn("animation:", svg)

    def test_workshop_is_always_visible_without_static_download_links(self):
        readme = (Path(__file__).resolve().parents[1] / "README.md").read_text(encoding="utf-8")
        self.assertIn('src="assets/profile/workshop.light.svg"', readme)
        self.assertNotIn("Animated AI workshop", readme)
        self.assertNotIn("Static illustration:", readme)


if __name__ == "__main__":
    unittest.main()
