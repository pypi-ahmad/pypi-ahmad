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
    "email": ("EMAIL", "ahmad.iiitk@gmail.com", "direct", 136),
    "linkedin": ("LINKEDIN", "ahmad-mle", "direct", 136),
    "whatsapp": ("WHATSAPP", "pypi_ahmad", "direct", 136),
    "telegram": ("TELEGRAM", "dataintuitionist", "direct", 136),
    "portfolio": ("PORTFOLIO", "pypi-ahmad.github.io", "elsewhere", 136),
    "github": ("GITHUB", "pypi-ahmad", "elsewhere", 136),
    "twitter": ("X / TWITTER", "pypi_ahmad", "elsewhere", 136),
    "instagram": ("INSTAGRAM", "dataintuitionist", "elsewhere", 136),
    "facebook": ("FACEBOOK", "dataintuitionist", "elsewhere", 136),
}


def _defs(theme: Theme, rule: int = 32) -> str:
    return f'''<defs><linearGradient id="surface" x2="1" y2="1"><stop stop-color="{theme.bg}"/><stop offset="1" stop-color="{theme.bg2}"/></linearGradient><pattern id="rules" width="{rule}" height="{rule}" patternUnits="userSpaceOnUse"><path d="M0 {rule - .5}H{rule}" stroke="{theme.border}" opacity=".22"/></pattern></defs>'''


def section_header(theme: Theme, index: int, title: str, label: str) -> str:
    number = f"{index:02d} /"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="92" viewBox="0 0 960 92" role="img" aria-labelledby="title desc">
  <title id="title">{number} {_esc(title)}</title><desc id="desc">Numbered editorial section heading for {_esc(title)}.</desc>
  {_defs(theme)}
  <rect x=".75" y=".75" width="958.5" height="90.5" rx="8" fill="url(#surface)" stroke="{theme.border}" stroke-width="1.5"/>
  <path d="M24 16v60" stroke="{theme.accent}" stroke-width="3"/>
  <text x="42" y="55" fill="{theme.accent}" font-family="{MONO}" font-size="14" font-weight="700" letter-spacing="1.4">{number}</text>
  <text x="118" y="59" fill="{theme.title}" font-family="{DISPLAY}" font-size="29" font-weight="700">{_esc(title)}</text>
  <text x="928" y="52" text-anchor="end" fill="{theme.muted}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1.5">{label}</text>
  <path d="M118 72H928" stroke="{theme.border}"/><path d="M118 72h112" stroke="{theme.system}" stroke-width="1.5"/>
</svg>\n'''


def profile_hero(theme: Theme) -> str:
    title = "Ahmad Mujtaba"
    subtitle = "AI &amp; Data Science Engineer &#183; Deloitte US-India &#183; Gurugram, India"
    summary = "Production AI Engineer focused on multimodal document intelligence, LLM extraction architectures, agentic workflows, and LLM evaluation."
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="146" viewBox="0 0 600 146" role="img" aria-labelledby="title desc"><title id="title">{title}</title><desc id="desc">{subtitle} {summary}</desc>{_defs(theme)}<rect x=".75" y=".75" width="598.5" height="144.5" rx="8" fill="url(#surface)" stroke="{theme.border}" stroke-width="1.5"/><path d="M18 18v110" stroke="{theme.accent}" stroke-width="3"/><text x="36" y="45" fill="{theme.title}" font-family="{DISPLAY}" font-size="29" font-weight="700">{title}</text><path d="M36 59h528" stroke="{theme.border}"/><text x="36" y="82" fill="{theme.text}" font-family="{DISPLAY}" font-size="15">{subtitle}</text><text x="36" y="108" fill="{theme.text}" font-family="{DISPLAY}" font-size="14">Production AI Engineer focused on multimodal document intelligence, LLM extraction</text><text x="36" y="128" fill="{theme.text}" font-family="{DISPLAY}" font-size="14">architectures, agentic workflows, and LLM evaluation.</text></svg>\n'''


