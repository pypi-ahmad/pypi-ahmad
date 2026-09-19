"""Build deterministic, network-free artwork for the profile README."""

from pathlib import Path

from generate_repo_cards import FEATURED, THEMES, Theme, _esc, _wrap

MONO = "Cascadia Code,Cascadia Mono,Consolas,monospace"
DISPLAY = "Segoe UI,Arial,sans-serif"

SECTIONS = {
    "featured-projects": ("Featured projects", "SELECTED WORK"),
    "case-studies": ("Case studies", "ENGINEERING DECISIONS"),
    "public-projects": ("Public projects", "OPEN SOURCE"),
    "about": ("About", "BACKGROUND"),
    "measured-outcomes": ("Measured outcomes", "EVIDENCE"),
    "professional-experience": ("Professional experience", "EXPERIENCE"),
    "skills": ("Skills, with context", "TOOLKIT"),
    "fde": ("Forward-deployed AI engineering", "LEARNING PATH"),
    "education": ("Education & credentials", "CREDENTIALS"),
    "activity": ("Activity", "CONTRIBUTIONS"),
    "github-statistics": ("GitHub statistics", "LIVE SNAPSHOT"),
    "repository-showcase": ("Repository showcase", "MORE WORK"),
    "repository": ("Repository", "GOVERNANCE"),
    "contact": ("Contact & availability", "AVAILABLE"),
}

CONTACTS = {
    "email": ("EMAIL", "ahmad.iiitk@gmail.com", "direct", 226),
    "linkedin": ("LINKEDIN", "ahmad-mle", "direct", 226),
    "whatsapp": ("WHATSAPP", "pypi_ahmad", "direct", 226),
    "telegram": ("TELEGRAM", "dataintuitionist", "direct", 226),
    "portfolio": ("PORTFOLIO", "pypi-ahmad.github.io", "elsewhere", 180),
    "github": ("GITHUB", "pypi-ahmad", "elsewhere", 180),
    "twitter": ("X / TWITTER", "pypi_ahmad", "elsewhere", 180),
    "instagram": ("INSTAGRAM", "dataintuitionist", "elsewhere", 180),
    "facebook": ("FACEBOOK", "dataintuitionist", "elsewhere", 180),
}


def _defs(theme: Theme, grid: int = 24) -> str:
    return f'''<defs><linearGradient id="surface" x2="1" y2="1"><stop stop-color="{theme.bg}"/><stop offset="1" stop-color="{theme.bg2}"/></linearGradient><pattern id="grid" width="{grid}" height="{grid}" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{theme.muted}" opacity=".13"/></pattern></defs>'''


def section_header(theme: Theme, index: int, title: str, label: str) -> str:
    number = f"{index:02d} /"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="92" viewBox="0 0 960 92" role="img" aria-labelledby="title desc">
  <title id="title">{number} {_esc(title)}</title><desc id="desc">Numbered section heading for {_esc(title)}.</desc>{_defs(theme)}
  <rect x=".75" y=".75" width="958.5" height="90.5" rx="14" fill="url(#surface)" stroke="{theme.border}" stroke-width="1.5"/><rect x="10" y="10" width="940" height="72" rx="10" fill="url(#grid)"/>
  <path d="M20 25V16h9M940 67v9h-9" fill="none" stroke="{theme.system}" stroke-width="1.5"/>
  <text x="30" y="56" fill="{theme.system}" font-family="{MONO}" font-size="16" font-weight="700" letter-spacing="1.4">{number}</text>
  <text x="112" y="59" fill="{theme.title}" font-family="{DISPLAY}" font-size="30" font-weight="700">{_esc(title)}</text>
  <text x="928" y="54" text-anchor="end" fill="{theme.muted}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1.5">{label}</text>
  <path d="M112 70H928" stroke="{theme.border}"/><path d="M112 70h96" stroke="{theme.accent}" stroke-width="2"/>
