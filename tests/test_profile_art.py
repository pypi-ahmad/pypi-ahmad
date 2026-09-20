"""Checks for bounded, accessible, deterministic profile artwork."""

import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from generate_profile_art import (  # noqa: E402
    CONTACTS,
    DISPLAY,
    MONO,
    SECTIONS,
    contact_aurora,
    contact_cell,
    cta,
    featured_row,
    section_header,
    telemetry,
    workshop,
)
from generate_repo_cards import FEATURED, THEMES, RepoInfo, _render_svg  # noqa: E402


class ProfileArtTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.readme = (cls.root / "README.md").read_text(encoding="utf-8")

    def test_theme_palette_and_typography_are_consistent(self):
        expected = {
            "dark": (
                "#0C0C0D", "#151517", "#343438", "#F4F1EA", "#C9C5BD",
                "#96928A", "#FF5A5F", "#B8BCC4", "#FF5A5F",
            ),
            "light": (
                "#F2EFE8", "#FFFEFA", "#D2CEC5", "#171719", "#3F3E42",
                "#66635E", "#B4232F", "#565A62", "#B4232F",
            ),
        }
        legacy = (
            "#020A05", "#06120A", "#174D2A", "#E7FFEC", "#B8D8C0",
            "#86A88F", "#39FF14", "#00E676", "#F2B134", "#39D9FF",
        )
        for theme in THEMES:
            self.assertEqual(
                (theme.bg, theme.bg2, theme.border, theme.title, theme.text,
                 theme.muted, theme.accent, theme.system, theme.live),
                expected[theme.name],
            )
            for renderer in (telemetry, contact_aurora):
                svg = renderer(theme)
                self.assertIn(MONO, svg)
                self.assertFalse(any(color in svg for color in legacy))
        self.assertNotEqual(expected["dark"], expected["light"])

    def test_readable_text_colors_clear_wcag_contrast(self):
        def luminance(color):
            channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
            channels = [value / 12.92 if value <= .03928 else ((value + .055) / 1.055) ** 2.4 for value in channels]
            return .2126 * channels[0] + .7152 * channels[1] + .0722 * channels[2]

        for theme in THEMES:
            for foreground in (theme.title, theme.text, theme.muted, theme.accent, theme.system):
                for background in (theme.bg, theme.bg2):
                    lighter, darker = sorted((luminance(foreground), luminance(background)), reverse=True)
                    self.assertGreaterEqual((lighter + .05) / (darker + .05), 4.5)

    def test_generated_assets_are_adaptive_parseable_and_green_free(self):
        legacy = ("#020A05", "#06120A", "#174D2A", "#E7FFEC", "#39FF14", "#00E676")
        asset_dir = self.root / "assets" / "profile"
        dark_assets = sorted(asset_dir.glob("*.dark.svg"))
        self.assertEqual(len(dark_assets), 34)
        for dark_path in dark_assets:
            light_path = dark_path.with_name(dark_path.name.replace(".dark.svg", ".light.svg"))
            dark = dark_path.read_text(encoding="utf-8")
            light = light_path.read_text(encoding="utf-8")
            ET.fromstring(dark)
            ET.fromstring(light)
            self.assertNotEqual(dark, light)
            self.assertFalse(any(color in dark or color in light for color in legacy))

        self.assertIn("color=0C0C0D", self.readme)
        self.assertIn("color=F2EFE8", self.readme)

    def test_every_major_section_has_a_numbered_semantic_header(self):
        self.assertEqual(len(SECTIONS), 14)
        for index, (name, (title, label)) in enumerate(SECTIONS.items(), 1):
            themed = []
            for theme in THEMES:
                svg = section_header(theme, index, title, label)
                themed.append(svg)
                node = ET.fromstring(svg)
                self.assertEqual(node.get("viewBox"), "0 0 960 92")
                self.assertIn(f"{index:02d} /", svg)
                self.assertIn(title.replace("&", "&amp;"), svg)
                self.assertIn(label, svg)
                self.assertIn(MONO, svg)
                self.assertIn(DISPLAY, svg)
                for color in (theme.bg, theme.bg2, theme.accent, theme.system, theme.title, theme.muted, theme.border):
                    self.assertIn(color, svg)
                self.assertIn(f"assets/profile/section-{name}.{theme.suffix}.svg", self.readme)
            self.assertNotEqual(themed[0], themed[1])
            heading_id = {
                "skills": "skills-with-context",
                "fde": "forward-deployed-ai-engineering",
                "education": "education--credentials",
                "contact": "contact--availability",
            }.get(name, name)
            self.assertIn(f'<h2 id="{heading_id}">', self.readme)

    def test_telemetry_is_adaptive_and_complete(self):
        for theme in THEMES:
            svg = telemetry(theme)
            ET.fromstring(svg)
            for value in ("FOCUS", "multimodal AI", "LOCATION", "Gurugram", "STATUS", "available", "MODE", "production"):
                self.assertIn(value, svg)
            self.assertIn(f"assets/profile/telemetry.{theme.suffix}.svg", self.readme)

    def test_header_ctas_are_adaptive_accessible_and_keep_brand_art(self):
        expected = {
            "portfolio": ("View portfolio", ("#EA4335", "#FBBC04", "#34A853", "#4285F4")),
            "email": ("Email Ahmad Mujtaba", ("#4285F4", "#34A853", "#EA4335", "#FBBC04", "#C5221F")),
            "linkedin": ("Connect on LinkedIn", ("#0A66C2", "M416 32H31.9")),
        }
        for kind, (title, marks) in expected.items():
            for theme in THEMES:
                svg = cta(theme, kind)
                node = ET.fromstring(svg)
                self.assertEqual(node.get("viewBox"), "0 0 240 56")
                self.assertEqual(node.find("{http://www.w3.org/2000/svg}title").text, title)
                self.assertIn(MONO, svg)
                self.assertIn(DISPLAY, svg)
                for mark in marks:
                    self.assertIn(mark, svg)
                self.assertIn(f"assets/profile/cta-{kind}.{theme.suffix}.svg", self.readme)
        for destination in (
            'href="https://pypi-ahmad.github.io/"',
            'href="mailto:ahmad.iiitk@gmail.com"',
            'href="https://www.linkedin.com/in/ahmad-mle/"',
        ):
            self.assertIn(destination, self.readme)

    def test_featured_projects_are_full_width_editorial_rows(self):
        for repo, (title, category, description, _, flow) in FEATURED.items():
            for theme in THEMES:
                svg = featured_row(theme, repo)
                root = ET.fromstring(svg)
                self.assertEqual(root.get("viewBox"), "0 0 960 180")
                self.assertEqual(root.find("{http://www.w3.org/2000/svg}title").text, title)
                self.assertIn(category, svg)
                self.assertIn("ARCHITECTURE FLOW", svg)
                self.assertIn("VIEW CODE", svg)
                for node in flow:
                    self.assertIn(node, svg)
                self.assertIn(f'width="960" alt="{title if title != "Prompt optimizer" else "Self-Improving Prompt Optimizer"}', self.readme)
            self.assertIn(f'href="https://github.com/pypi-ahmad/{repo}"', self.readme)
            self.assertIn(description, featured_row(THEMES[0], repo).replace("…", "…"))

    def test_contact_directory_preserves_all_destinations_as_cells(self):
        destinations = (
            "mailto:ahmad.iiitk@gmail.com",
            "https://www.linkedin.com/in/ahmad-mle/",
            "https://wa.me/pypi_ahmad",
            "https://t.me/dataintuitionist",
            "https://pypi-ahmad.github.io/",
            "https://github.com/pypi-ahmad",
            "https://x.com/pypi_ahmad",
            "https://www.instagram.com/dataintuitionist/",
            "https://www.facebook.com/dataintuitionist/",
        )
        self.assertEqual(len(CONTACTS), 9)
        self.assertIn("DIRECT CHANNELS", self.readme)
        self.assertIn("ELSEWHERE", self.readme)
        self.assertNotIn('src="contacts-icons/', self.readme)
        for key in CONTACTS:
            for theme in THEMES:
                svg = contact_cell(theme, key)
                ET.fromstring(svg)
                self.assertIn(MONO, svg)
                self.assertIn(DISPLAY, svg)
                self.assertIn(f"assets/profile/contact-{key}.{theme.suffix}.svg", self.readme)
        for destination in destinations:
            self.assertIn(f'href="{destination}"', self.readme)

    def test_contact_banner_and_workshop_are_accessible(self):
        for theme in THEMES:
            banner = contact_aurora(theme)
            self.assertEqual(banner, (self.root / "assets" / "profile" / f"contact-aurora.{theme.suffix}.svg").read_text(encoding="utf-8"))
            self.assertIn("Let’s work together", banner)
            for animated in (True, False):
                svg = workshop(theme, animated=animated)
                root = ET.fromstring(svg)
                self.assertEqual(root.get("viewBox"), "0 0 960 260")
                self.assertIn("DATAINTUITIONIST IN", svg)
                self.assertIn("ILLUSTRATIVE TRACE", svg)
                self.assertIn('<g transform="translate(72 78)"><g class="paper">', svg)
                for line in ("document received", "layout parsed", "fields extracted", "evaluation passed", "review required · 2 fields"):
                    self.assertIn(line, svg)
                if animated:
                    self.assertIn("12s linear infinite", svg)
                    self.assertIn("prefers-reduced-motion:reduce", svg)
                else:
                    self.assertNotIn("@keyframes", svg)

    def test_live_repo_card_text_is_escaped_and_bounded(self):
        info = RepoInfo("someone", "a" * 140, 'Read <data> & compare "results" ' * 20, 12, 3, "Python", "2026-09-20T12:00:00Z", "https://example.com")
        for theme in THEMES:
            root = ET.fromstring(_render_svg(info, theme))
            texts = root.findall(".//{http://www.w3.org/2000/svg}text")
            titles = [text.text for text in texts if text.get("font-size") == "24"]
            descriptions = [text.text for text in texts if text.get("font-size") == "18"]
            self.assertLessEqual(len(titles), 2)
            self.assertTrue(all(len(line) <= 25 for line in titles))
            self.assertLessEqual(len(descriptions), 3)
            self.assertTrue(all(len(line) <= 36 for line in descriptions))
            serialized = ET.tostring(root, encoding="unicode")
            self.assertIn("★ 12", serialized)
            self.assertIn("Updated 2026-09-20", serialized)

    def test_curated_copy_is_scoped_to_profile_owner(self):
        info = RepoInfo("another-owner", "video-summarizer", "Another implementation.", 0, 0, "", "", "")
        svg = _render_svg(info, THEMES[0])
        self.assertIn("Another implementation.", svg)
        self.assertNotIn("04 / MULTIMODAL", svg)


if __name__ == "__main__":
    unittest.main()