def profile_hero_mobile(theme: Theme) -> str:
    title = "Ahmad Mujtaba"
    subtitle = "AI &amp; Data Science Engineer &#183; Deloitte US-India &#183; Gurugram, India"
    summary = "Production AI Engineer focused on multimodal document intelligence, LLM extraction architectures, agentic workflows, and LLM evaluation."
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="360" height="188" viewBox="0 0 360 188" role="img" aria-labelledby="title desc"><title id="title">{title}</title><desc id="desc">{subtitle} {summary}</desc>{_defs(theme)}<rect x=".75" y=".75" width="358.5" height="186.5" rx="8" fill="url(#surface)" stroke="{theme.border}" stroke-width="1.5"/><path d="M18 18v152" stroke="{theme.accent}" stroke-width="3"/><text x="36" y="45" fill="{theme.title}" font-family="{DISPLAY}" font-size="28" font-weight="700">{title}</text><path d="M36 59h288" stroke="{theme.border}"/><text x="36" y="82" fill="{theme.text}" font-family="{DISPLAY}" font-size="14">{subtitle}</text><text x="36" y="110" fill="{theme.text}" font-family="{DISPLAY}" font-size="13">Production AI Engineer focused on multimodal</text><text x="36" y="130" fill="{theme.text}" font-family="{DISPLAY}" font-size="13">document intelligence, LLM extraction architectures,</text><text x="36" y="150" fill="{theme.text}" font-family="{DISPLAY}" font-size="13">agentic workflows, and LLM evaluation.</text></svg>\n'''


def contact_group_label(theme: Theme, label: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="360" height="32" viewBox="0 0 360 32" role="img" aria-labelledby="title desc"><title id="title">{_esc(label.title())}</title><desc id="desc">Contact directory group: {_esc(label.lower())}.</desc><path d="M12 24h336" stroke="{theme.border}"/><path d="M12 24h92" stroke="{theme.accent}" stroke-width="1.5"/><text x="12" y="16" fill="{theme.muted}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1.1">{_esc(label)}</text></svg>\n'''


def footer_signature(theme: Theme) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="260" height="36" viewBox="0 0 260 36" role="img" aria-labelledby="title desc"><title id="title">Made with love by Ahmad Mujtaba</title><desc id="desc">Profile footer signature.</desc><path d="M8 7v22" stroke="{theme.accent}" stroke-width="2"/><text x="22" y="23" fill="{theme.text}" font-family="{DISPLAY}" font-size="15">Made with</text><text x="101" y="23" fill="{theme.accent}" font-family="{DISPLAY}" font-size="15">&#9829;</text><text x="120" y="23" fill="{theme.text}" font-family="{DISPLAY}" font-size="15">by Ahmad Mujtaba</text></svg>\n'''