</svg>\n'''


def telemetry(theme: Theme) -> str:
    items = (("FOCUS", "multimodal AI"), ("LOCATION", "Gurugram"), ("STATUS", "available"), ("MODE", "production"))
    cells = []
    for i, (label, value) in enumerate(items):
        x = 24 + i * 240
        rule = f'<path d="M{x - 12} 16v40" stroke="{theme.border}"/>' if i else ""
        dot = f'<circle cx="{x}" cy="43" r="4" fill="{theme.live}"/>' if label == "STATUS" else ""
        value_x = x + 13 if label == "STATUS" else x
        cells.append(f'{rule}<text x="{x}" y="25" fill="{theme.muted}" font-family="{MONO}" font-size="9" font-weight="700" letter-spacing="1.2">{label}</text>{dot}<text x="{value_x}" y="47" fill="{theme.title}" font-family="{MONO}" font-size="13" font-weight="600">{value}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="68" viewBox="0 0 960 68" role="img" aria-labelledby="title desc"><title id="title">Profile telemetry</title><desc id="desc">Focus: multimodal AI. Location: Gurugram. Status: available. Mode: production.</desc>{_defs(theme, 20)}<rect x=".75" y=".75" width="958.5" height="66.5" rx="13" fill="url(#surface)" stroke="{theme.border}" stroke-width="1.5"/><rect x="8" y="8" width="944" height="52" rx="9" fill="url(#grid)"/>{''.join(cells)}</svg>\n'''


def _brand_icon(kind: str) -> str:
    if kind == "portfolio":
        return '''<g transform="translate(16 12)"><path d="M16 0a16 16 0 0 1 13.86 8H16a8 8 0 0 0-6.93 4L4.45 4A15.94 15.94 0 0 1 16 0z" fill="#EA4335"/><path d="M29.86 8A16 16 0 0 1 16 32l6.93-12A8 8 0 0 0 24 16c0-1.46-.39-2.83-1.07-4z" fill="#FBBC04"/><path d="M16 32A16 16 0 0 1 4.45 4l6.93 12A8 8 0 0 0 16 24c2.96 0 5.55-1.61 6.93-4z" fill="#34A853"/><circle cx="16" cy="16" r="6.8" fill="#4285F4" stroke="#FFF" stroke-width="2.4"/></g>'''
    if kind == "email":
        return '''<svg x="16" y="12" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><path d="M3 19V6" stroke="#4285F4"/><path d="M21 6v13" stroke="#34A853"/><path d="m3 6 9 7 9-7" stroke="#EA4335"/><path d="m3 6 3 2.33" stroke="#FBBC04"/><path d="m18 8.33 3-2.33" stroke="#C5221F"/></svg>'''
    return '''<svg x="16" y="12" width="32" height="32" viewBox="0 0 448 512"><path fill="#0A66C2" d="M416 32H31.9C14.3 32 0 46.5 0 64.3v383.4C0 465.5 14.3 480 31.9 480H416c17.6 0 32-14.5 32-32.3V64.3C448 46.5 433.6 32 416 32zM135.4 416H69V202.2h66.5V416zm-33.2-243c-21.3 0-38.5-17.3-38.5-38.5S80.9 96 102.2 96c21.2 0 38.5 17.3 38.5 38.5 0 21.3-17.2 38.5-38.5 38.5zm282.1 243h-66.4V312c0-24.8-.5-56.7-34.5-56.7-34.6 0-39.9 27-39.9 54.9V416h-66.4V202.2h63.7v29.2h.9c8.9-16.8 30.6-34.5 62.9-34.5 67.2 0 79.7 44.3 79.7 101.9V416z"/></svg>'''


