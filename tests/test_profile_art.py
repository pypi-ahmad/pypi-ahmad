"""Checks for bounded, accessible, deterministic profile artwork."""

import sys
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from generate_profile_art import (  # noqa: E402
    CONTACTS,
    DISPLAY,
    MONO,
    SECTIONS,
    contact_aurora,
    contact_aurora_mobile,
    contact_cell,
    cta,
    featured_row,
    featured_row_mobile,
    section_header,
    telemetry,
    telemetry_mobile,
    workshop,
    workshop_mobile,
)
from generate_repo_cards import FEATURED, THEMES, RepoInfo, _render_svg  # noqa: E402


class ReadmeStructureParser(HTMLParser):
    """Collect the native HTML semantics GitHub preserves in the profile README."""

    def __init__(self):
        super().__init__()
        self.headings = []
        self.details = 0
        self.summaries = 0
        self.images = []
        self.anchor_depth = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a":
            self.anchor_depth += 1
        elif tag in {"h1", "h2"}:
            self.headings.append(tag)
        elif tag == "details":
            self.details += 1
        elif tag == "summary":
            self.summaries += 1
        elif tag == "img":
            self.images.append((attributes, self.anchor_depth > 0))

    def handle_endtag(self, tag):
        if tag == "a":
            self.anchor_depth -= 1


class ProfileArtTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.readme = (cls.root / "README.md").read_text(encoding="utf-8")

    def test_theme_palette_and_typography_are_consistent(self):
        expected = {
            "dark": (
                "#0C0C0D", "#151517", "#343438", "#F4F1EA", "#C9C5BD",
                "#96928A", "#FF5A5F", "#B8BCC4", "#5FD38D", "#F2B84B",
            ),
            "light": (
                "#F2EFE8", "#FFFEFA", "#D2CEC5", "#171719", "#3F3E42",
                "#66635E", "#B4232F", "#565A62", "#18794E", "#8A4F00",
            ),
        }
        legacy = (
            "#020A05", "#06120A", "#174D2A", "#E7FFEC", "#B8D8C0",
            "#86A88F", "#39FF14", "#00E676", "#F2B134", "#39D9FF",
        )
        for theme in THEMES:
            self.assertEqual(
                (theme.bg, theme.bg2, theme.border, theme.title, theme.text,
                 theme.muted, theme.accent, theme.system, theme.live,
                 theme.attention),
                expected[theme.name],
            )
            self.assertEqual(len({theme.accent, theme.live, theme.attention}), 3)
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
            for foreground in (
                theme.title, theme.text, theme.muted, theme.accent,
                theme.system, theme.live, theme.attention,
            ):
                for background in (theme.bg, theme.bg2):
                    lighter, darker = sorted((luminance(foreground), luminance(background)), reverse=True)
                    self.assertGreaterEqual((lighter + .05) / (darker + .05), 4.5)

    def test_generated_assets_are_adaptive_parseable_and_green_free(self):
        legacy = ("#020A05", "#06120A", "#174D2A", "#E7FFEC", "#39FF14", "#00E676")
        asset_dir = self.root / "assets" / "profile"
        dark_assets = sorted(asset_dir.glob("*.dark.svg"))
        self.assertEqual(len(dark_assets), 42)
        for dark_path in dark_assets:
            light_path = dark_path.with_name(dark_path.name.replace(".dark.svg", ".light.svg"))
            dark = dark_path.read_text(encoding="utf-8")
            light = light_path.read_text(encoding="utf-8")
            for svg in (dark, light):
                root = ET.fromstring(svg)
                self.assertEqual(root.get("role"), "img")
                self.assertTrue(root.get("aria-label") or root.get("aria-labelledby"))
                self.assertTrue(root.find("{http://www.w3.org/2000/svg}title").text.strip())
                self.assertTrue(root.find("{http://www.w3.org/2000/svg}desc").text.strip())
            self.assertNotEqual(dark, light)
            self.assertFalse(any(color in dark or color in light for color in legacy))

        self.assertIn("color=0C0C0D", self.readme)
        self.assertIn("color=F2EFE8", self.readme)

    def test_readme_uses_native_disclosures_and_descriptive_images(self):
        parser = ReadmeStructureParser()
        parser.feed(self.readme)

        self.assertEqual(parser.headings.count("h1"), 1)
        self.assertEqual(parser.headings.count("h2"), len(SECTIONS))
        self.assertNotRegex(self.readme, r"<h2[^>]*>\s*<picture>")
        self.assertEqual(parser.details, parser.summaries)
        self.assertNotRegex(self.readme, r"\btabindex\s*=")
        self.assertNotRegex(self.readme, r"\baria-hidden\s*=")

        footer_src = "https://capsule-render.vercel.app/api?type=waving&color=F2EFE8&height=90&section=footer"
        for attributes, is_functional in parser.images:
            source = attributes.get("src", "")
            alt = attributes.get("alt")
            if source == footer_src:
                self.assertEqual(alt, "")
            else:
                self.assertTrue(alt and alt.strip(), source)
            if is_functional:
                self.assertTrue(alt and alt.strip(), source)

    def test_workshop_uses_static_sources_before_animated_sources(self):
        dark_static = 'srcset="assets/profile/workshop-static.dark.svg"'
        light_static = 'srcset="assets/profile/workshop-static.light.svg"'
        dark_animated = 'srcset="assets/profile/workshop.dark.svg"'
        light_animated = 'src="assets/profile/workshop.light.svg"'
        mobile_dark_static = 'srcset="assets/profile/workshop-static-mobile.dark.svg"'
        mobile_light_static = 'srcset="assets/profile/workshop-static-mobile.light.svg"'
        mobile_dark_animated = 'srcset="assets/profile/workshop-mobile.dark.svg"'
        mobile_light_animated = 'srcset="assets/profile/workshop-mobile.light.svg"'
        self.assertLess(self.readme.index(dark_static), self.readme.index(dark_animated))
        self.assertLess(self.readme.index(light_static), self.readme.index(light_animated))
        self.assertLess(self.readme.index(mobile_dark_static), self.readme.index(mobile_dark_animated))
        self.assertLess(self.readme.index(mobile_light_static), self.readme.index(mobile_light_animated))

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
                self.assertNotIn(f"assets/profile/section-{name}.{theme.suffix}.svg", self.readme)
            self.assertNotEqual(themed[0], themed[1])
            heading_id = {
                "skills": "skills-with-context",
                "fde": "forward-deployed-ai-engineering",
                "education": "education--credentials",
                "contact": "contact--availability",
            }.get(name, name)
            heading_text = title.replace("&", "&amp;")
            self.assertIn(f'<h2 id="{heading_id}">{index:02d} / {heading_text}</h2>', self.readme)

    def test_telemetry_is_adaptive_and_complete(self):
        for theme in THEMES:
            svg = telemetry(theme)
            ET.fromstring(svg)
            mobile = telemetry_mobile(theme)
            self.assertEqual(ET.fromstring(mobile).get("viewBox"), "0 0 360 96")
            for value in ("FOCUS", "multimodal AI", "LOCATION", "Gurugram", "STATUS", "available", "MODE", "production"):
                self.assertIn(value, svg)
            self.assertIn(theme.live, svg)
            self.assertIn(theme.live, mobile)
            self.assertIn(f"assets/profile/telemetry-mobile.{theme.suffix}.svg", self.readme)
            self.assertIn(f"assets/profile/telemetry.{theme.suffix}.svg", self.readme)

    def test_header_ctas_are_adaptive_accessible_and_keep_brand_art(self):
        expected = {
            "portfolio": ("Open Ahmad Mujtaba's portfolio", ("#EA4335", "#FBBC04", "#34A853", "#4285F4")),
            "email": ("Email Ahmad Mujtaba", ("#4285F4", "#34A853", "#EA4335", "#FBBC04", "#C5221F")),
            "linkedin": ("Connect on LinkedIn", ("#0A66C2", "M416 32H31.9")),
        }
        for kind, (title, marks) in expected.items():
            for theme in THEMES:
                svg = cta(theme, kind)
                node = ET.fromstring(svg)
                self.assertEqual(node.get("viewBox"), "0 0 136 56")
                sizes = {text.get("font-size") for text in node.findall("{http://www.w3.org/2000/svg}text")}
                self.assertEqual(sizes, {"9", "12"})
                self.assertIn('d="M8 1H128"', svg)
                self.assertIn('stroke-width="2" stroke-linecap="round" stroke-linejoin="round"', svg)
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
                mobile = featured_row_mobile(theme, repo)
                root = ET.fromstring(svg)
                mobile_root = ET.fromstring(mobile)
                self.assertEqual(root.get("viewBox"), "0 0 600 160")
                self.assertEqual(mobile_root.get("viewBox"), "0 0 360 208")
                self.assertEqual(root.find("{http://www.w3.org/2000/svg}title").text, title)
                for variant, body_size in ((root, "16"), (mobile_root, "14")):
                    texts = variant.findall("{http://www.w3.org/2000/svg}text")
                    titles = [node.text for node in texts if node.get("font-size") == "22"]
                    descriptions = [node.text for node in texts if node.get("font-size") == body_size]
                    self.assertEqual(titles, [title])
                    self.assertEqual(" ".join(descriptions), description)
                    flow_text = next(node for node in texts if node.find("{http://www.w3.org/2000/svg}tspan") is not None)
                    self.assertEqual("".join(flow_text.itertext()), " → ".join(flow))
                self.assertEqual(
                    svg,
                    (self.root / "assets" / "profile" / f"{repo}.{theme.suffix}.svg").read_text(encoding="utf-8"),
                )
                self.assertIn(category, svg)
                self.assertIn("ARCHITECTURE FLOW", svg)
                self.assertIn("OPEN REPOSITORY", svg)
                for node in flow:
                    self.assertIn(node, svg)
                    self.assertIn(node, mobile)
                self.assertIn(f'width="600" alt="{title if title != "Prompt optimizer" else "Self-Improving Prompt Optimizer"}', self.readme)
                self.assertIn(f"assets/profile/{repo}-mobile.{theme.suffix}.svg", self.readme)
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
                node = ET.fromstring(svg)
                self.assertEqual(node.get("viewBox"), "0 0 136 72")
                sizes = {text.get("font-size") for text in node.findall("{http://www.w3.org/2000/svg}text")}
                self.assertNotIn("8.5", sizes)
                self.assertIn("10", sizes)
                self.assertIn('stroke-width="2" stroke-linecap="round" stroke-linejoin="round"', svg)
                self.assertIn(MONO, svg)
                self.assertIn(DISPLAY, svg)
                self.assertIn(f"assets/profile/contact-{key}.{theme.suffix}.svg", self.readme)
        for destination in destinations:
            self.assertIn(f'href="{destination}"', self.readme)

    def test_readme_layout_supports_narrow_and_zoomed_views(self):
        self.assertNotIn("max-width: 600px", self.readme)
        self.assertNotIn("max-width: 760px", self.readme)
        self.assertEqual(self.readme.count("max-width: 480px"), 16)
        self.assertNotIn('width="49%"', self.readme)
        self.assertNotIn('width="32%"', self.readme)
        self.assertNotIn('width="100%"', self.readme)
        self.assertNotIn('height="170"', self.readme)
        self.assertLessEqual(2 * 136, 288)

        compact_stats = {"stats.svg": "467", "top-langs.svg": "300", "streak.svg": "495"}
        for asset, width in compact_stats.items():
            self.assertRegex(
                self.readme,
                rf'<img[^>]+{asset}[^>]+width="{width}"',
            )

        for repo in ("computer-use", "grounded-docparse", "Agentic-Document-Extraction", "local-ai-chat-studio"):
            self.assertRegex(
                self.readme,
                rf'<img[^>]+{repo}\.light\.svg[^>]+width="390"',
            )

        parser = ReadmeStructureParser()
        parser.feed(self.readme)
        full_width_assets = {
            "telemetry.light.svg", "workshop.light.svg", "contact-aurora.light.svg",
            *(f"{repo}.light.svg" for repo in FEATURED),
        }
        for attributes, _ in parser.images:
            source = attributes.get("src", "")
            if (
                source.startswith("assets/profile/")
                and source.rsplit("/", 1)[-1] in full_width_assets
            ):
                self.assertEqual(attributes.get("width"), "600", source)
            elif "profile-3d-contrib/" in source or "/output/" in source or any(
                f"/profile-stats/{name}." in source
                for name in ("reach", "coding", "distribution")
            ):
                self.assertEqual(attributes.get("width"), "820", source)
            elif source.startswith("certifications/") and source.endswith(".png"):
                expected_width = "300" if "claude-certified-associate-foundations" in source else "390"
                self.assertEqual(attributes.get("width"), expected_width, source)

    def test_interface_links_name_their_destination(self):
        self.assertNotRegex(
            self.readme,
            r"\[(?:Repository|Portfolio study|Detailed experience|Demo)\]\(",
        )
        for label in (
            "View the LoRA Fine-tune Studio repository",
            "Read the Prompt Optimizer portfolio study",
            "Try the Hinglish Turn Detection demo",
            "Read about prior-authorization document processing",
            "Read about warranty processing",
        ):
            self.assertIn(f"[{label}]", self.readme)
        for alt in (
            "Open Ahmad Mujtaba’s portfolio",
            "View Ahmad Mujtaba on GitHub",
            "View Ahmad Mujtaba on X",
        ):
            self.assertIn(f'alt="{alt}"', self.readme)

    def test_contact_banner_and_workshop_are_accessible(self):
        for theme in THEMES:
            banner = contact_aurora(theme)
            mobile_banner = contact_aurora_mobile(theme)
            self.assertEqual(banner, (self.root / "assets" / "profile" / f"contact-aurora.{theme.suffix}.svg").read_text(encoding="utf-8"))
            self.assertEqual(mobile_banner, (self.root / "assets" / "profile" / f"contact-aurora-mobile.{theme.suffix}.svg").read_text(encoding="utf-8"))
            self.assertIn("Let’s work together", banner)
            self.assertIn("Let’s work together", mobile_banner)
            for animated in (True, False):
                svg = workshop(theme, animated=animated)
                mobile_svg = workshop_mobile(theme, animated=animated)
                root = ET.fromstring(svg)
                mobile_root = ET.fromstring(mobile_svg)
                self.assertEqual(root.get("viewBox"), "0 0 600 160")
                self.assertEqual(mobile_root.get("viewBox"), "0 0 360 240")
                self.assertIn("DATAINTUITIONIST IN", svg)
                self.assertIn("ILLUSTRATIVE TRACE", svg)
                self.assertIn('<g class="paper">', svg)
                for line in ("document received", "layout parsed", "fields extracted", "evaluation passed", "review required · 2 fields"):
                    self.assertIn(line, svg)
                self.assertIn(theme.live, svg)
                self.assertIn(theme.attention, svg)
                if animated:
                    self.assertIn("12s linear infinite", svg)
                    self.assertIn("prefers-reduced-motion:no-preference", svg)
                    self.assertIn("prefers-reduced-motion:no-preference", mobile_svg)
                    self.assertNotIn("animation:float", svg)
                    self.assertNotIn("animation:float", mobile_svg)
                else:
                    self.assertNotIn("@keyframes", svg)
                    self.assertNotIn("@keyframes", mobile_svg)

    def test_compact_artwork_dimensions_and_saved_variants(self):
        renderers = (
            ("telemetry", telemetry, (600, 52)),
            ("telemetry-mobile", telemetry_mobile, (360, 96)),
            ("contact-aurora", contact_aurora, (600, 88)),
            ("contact-aurora-mobile", contact_aurora_mobile, (360, 120)),
            ("workshop", lambda theme: workshop(theme, animated=True), (600, 160)),
            ("workshop-static", lambda theme: workshop(theme, animated=False), (600, 160)),
            ("workshop-mobile", lambda theme: workshop_mobile(theme, animated=True), (360, 240)),
            ("workshop-static-mobile", lambda theme: workshop_mobile(theme, animated=False), (360, 240)),
            *((repo, lambda theme, repo=repo: featured_row(theme, repo), (600, 160)) for repo in FEATURED),
            *((f"{repo}-mobile", lambda theme, repo=repo: featured_row_mobile(theme, repo), (360, 208)) for repo in FEATURED),
        )
        for theme in THEMES:
            for name, renderer, (width, height) in renderers:
                with self.subTest(theme=theme.name, asset=name):
                    svg = renderer(theme)
                    root = ET.fromstring(svg)
                    self.assertEqual(root.get("viewBox"), f"0 0 {width} {height}")
                    self.assertEqual(root.get("width"), str(width))
                    self.assertEqual(root.get("height"), str(height))
                    self.assertEqual(
                        svg,
                        (self.root / "assets" / "profile" / f"{name}.{theme.suffix}.svg").read_text(encoding="utf-8"),
                    )

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
            description_y = [int(text.get("y")) for text in texts if text.get("font-size") == "18"]
            self.assertTrue(all(b - a == 27 for a, b in zip(description_y, description_y[1:])))
            serialized = ET.tostring(root, encoding="unicode")
            self.assertIn("★ 12", serialized)
            self.assertIn("Updated 2026-09-20", serialized)
            self.assertIn('d="M10 1H410"', serialized)

    def test_curated_copy_is_scoped_to_profile_owner(self):
        info = RepoInfo("another-owner", "video-summarizer", "Another implementation.", 0, 0, "", "", "")
        svg = _render_svg(info, THEMES[0])
        self.assertIn("Another implementation.", svg)
        self.assertNotIn("04 / MULTIMODAL", svg)

        independent = _render_svg(info, THEMES[0], show_metrics=False)
        self.assertIn("OPEN REPOSITORY", independent)
        self.assertNotIn("VIEW CODE", independent)


if __name__ == "__main__":
    unittest.main()