def _compact_panel(theme: Theme, width: int, height: int, title: str, description: str, body: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc"><title id="title">{_esc(title)}</title><desc id="desc">{_esc(description)}</desc>{_defs(theme)}<rect x=".75" y=".75" width="{width - 1.5}" height="{height - 1.5}" rx="8" fill="url(#surface)" stroke="{theme.border}" stroke-width="1.5"/><rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="8" fill="url(#rules)"/>{body}</svg>\n'''


def telemetry(theme: Theme) -> str:
    items = (("FOCUS", "multimodal AI"), ("LOCATION", "Gurugram"), ("STATUS", "available"), ("MODE", "production"))
    cells = []
    for i, (label, value) in enumerate(items):
        x = 16 + i * 150
        rule = f'<path d="M{x - 16} 10v32" stroke="{theme.border}"/>' if i else ""
        dot = f'<circle cx="{x}" cy="33" r="3" fill="{theme.live}"/>' if label == "STATUS" else ""
        value_x = x + 11 if label == "STATUS" else x
        cells.append(f'{rule}<text x="{x}" y="17" fill="{theme.muted}" font-family="{MONO}" font-size="9" font-weight="700" letter-spacing="1">{label}</text>{dot}<text x="{value_x}" y="37" fill="{theme.title}" font-family="{MONO}" font-size="16" font-weight="600">{value}</text>')
    return _compact_panel(theme, 600, 52, "Profile telemetry", "Focus: multimodal AI. Location: Gurugram. Status: available. Mode: production.", f'<path d="M8 1H592" stroke="{theme.accent}" stroke-width="2" stroke-linecap="round"/>' + "".join(cells))

def telemetry_mobile(theme: Theme) -> str:
    items = (("FOCUS", "multimodal AI"), ("LOCATION", "Gurugram"), ("STATUS", "available"), ("MODE", "production"))
    cells = []
    for i, (label, value) in enumerate(items):
        x, y = 18 + (i % 2) * 172, (i // 2) * 46
        dot = f'<circle cx="{x}" cy="{y + 34}" r="3" fill="{theme.live}"/>' if label == "STATUS" else ""
        value_x = x + 11 if label == "STATUS" else x
        cells.append(f'<text x="{x}" y="{y + 19}" fill="{theme.muted}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1">{label}</text>{dot}<text x="{value_x}" y="{y + 38}" fill="{theme.title}" font-family="{MONO}" font-size="14" font-weight="600">{value}</text>')
    return _compact_panel(theme, 360, 96, "Profile telemetry", "Focus: multimodal AI. Location: Gurugram. Status: available. Mode: production.", f'<path d="M8 1H352" stroke="{theme.accent}" stroke-width="2" stroke-linecap="round"/><path d="M180 10v76M14 48h332" stroke="{theme.border}"/>' + "".join(cells))

def cta(theme: Theme, kind: str) -> str:
    title, label, action = {"portfolio": ("Open Ahmad Mujtaba's portfolio", "PORTFOLIO", "Open site"), "email": ("Email Ahmad Mujtaba", "EMAIL", "Email me"), "linkedin": ("Connect on LinkedIn", "LINKEDIN", "Connect")}[kind]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="136" height="56" viewBox="0 0 136 56" role="img" aria-labelledby="title desc"><title id="title">{title}</title><desc id="desc">Editorial {kind} action.</desc><rect x=".5" y=".5" width="135" height="55" rx="7.5" fill="{theme.bg2}" stroke="{theme.border}"/><path d="M8 1H128" stroke="{theme.accent}" stroke-width="2" stroke-linecap="round"/><path d="M18 14v28" stroke="{theme.accent}" stroke-width="2"/><text x="30" y="22" fill="{theme.muted}" font-family="{MONO}" font-size="9" font-weight="700" letter-spacing=".65">{label}</text><text x="30" y="41" fill="{theme.title}" font-family="{DISPLAY}" font-size="12" font-weight="700">{action}</text><path d="M120 28h8m-3-3 3 3-3 3" fill="none" stroke="{theme.accent}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>\n'''


def featured_row(theme: Theme, repo: str) -> str:
    title, category, description, _, flow = FEATURED[repo]
    lines = _wrap(description, 62, 2)
    body = "".join(f'<text x="22" y="{77 + i * 20}" fill="{theme.text}" font-family="{DISPLAY}" font-size="16">{_esc(line)}</text>' for i, line in enumerate(lines))
    flow_svg = f'<tspan fill="{theme.accent}"> → </tspan>'.join(f'<tspan>{_esc(node)}</tspan>' for node in flow)
    content = f'''<path d="M12 14v86" stroke="{theme.accent}" stroke-width="3"/><text x="22" y="24" fill="{theme.muted}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1">{_esc(category)}</text><text x="578" y="24" text-anchor="end" fill="{theme.accent}" font-family="{MONO}" font-size="11" font-weight="700">OPEN REPOSITORY ↗</text><text x="22" y="51" fill="{theme.title}" font-family="{DISPLAY}" font-size="22" font-weight="700">{_esc(title)}</text>{body}<path d="M20 110h560" stroke="{theme.border}"/><text x="22" y="128" fill="{theme.muted}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1">ARCHITECTURE FLOW</text><text x="22" y="147" fill="{theme.text}" font-family="{MONO}" font-size="13">{flow_svg}</text>'''
    return _compact_panel(theme, 600, 160, title, f"{description} Flow: {' to '.join(flow)}.", content)

def featured_row_mobile(theme: Theme, repo: str) -> str:
    title, category, description, _, flow = FEATURED[repo]
    lines = _wrap(description, 43, 3)
    body = "".join(f'<text x="22" y="{78 + i * 19}" fill="{theme.text}" font-family="{DISPLAY}" font-size="14">{_esc(line)}</text>' for i, line in enumerate(lines))
    flow_svg = f'<tspan fill="{theme.accent}"> → </tspan>'.join(f'<tspan>{_esc(node)}</tspan>' for node in flow)
    content = f'''<path d="M12 14v132" stroke="{theme.accent}" stroke-width="3"/><text x="22" y="26" fill="{theme.muted}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1">{_esc(category)}</text><text x="22" y="52" fill="{theme.title}" font-family="{DISPLAY}" font-size="22" font-weight="700">{_esc(title)}</text>{body}<text x="22" y="140" fill="{theme.accent}" font-family="{MONO}" font-size="11" font-weight="700">OPEN REPOSITORY ↗</text><path d="M20 154h320" stroke="{theme.border}"/><text x="22" y="172" fill="{theme.muted}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1">ARCHITECTURE FLOW</text><text x="22" y="192" fill="{theme.text}" font-family="{MONO}" font-size="11">{flow_svg}</text>'''
    return _compact_panel(theme, 360, 208, title, f"{description} Flow: {' to '.join(flow)}.", content)

def contact_cell(theme: Theme, key: str) -> str:
    label, value, _, width = CONTACTS[key]
    size = 12
    value_lines = {"email": ("ahmad.iiitk", "@gmail.com"), "portfolio": ("pypi-ahmad", ".github.io")}.get(key, (value,))
    value_svg = "".join(f'<text x="14" y="{49 + i * 14}" fill="{theme.title}" font-family="{DISPLAY}" font-size="{size}" font-weight="600">{_esc(line)}</text>' for i, line in enumerate(value_lines))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="72" viewBox="0 0 {width} 72" role="img" aria-labelledby="title desc"><title id="title">{_esc(label.title())}: {_esc(value)}</title><desc id="desc">Open Ahmad Mujtaba's {_esc(label.lower())} contact.</desc><rect x=".75" y=".75" width="{width - 1.5}" height="70.5" rx="5" fill="{theme.bg2}" stroke="{theme.border}" stroke-width="1.5"/><path d="M6 1H{width - 6}" stroke="{theme.accent}" stroke-width="2" stroke-linecap="round"/><text x="14" y="25" fill="{theme.muted}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing=".9">{label}</text>{value_svg}<path d="M{width - 25} 22h9m-4-4 4 4-4 4" fill="none" stroke="{theme.accent}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>\n'''


def contact_aurora(theme: Theme) -> str:
    body = f'''<path d="M12 12v64" stroke="{theme.accent}" stroke-width="3"/><text x="22" y="22" fill="{theme.muted}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1">OPEN TO COLLABORATION</text><text x="22" y="49" fill="{theme.title}" font-family="{DISPLAY}" font-size="24" font-weight="700">Let’s work together</text><circle cx="25" cy="68" r="3" fill="{theme.live}"/><text x="36" y="72" fill="{theme.muted}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1">AVAILABLE</text><path d="M296 14v60" stroke="{theme.border}"/><text x="314" y="36" fill="{theme.text}" font-family="{DISPLAY}" font-size="14">Production AI · Document Intelligence</text><text x="314" y="57" fill="{theme.text}" font-family="{DISPLAY}" font-size="14">Agentic Systems · Evaluation</text>'''
    return _compact_panel(theme, 600, 88, "Let’s work together", "An invitation to collaborate in production AI.", body)

def contact_aurora_mobile(theme: Theme) -> str:
    body = f'''<path d="M12 12v96" stroke="{theme.accent}" stroke-width="3"/><text x="24" y="22" fill="{theme.muted}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1">OPEN TO COLLABORATION</text><text x="24" y="47" fill="{theme.title}" font-family="{DISPLAY}" font-size="24" font-weight="700">Let’s work together</text><text x="24" y="71" fill="{theme.text}" font-family="{DISPLAY}" font-size="14">Production AI · Document Intelligence</text><text x="24" y="91" fill="{theme.text}" font-family="{DISPLAY}" font-size="14">Agentic Systems · Evaluation</text><circle cx="27" cy="108" r="3" fill="{theme.live}"/><text x="38" y="112" fill="{theme.muted}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1">AVAILABLE</text>'''
    return _compact_panel(theme, 360, 120, "Let’s work together", "An invitation to collaborate in production AI.", body)

def _workshop_diagram(theme: Theme) -> str:
    return f'''<g transform="translate(20 42)"><g class="paper"><rect x="18" y="7" width="42" height="64" rx="4" fill="{theme.bg2}" stroke="{theme.border}" transform="rotate(7 39 39)"/><rect x="12" y="4" width="42" height="64" rx="4" fill="{theme.bg2}" stroke="{theme.system}"/><path d="M21 20h22m-22 10h26m-26 10h26m-26 10h16" stroke="{theme.muted}" stroke-width="1.5"/><path d="M21 59h24" stroke="{theme.accent}" stroke-width="2"/></g><path d="M68 36h82" fill="none" stroke="{theme.system}" stroke-width="1.5"/><path class="flow" d="M68 36h82" fill="none" stroke="{theme.accent}" stroke-width="2" stroke-dasharray="12 100"/><circle cx="110" cy="36" r="4" fill="{theme.bg2}" stroke="{theme.accent}" stroke-width="1.5"/><g transform="translate(150 0)"><rect width="132" height="70" rx="8" fill="{theme.bg2}" stroke="{theme.accent}" stroke-width="1.5"/><path d="M43 27l12-12 12 12-12 12zM61 27l12-12 12 12-12 12z" fill="none" stroke="{theme.accent}" stroke-width="2"/><circle cx="114" cy="14" r="3" fill="{theme.live}"/><text x="66" y="57" text-anchor="middle" fill="{theme.title}" font-family="{MONO}" font-size="11" letter-spacing="1">BUILD / EVAL</text></g></g>'''


def _workshop_trace(theme: Theme, x: int, y: int, width: int, font_size: int) -> str:
    trace = (("01", "document received", theme.text), ("02", "layout parsed", theme.text), ("03", "fields extracted", theme.text), ("04", "evaluation passed", theme.live), ("05", "review required · 2 fields", theme.attention))
    lines = "".join(f'<text x="14" y="{39 + i * 15}" font-family="{MONO}" font-size="{font_size}"><tspan fill="{theme.muted}">{number}</tspan><tspan x="44" fill="{color}">{text}</tspan></text>' for i, (number, text, color) in enumerate(trace))
    return f'''<g transform="translate({x} {y})"><rect width="{width}" height="108" rx="5" fill="{theme.bg2}" stroke="{theme.border}"/><circle cx="14" cy="14" r="3" fill="{theme.live}"/><text x="25" y="18" fill="{theme.muted}" font-family="{MONO}" font-size="10" letter-spacing=".8">ILLUSTRATIVE TRACE</text><path d="M0 25h{width}" stroke="{theme.border}"/>{lines}</g>'''


def workshop(theme: Theme, *, animated: bool) -> str:
    animation = "@media (prefers-reduced-motion:no-preference){.flow{animation:flow 12s linear infinite}}@keyframes flow{to{stroke-dashoffset:-672}}" if animated else ""
    body = f'''<style>{animation}</style><path d="M12 12v14" stroke="{theme.accent}" stroke-width="3"/><text x="22" y="22" fill="{theme.title}" font-family="{MONO}" font-size="10" font-weight="700">DATAINTUITIONIST IN</text><text x="578" y="22" text-anchor="end" fill="{theme.muted}" font-family="{MONO}" font-size="9" letter-spacing="1">THE AI WORKSHOP</text><path d="M20 32h560" stroke="{theme.border}"/>{_workshop_diagram(theme)}{_workshop_trace(theme, 330, 42, 250, 11)}'''
    return _compact_panel(theme, 600, 160, "Ahmad's AI workshop", "An AI system workshop with document input, model evaluation, and an illustrative review trace.", body)

def workshop_mobile(theme: Theme, *, animated: bool) -> str:
    animation = "@media (prefers-reduced-motion:no-preference){.flow{animation:flow 12s linear infinite}}@keyframes flow{to{stroke-dashoffset:-672}}" if animated else ""
    body = f'''<style>{animation}</style><path d="M12 12v14" stroke="{theme.accent}" stroke-width="3"/><text x="22" y="22" fill="{theme.title}" font-family="{MONO}" font-size="10" font-weight="700">DATAINTUITIONIST IN</text><text x="338" y="22" text-anchor="end" fill="{theme.muted}" font-family="{MONO}" font-size="9" letter-spacing="1">AI WORKSHOP</text><path d="M20 32h320" stroke="{theme.border}"/>{_workshop_diagram(theme)}{_workshop_trace(theme, 20, 120, 320, 14)}'''
    return _compact_panel(theme, 360, 240, "Ahmad's AI workshop", "An AI system workshop with document input, model evaluation, and an illustrative review trace.", body)

def main() -> None:
    output = Path(__file__).resolve().parents[1] / "assets" / "profile"
    output.mkdir(parents=True, exist_ok=True)
    written = 0
    for theme in THEMES:
        (output / f"profile-hero.{theme.suffix}.svg").write_text(profile_hero(theme), encoding="utf-8"); written += 1
        (output / f"profile-hero-mobile.{theme.suffix}.svg").write_text(profile_hero_mobile(theme), encoding="utf-8"); written += 1
        for animated in (True, False):
            name = "workshop" if animated else "workshop-static"
            (output / f"{name}.{theme.suffix}.svg").write_text(workshop(theme, animated=animated), encoding="utf-8"); written += 1
            (output / f"{name}-mobile.{theme.suffix}.svg").write_text(workshop_mobile(theme, animated=animated), encoding="utf-8"); written += 1
        (output / f"telemetry.{theme.suffix}.svg").write_text(telemetry(theme), encoding="utf-8"); written += 1
        (output / f"telemetry-mobile.{theme.suffix}.svg").write_text(telemetry_mobile(theme), encoding="utf-8"); written += 1
        for kind in ("portfolio", "email", "linkedin"):
            (output / f"cta-{kind}.{theme.suffix}.svg").write_text(cta(theme, kind), encoding="utf-8"); written += 1
        for repo in FEATURED:
            (output / f"{repo}.{theme.suffix}.svg").write_text(featured_row(theme, repo), encoding="utf-8"); written += 1
            (output / f"{repo}-mobile.{theme.suffix}.svg").write_text(featured_row_mobile(theme, repo), encoding="utf-8"); written += 1
        for index, (name, (title, label)) in enumerate(SECTIONS.items(), 1):
            (output / f"section-{name}.{theme.suffix}.svg").write_text(section_header(theme, index, title, label), encoding="utf-8"); written += 1
        for key in CONTACTS:
            (output / f"contact-{key}.{theme.suffix}.svg").write_text(contact_cell(theme, key), encoding="utf-8"); written += 1
        for label, name in (("DIRECT CHANNELS", "direct-channels"), ("ELSEWHERE", "elsewhere")):
            (output / f"contact-{name}.{theme.suffix}.svg").write_text(contact_group_label(theme, label), encoding="utf-8"); written += 1
        (output / f"contact-aurora.{theme.suffix}.svg").write_text(contact_aurora(theme), encoding="utf-8"); written += 1
        (output / f"contact-aurora-mobile.{theme.suffix}.svg").write_text(contact_aurora_mobile(theme), encoding="utf-8"); written += 1
        (output / f"footer-signature.{theme.suffix}.svg").write_text(footer_signature(theme), encoding="utf-8"); written += 1
    print(f"Generated {written} profile assets in {output}")


if __name__ == "__main__":
    main()