def cta(theme: Theme, kind: str) -> str:
    title, eyebrow, action = {"portfolio": ("View portfolio", "EXPLORE", "View portfolio"), "email": ("Email Ahmad Mujtaba", "START A CONVERSATION", "Email me"), "linkedin": ("Connect on LinkedIn", "PROFESSIONAL NETWORK", "Connect on LinkedIn")}[kind]
    fit = ' textLength="120" lengthAdjust="spacingAndGlyphs"' if kind == "linkedin" else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="240" height="56" viewBox="0 0 240 56" role="img" aria-labelledby="title desc"><title id="title">{title}</title><desc id="desc">Terminal-style {kind} action.</desc><rect x=".5" y=".5" width="239" height="55" rx="13.5" fill="{theme.bg2}" stroke="{theme.border}"/>{_brand_icon(kind)}<path d="M68 13v30" stroke="{theme.accent}" stroke-width="2"/><text x="84" y="24" fill="{theme.system}" font-family="{MONO}" font-size="8.5" font-weight="700" letter-spacing="1.1">{eyebrow}</text><text x="84" y="41" fill="{theme.title}" font-family="{MONO}" font-size="14" font-weight="700"{fit}>{action}</text><path d="M217 28h10m-4-4 4 4-4 4" fill="none" stroke="{theme.accent}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>\n'''


def featured_row(theme: Theme, repo: str) -> str:
    title, category, description, _, flow = FEATURED[repo]
    lines = _wrap(description, 48, 2)
    body = "".join(f'<text x="238" y="{100 + i * 23}" fill="{theme.text}" font-family="{DISPLAY}" font-size="16">{_esc(line)}</text>' for i, line in enumerate(lines))
    nodes = []
    for i, name in enumerate(flow):
        x, y = 690 + (i % 2) * 130, 50 + (i // 2) * 66
        nodes.append(f'<rect x="{x}" y="{y}" width="108" height="34" rx="6" fill="{theme.bg}" stroke="{theme.border}"/><text x="{x + 54}" y="{y + 22}" text-anchor="middle" fill="{theme.text}" font-family="{MONO}" font-size="10">{_esc(name)}</text>')
    edges = f'<path d="M798 67h22M744 84v32M798 133h22" fill="none" stroke="{theme.system}"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="180" viewBox="0 0 960 180" role="img" aria-labelledby="title desc"><title id="title">{_esc(title)}</title><desc id="desc">{_esc(description)} Flow: {_esc(' to '.join(flow))}.</desc>{_defs(theme)}<rect x=".75" y=".75" width="958.5" height="178.5" rx="16" fill="url(#surface)" stroke="{theme.border}" stroke-width="1.5"/><rect x="10" y="10" width="940" height="160" rx="12" fill="url(#grid)"/><path d="M210 24v132M660 24v132" stroke="{theme.border}"/><text x="28" y="49" fill="{theme.system}" font-family="{MONO}" font-size="11" font-weight="700" letter-spacing="1.4">{_esc(category)}</text><text x="28" y="82" fill="{theme.title}" font-family="{DISPLAY}" font-size="24" font-weight="700">{_esc(title)}</text><text x="28" y="144" fill="{theme.accent}" font-family="{MONO}" font-size="11" font-weight="700">VIEW CODE ↗</text><text x="238" y="55" fill="{theme.muted}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1.3">PROJECT / SYSTEM</text>{body}<text x="690" y="31" fill="{theme.muted}" font-family="{MONO}" font-size="9" font-weight="700" letter-spacing="1.2">ARCHITECTURE FLOW</text>{edges}{''.join(nodes)}<path d="M20 24V16h8M940 156v8h-8" fill="none" stroke="{theme.system}" stroke-width="1.5"/></svg>\n'''


def contact_cell(theme: Theme, key: str) -> str:
    label, value, _, width = CONTACTS[key]
    size = 12 if len(value) > 19 else 14
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="72" viewBox="0 0 {width} 72" role="img" aria-labelledby="title desc"><title id="title">{_esc(label.title())}: {_esc(value)}</title><desc id="desc">Open Ahmad Mujtaba's {_esc(label.lower())} contact.</desc><rect x=".75" y=".75" width="{width - 1.5}" height="70.5" rx="12" fill="{theme.bg2}" stroke="{theme.border}" stroke-width="1.5"/><path d="M16 18h24" stroke="{theme.system}" stroke-width="2"/><text x="16" y="31" fill="{theme.muted}" font-family="{MONO}" font-size="9" font-weight="700" letter-spacing="1.2">{label}</text><text x="16" y="53" fill="{theme.title}" font-family="{MONO}" font-size="{size}" font-weight="600">{_esc(value)}</text><path d="M{width - 29} 25h10m-4-4 4 4-4 4" fill="none" stroke="{theme.accent}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>\n'''


def contact_aurora(theme: Theme) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="160" viewBox="0 0 960 160" role="img" aria-labelledby="title desc"><title id="title">Let’s work together</title><desc id="desc">An invitation to collaborate in production AI.</desc><defs><linearGradient id="surface" x2="1"><stop stop-color="{theme.bg}"/><stop offset="1" stop-color="{theme.bg2}"/></linearGradient><radialGradient id="amber"><stop stop-color="{theme.accent}" stop-opacity=".18"/><stop offset="1" stop-color="{theme.accent}" stop-opacity="0"/></radialGradient><radialGradient id="cyan"><stop stop-color="{theme.system}" stop-opacity=".16"/><stop offset="1" stop-color="{theme.system}" stop-opacity="0"/></radialGradient><pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="{theme.muted}" opacity=".13"/></pattern></defs><rect x=".75" y=".75" width="958.5" height="158.5" rx="18" fill="url(#surface)" stroke="{theme.border}" stroke-width="1.5"/><rect x="12" y="12" width="936" height="136" rx="13" fill="url(#grid)"/><ellipse cx="355" cy="86" rx="270" ry="110" fill="url(#amber)"/><ellipse cx="650" cy="95" rx="260" ry="105" fill="url(#cyan)"/><path d="M28 31V20h11M932 129v11h-11" fill="none" stroke="{theme.system}" stroke-width="1.5"/><text x="480" y="52" text-anchor="middle" fill="{theme.system}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="2.2">OPEN TO COLLABORATION</text><text x="480" y="91" text-anchor="middle" fill="{theme.title}" font-family="{DISPLAY}" font-size="30" font-weight="700">Let’s work together</text><text x="480" y="121" text-anchor="middle" fill="{theme.text}" font-family="{MONO}" font-size="12">Production AI · Document Intelligence · Agentic Systems</text><circle cx="394" cy="139" r="4" fill="{theme.live}"/><text x="406" y="143" fill="{theme.muted}" font-family="{MONO}" font-size="10">AVAILABLE</text></svg>\n'''


def workshop(theme: Theme, *, animated: bool) -> str:
    animation = ".flow{animation:flow 12s linear infinite}.paper{animation:float 12s ease-in-out infinite}@keyframes flow{to{stroke-dashoffset:-800}}@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}@media (prefers-reduced-motion:reduce){.flow,.paper{animation:none}}" if animated else ""
    trace = (("01", "document received", theme.text), ("02", "layout parsed", theme.text), ("03", "fields extracted", theme.text), ("04", "evaluation passed", theme.live), ("05", "review required · 2 fields", theme.accent))
    trace_svg = "".join(f'<text x="24" y="{56 + i * 22}" font-family="{MONO}" font-size="10"><tspan fill="{theme.muted}">{n}</tspan><tspan x="50" fill="{color}">{text}</tspan></text>' for i, (n, text, color) in enumerate(trace))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="260" viewBox="0 0 960 260" role="img" aria-labelledby="title description"><title id="title">Ahmad's AI workshop</title><desc id="description">An AI system workshop with document input, model evaluation, and an illustrative review trace.</desc><defs><linearGradient id="surface" x2="1" y2="1"><stop stop-color="{theme.bg}"/><stop offset="1" stop-color="{theme.bg2}"/></linearGradient><linearGradient id="line"><stop stop-color="{theme.system}"/><stop offset="1" stop-color="{theme.accent}"/></linearGradient><pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{theme.muted}" opacity=".16"/></pattern><style>{animation}</style></defs><rect x="1" y="1" width="958" height="258" rx="24" fill="url(#surface)" stroke="{theme.border}"/><rect x="14" y="14" width="932" height="232" rx="16" fill="url(#grid)"/><path d="M30 34V22h12M930 226v12h-12" fill="none" stroke="{theme.system}" stroke-width="1.5"/><text x="32" y="45" fill="{theme.system}" font-family="{MONO}" font-size="11" font-weight="700">DATAINTUITIONIST IN</text><text x="928" y="45" text-anchor="end" fill="{theme.muted}" font-family="{MONO}" font-size="10" letter-spacing="1.6">THE AI WORKSHOP</text><g fill="none" stroke="{theme.border}" stroke-width="2"><path d="M190 139h168"/><path d="M510 139h170"/></g><g class="flow" fill="none" stroke="url(#line)" stroke-width="3" stroke-dasharray="12 220"><path d="M190 139h168"/><path d="M510 139h170"/></g><g class="paper" transform="translate(72 78)"><rect x="12" y="2" width="92" height="126" rx="9" fill="{theme.bg2}" stroke="{theme.border}" transform="rotate(8 58 65)"/><rect width="92" height="128" rx="9" fill="{theme.bg}" stroke="{theme.system}" stroke-width="1.5" transform="rotate(-5 46 64)"/><path d="M18 30h42m-42 14h55m-55 14h55m-55 14h34" stroke="{theme.muted}" stroke-width="2"/><path d="M20 98h50" stroke="{theme.system}" stroke-width="3"/></g><g transform="translate(358 73)"><rect x="-12" y="-12" width="176" height="156" rx="30" fill="{theme.system}" opacity=".05"/><rect width="152" height="132" rx="24" fill="{theme.bg}" stroke="{theme.accent}" stroke-width="2"/><path d="M45 65l18-18 18 18-18 18zM69 65l18-18 18 18-18 18z" fill="none" stroke="{theme.accent}" stroke-width="3"/><circle cx="126" cy="23" r="4" fill="{theme.system}"/><text x="76" y="112" text-anchor="middle" fill="{theme.title}" font-family="{MONO}" font-size="11" letter-spacing="1.6">BUILD / EVAL</text></g><g transform="translate(694 62)"><rect width="224" height="166" rx="12" fill="{theme.bg}" stroke="{theme.border}" stroke-width="1.5"/><path d="M0 32h224" stroke="{theme.border}"/><circle cx="16" cy="16" r="3" fill="{theme.live}"/><text x="29" y="20" fill="{theme.muted}" font-family="{MONO}" font-size="9" letter-spacing="1.1">ILLUSTRATIVE TRACE</text>{trace_svg}</g><g fill="{theme.bg}" stroke="{theme.system}" stroke-width="2"><circle cx="260" cy="139" r="7"/><circle cx="604" cy="139" r="7"/></g></svg>\n'''


def main() -> None:
    output = Path(__file__).resolve().parents[1] / "assets" / "profile"
    output.mkdir(parents=True, exist_ok=True)
    written = 0
    for theme in THEMES:
        for animated in (True, False):
            name = "workshop" if animated else "workshop-static"
            (output / f"{name}.{theme.suffix}.svg").write_text(workshop(theme, animated=animated), encoding="utf-8"); written += 1
        (output / f"telemetry.{theme.suffix}.svg").write_text(telemetry(theme), encoding="utf-8"); written += 1
        for kind in ("portfolio", "email", "linkedin"):
            (output / f"cta-{kind}.{theme.suffix}.svg").write_text(cta(theme, kind), encoding="utf-8"); written += 1
        for repo in FEATURED:
            (output / f"{repo}.{theme.suffix}.svg").write_text(featured_row(theme, repo), encoding="utf-8"); written += 1
        for index, (name, (title, label)) in enumerate(SECTIONS.items(), 1):
            (output / f"section-{name}.{theme.suffix}.svg").write_text(section_header(theme, index, title, label), encoding="utf-8"); written += 1
        for key in CONTACTS:
            (output / f"contact-{key}.{theme.suffix}.svg").write_text(contact_cell(theme, key), encoding="utf-8"); written += 1
        (output / f"contact-aurora.{theme.suffix}.svg").write_text(contact_aurora(theme), encoding="utf-8"); written += 1
    print(f"Generated {written} profile assets in {output}")


if __name__ == "__main__":
    main()
