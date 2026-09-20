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


def telemetry(theme: Theme) -> str:
    items = (("FOCUS", "multimodal AI"), ("LOCATION", "Gurugram"), ("STATUS", "available"), ("MODE", "production"))
    cells = []
    for i, (label, value) in enumerate(items):
        x = 24 + i * 240
        rule = f'<path d="M{x - 12} 16v40" stroke="{theme.border}"/>' if i else ""
        dot = f'<circle cx="{x}" cy="43" r="4" fill="{theme.live}"/>' if label == "STATUS" else ""
        value_x = x + 13 if label == "STATUS" else x
        cells.append(f'{rule}<text x="{x}" y="25" fill="{theme.muted}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1.1">{label}</text>{dot}<text x="{value_x}" y="47" fill="{theme.title}" font-family="{MONO}" font-size="13" font-weight="600">{value}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="68" viewBox="0 0 960 68" role="img" aria-labelledby="title desc"><title id="title">Profile telemetry</title><desc id="desc">Focus: multimodal AI. Location: Gurugram. Status: available. Mode: production.</desc>{_defs(theme)}<rect x=".75" y=".75" width="958.5" height="66.5" rx="7" fill="url(#surface)" stroke="{theme.border}" stroke-width="1.5"/><path d="M8 1H952" stroke="{theme.accent}" stroke-width="2" stroke-linecap="round"/>{''.join(cells)}</svg>\n'''


def telemetry_mobile(theme: Theme) -> str:
    items = (("FOCUS", "multimodal AI"), ("LOCATION", "Gurugram"), ("STATUS", "available"), ("MODE", "production"))
    cells = []
    for i, (label, value) in enumerate(items):
        x, y = 20 + (i % 2) * 170, 20 + (i // 2) * 64
        dot = f'<circle cx="{x}" cy="{y + 29}" r="4" fill="{theme.live}"/>' if label == "STATUS" else ""
        value_x = x + 13 if label == "STATUS" else x
        cells.append(f'<text x="{x}" y="{y + 8}" fill="{theme.muted}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1">{label}</text>{dot}<text x="{value_x}" y="{y + 34}" fill="{theme.title}" font-family="{MONO}" font-size="13" font-weight="600">{value}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="360" height="148" viewBox="0 0 360 148" role="img" aria-labelledby="title desc"><title id="title">Profile telemetry</title><desc id="desc">Focus: multimodal AI. Location: Gurugram. Status: available. Mode: production.</desc>{_defs(theme)}<rect x=".75" y=".75" width="358.5" height="146.5" rx="7" fill="url(#surface)" stroke="{theme.border}" stroke-width="1.5"/><path d="M8 1H352" stroke="{theme.accent}" stroke-width="2" stroke-linecap="round"/><path d="M180 14v120M14 74h332" stroke="{theme.border}"/>{''.join(cells)}</svg>\n'''


def _brand_icon(kind: str) -> str:
    if kind == "portfolio":
        return '''<g transform="translate(16 12)"><path d="M16 0a16 16 0 0 1 13.86 8H16a8 8 0 0 0-6.93 4L4.45 4A15.94 15.94 0 0 1 16 0z" fill="#EA4335"/><path d="M29.86 8A16 16 0 0 1 16 32l6.93-12A8 8 0 0 0 24 16c0-1.46-.39-2.83-1.07-4z" fill="#FBBC04"/><path d="M16 32A16 16 0 0 1 4.45 4l6.93 12A8 8 0 0 0 16 24c2.96 0 5.55-1.61 6.93-4z" fill="#34A853"/><circle cx="16" cy="16" r="6.8" fill="#4285F4" stroke="#FFF" stroke-width="2.4"/></g>'''
    if kind == "email":
        return '''<svg x="16" y="12" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><path d="M3 19V6" stroke="#4285F4"/><path d="M21 6v13" stroke="#34A853"/><path d="m3 6 9 7 9-7" stroke="#EA4335"/><path d="m3 6 3 2.33" stroke="#FBBC04"/><path d="m18 8.33 3-2.33" stroke="#C5221F"/></svg>'''
    return '''<svg x="16" y="12" width="32" height="32" viewBox="0 0 448 512"><path fill="#0A66C2" d="M416 32H31.9C14.3 32 0 46.5 0 64.3v383.4C0 465.5 14.3 480 31.9 480H416c17.6 0 32-14.5 32-32.3V64.3C448 46.5 433.6 32 416 32zM135.4 416H69V202.2h66.5V416zm-33.2-243c-21.3 0-38.5-17.3-38.5-38.5S80.9 96 102.2 96c21.2 0 38.5 17.3 38.5 38.5 0 21.3-17.2 38.5-38.5 38.5zm282.1 243h-66.4V312c0-24.8-.5-56.7-34.5-56.7-34.6 0-39.9 27-39.9 54.9V416h-66.4V202.2h63.7v29.2h.9c8.9-16.8 30.6-34.5 62.9-34.5 67.2 0 79.7 44.3 79.7 101.9V416z"/></svg>'''


def cta(theme: Theme, kind: str) -> str:
    title, label, action = {"portfolio": ("Open Ahmad Mujtaba's portfolio", "PORTFOLIO", "Open site"), "email": ("Email Ahmad Mujtaba", "EMAIL", "Email me"), "linkedin": ("Connect on LinkedIn", "LINKEDIN", "Connect")}[kind]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="136" height="56" viewBox="0 0 136 56" role="img" aria-labelledby="title desc"><title id="title">{title}</title><desc id="desc">Editorial {kind} action.</desc><rect x=".5" y=".5" width="135" height="55" rx="7.5" fill="{theme.bg2}" stroke="{theme.border}"/><path d="M8 1H128" stroke="{theme.accent}" stroke-width="2" stroke-linecap="round"/><g transform="translate(-5 2) scale(.74)">{_brand_icon(kind)}</g><path d="M46 12v32" stroke="{theme.border}"/><text x="55" y="22" fill="{theme.muted}" font-family="{MONO}" font-size="9" font-weight="700" letter-spacing=".65">{label}</text><text x="55" y="41" fill="{theme.title}" font-family="{DISPLAY}" font-size="12" font-weight="700">{action}</text><path d="M120 28h8m-3-3 3 3-3 3" fill="none" stroke="{theme.accent}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>\n'''


def featured_row(theme: Theme, repo: str) -> str:
    title, category, description, _, flow = FEATURED[repo]
    title_lines = _wrap(title, 14, 2)
    title_svg = "".join(f'<text x="32" y="{82 + i * 26}" fill="{theme.title}" font-family="{DISPLAY}" font-size="22" font-weight="700">{_esc(line)}</text>' for i, line in enumerate(title_lines))
    lines = _wrap(description, 48, 2)
    body = "".join(f'<text x="238" y="{100 + i * 24}" fill="{theme.text}" font-family="{DISPLAY}" font-size="16">{_esc(line)}</text>' for i, line in enumerate(lines))
    nodes = []
    for i, name in enumerate(flow):
        x, y = 690 + (i % 2) * 130, 50 + (i // 2) * 66
        nodes.append(f'<rect x="{x}" y="{y}" width="108" height="34" rx="3" fill="{theme.bg2}" stroke="{theme.border}"/><text x="{x + 54}" y="{y + 22}" text-anchor="middle" fill="{theme.text}" font-family="{MONO}" font-size="10">{_esc(name)}</text>')
    edges = f'<path d="M798 67h22M744 84v32M798 133h22" fill="none" stroke="{theme.accent}" stroke-width="1.5"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="180" viewBox="0 0 960 180" role="img" aria-labelledby="title desc"><title id="title">{_esc(title)}</title><desc id="desc">{_esc(description)} Flow: {_esc(' to '.join(flow))}.</desc>{_defs(theme)}<rect x=".75" y=".75" width="958.5" height="178.5" rx="8" fill="url(#surface)" stroke="{theme.border}" stroke-width="1.5"/><rect x="1" y="1" width="958" height="178" rx="8" fill="url(#rules)"/><path d="M210 20v140M660 20v140" stroke="{theme.border}"/><path d="M18 20v140" stroke="{theme.accent}" stroke-width="3"/><text x="32" y="48" fill="{theme.muted}" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="1.2">{_esc(category)}</text>{title_svg}<text x="32" y="144" fill="{theme.accent}" font-family="{MONO}" font-size="12" font-weight="700">OPEN REPOSITORY ↗</text><text x="238" y="55" fill="{theme.muted}" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="1.1">PROJECT / SYSTEM</text>{body}<text x="690" y="31" fill="{theme.muted}" font-family="{MONO}" font-size="11" font-weight="700" letter-spacing="1">ARCHITECTURE FLOW</text>{edges}{''.join(nodes)}</svg>\n'''


def featured_row_mobile(theme: Theme, repo: str) -> str:
    title, category, description, _, flow = FEATURED[repo]
    title_lines = _wrap(title, 25, 2)
    description_lines = _wrap(description, 38, 3)
    title_svg = "".join(f'<text x="28" y="{65 + i * 28}" fill="{theme.title}" font-family="{DISPLAY}" font-size="23" font-weight="700">{_esc(line)}</text>' for i, line in enumerate(title_lines))
    body_y = 133 if len(title_lines) > 1 else 108
    body = "".join(f'<text x="28" y="{body_y + i * 21}" fill="{theme.text}" font-family="{DISPLAY}" font-size="14">{_esc(line)}</text>' for i, line in enumerate(description_lines))
    node_positions = ((28, 267), (192, 267), (28, 329), (192, 329))
    nodes = "".join(f'<rect x="{x}" y="{y}" width="140" height="40" rx="4" fill="{theme.bg2}" stroke="{theme.border}"/><text x="{x + 70}" y="{y + 25}" text-anchor="middle" fill="{theme.text}" font-family="{MONO}" font-size="11">{_esc(name)}</text>' for (x, y), name in zip(node_positions, flow))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="360" height="392" viewBox="0 0 360 392" role="img" aria-labelledby="title desc"><title id="title">{_esc(title)}</title><desc id="desc">{_esc(description)} Flow: {_esc(' to '.join(flow))}.</desc>{_defs(theme)}<rect x=".75" y=".75" width="358.5" height="390.5" rx="8" fill="url(#surface)" stroke="{theme.border}" stroke-width="1.5"/><rect x="1" y="1" width="358" height="390" rx="8" fill="url(#rules)"/><path d="M16 18v184" stroke="{theme.accent}" stroke-width="3"/><text x="28" y="34" fill="{theme.muted}" font-family="{MONO}" font-size="11" font-weight="700" letter-spacing="1">{_esc(category)}</text>{title_svg}{body}<text x="28" y="210" fill="{theme.accent}" font-family="{MONO}" font-size="12" font-weight="700">OPEN REPOSITORY ↗</text><path d="M20 230h320" stroke="{theme.border}"/><text x="28" y="252" fill="{theme.muted}" font-family="{MONO}" font-size="11" font-weight="700" letter-spacing="1">ARCHITECTURE FLOW</text>{nodes}<path d="M168 287h24M98 307v22M168 349h24" fill="none" stroke="{theme.accent}" stroke-width="1.5"/></svg>\n'''


def contact_cell(theme: Theme, key: str) -> str:
    label, value, _, width = CONTACTS[key]
    size = 12
    value_lines = {"email": ("ahmad.iiitk", "@gmail.com"), "portfolio": ("pypi-ahmad", ".github.io")}.get(key, (value,))
    value_svg = "".join(f'<text x="14" y="{49 + i * 14}" fill="{theme.title}" font-family="{DISPLAY}" font-size="{size}" font-weight="600">{_esc(line)}</text>' for i, line in enumerate(value_lines))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="72" viewBox="0 0 {width} 72" role="img" aria-labelledby="title desc"><title id="title">{_esc(label.title())}: {_esc(value)}</title><desc id="desc">Open Ahmad Mujtaba's {_esc(label.lower())} contact.</desc><rect x=".75" y=".75" width="{width - 1.5}" height="70.5" rx="5" fill="{theme.bg2}" stroke="{theme.border}" stroke-width="1.5"/><path d="M6 1H{width - 6}" stroke="{theme.accent}" stroke-width="2" stroke-linecap="round"/><text x="14" y="25" fill="{theme.muted}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing=".9">{label}</text>{value_svg}<path d="M{width - 25} 22h9m-4-4 4 4-4 4" fill="none" stroke="{theme.accent}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>\n'''


def contact_aurora(theme: Theme) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="160" viewBox="0 0 960 160" role="img" aria-labelledby="title desc"><title id="title">Let’s work together</title><desc id="desc">An invitation to collaborate in production AI.</desc>{_defs(theme)}<rect x=".75" y=".75" width="958.5" height="158.5" rx="8" fill="url(#surface)" stroke="{theme.border}" stroke-width="1.5"/><rect x="1" y="1" width="958" height="158" rx="8" fill="url(#rules)"/><path d="M30 24v112" stroke="{theme.accent}" stroke-width="4"/><text x="54" y="48" fill="{theme.muted}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="2.2">OPEN TO COLLABORATION</text><text x="54" y="89" fill="{theme.title}" font-family="{DISPLAY}" font-size="34" font-weight="700">Let’s work together</text><path d="M520 24v112" stroke="{theme.border}"/><text x="554" y="61" fill="{theme.text}" font-family="{DISPLAY}" font-size="14">Production AI · Document Intelligence</text><text x="554" y="84" fill="{theme.text}" font-family="{DISPLAY}" font-size="14">Agentic Systems · Evaluation</text><circle cx="558" cy="116" r="4" fill="{theme.live}"/><text x="571" y="120" fill="{theme.muted}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1.2">AVAILABLE</text></svg>\n'''


def contact_aurora_mobile(theme: Theme) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="360" height="220" viewBox="0 0 360 220" role="img" aria-labelledby="title desc"><title id="title">Let’s work together</title><desc id="desc">An invitation to collaborate in production AI.</desc>{_defs(theme)}<rect x=".75" y=".75" width="358.5" height="218.5" rx="8" fill="url(#surface)" stroke="{theme.border}" stroke-width="1.5"/><rect x="1" y="1" width="358" height="218" rx="8" fill="url(#rules)"/><path d="M20 22v176" stroke="{theme.accent}" stroke-width="4"/><text x="38" y="47" fill="{theme.muted}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1.3">OPEN TO COLLABORATION</text><text x="38" y="84" fill="{theme.title}" font-family="{DISPLAY}" font-size="27" font-weight="700">Let’s work together</text><path d="M38 105h292" stroke="{theme.border}"/><text x="38" y="135" fill="{theme.text}" font-family="{DISPLAY}" font-size="14">Production AI · Document Intelligence</text><text x="38" y="160" fill="{theme.text}" font-family="{DISPLAY}" font-size="14">Agentic Systems · Evaluation</text><circle cx="42" cy="190" r="4" fill="{theme.live}"/><text x="55" y="194" fill="{theme.muted}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1.2">AVAILABLE</text></svg>\n'''


def workshop(theme: Theme, *, animated: bool) -> str:
    animation = "@media (prefers-reduced-motion:no-preference){.flow{animation:flow 12s linear infinite}}@keyframes flow{to{stroke-dashoffset:-800}}" if animated else ""
    trace = (("01", "document received", theme.text), ("02", "layout parsed", theme.text), ("03", "fields extracted", theme.text), ("04", "evaluation passed", theme.live), ("05", "review required · 2 fields", theme.attention))
    trace_svg = "".join(f'<text x="24" y="{56 + i * 22}" font-family="{MONO}" font-size="10"><tspan fill="{theme.muted}">{n}</tspan><tspan x="50" fill="{color}">{text}</tspan></text>' for i, (n, text, color) in enumerate(trace))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="260" viewBox="0 0 960 260" role="img" aria-labelledby="title description"><title id="title">Ahmad's AI workshop</title><desc id="description">An AI system workshop with document input, model evaluation, and an illustrative review trace.</desc><defs><linearGradient id="surface" x2="1" y2="1"><stop stop-color="{theme.bg}"/><stop offset="1" stop-color="{theme.bg2}"/></linearGradient><linearGradient id="line"><stop stop-color="{theme.system}"/><stop offset="1" stop-color="{theme.accent}"/></linearGradient><pattern id="rules" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M0 31.5H32" stroke="{theme.border}" opacity=".22"/></pattern><style>{animation}</style></defs><rect x="1" y="1" width="958" height="258" rx="12" fill="url(#surface)" stroke="{theme.border}"/><rect x="1" y="1" width="958" height="258" rx="12" fill="url(#rules)"/><path d="M24 18v30" stroke="{theme.accent}" stroke-width="3"/><text x="38" y="40" fill="{theme.title}" font-family="{MONO}" font-size="11" font-weight="700">DATAINTUITIONIST IN</text><text x="928" y="40" text-anchor="end" fill="{theme.muted}" font-family="{MONO}" font-size="10" letter-spacing="1.6">THE AI WORKSHOP</text><path d="M24 54H936" stroke="{theme.border}"/><g fill="none" stroke="{theme.system}" stroke-width="1.5"><path d="M190 139h168"/><path d="M510 139h170"/></g><g class="flow" fill="none" stroke="url(#line)" stroke-width="2.5" stroke-dasharray="12 220"><path d="M190 139h168"/><path d="M510 139h170"/></g><g transform="translate(72 78)"><g class="paper"><rect x="12" y="2" width="92" height="126" rx="5" fill="{theme.bg2}" stroke="{theme.border}" transform="rotate(8 58 65)"/><rect width="92" height="128" rx="5" fill="{theme.bg2}" stroke="{theme.system}" stroke-width="1.5" transform="rotate(-5 46 64)"/><path d="M18 30h42m-42 14h55m-55 14h55m-55 14h34" stroke="{theme.muted}" stroke-width="2"/><path d="M20 98h50" stroke="{theme.accent}" stroke-width="3"/></g></g><g transform="translate(358 73)"><rect width="152" height="132" rx="12" fill="{theme.bg2}" stroke="{theme.accent}" stroke-width="2"/><path d="M45 65l18-18 18 18-18 18zM69 65l18-18 18 18-18 18z" fill="none" stroke="{theme.accent}" stroke-width="3"/><circle cx="126" cy="23" r="4" fill="{theme.accent}"/><text x="76" y="112" text-anchor="middle" fill="{theme.title}" font-family="{MONO}" font-size="11" letter-spacing="1.6">BUILD / EVAL</text></g><g transform="translate(694 62)"><rect width="224" height="166" rx="6" fill="{theme.bg2}" stroke="{theme.border}" stroke-width="1.5"/><path d="M0 32h224" stroke="{theme.border}"/><circle cx="16" cy="16" r="3" fill="{theme.live}"/><text x="29" y="20" fill="{theme.muted}" font-family="{MONO}" font-size="9" letter-spacing="1.1">ILLUSTRATIVE TRACE</text>{trace_svg}</g><g fill="{theme.bg2}" stroke="{theme.accent}" stroke-width="2"><circle cx="260" cy="139" r="7"/><circle cx="604" cy="139" r="7"/></g></svg>\n'''


def workshop_mobile(theme: Theme, *, animated: bool) -> str:
    animation = "@media (prefers-reduced-motion:no-preference){.flow{animation:flow 12s linear infinite}}@keyframes flow{to{stroke-dashoffset:-500}}" if animated else ""
    trace = (("01", "document received", theme.text), ("02", "layout parsed", theme.text), ("03", "fields extracted", theme.text), ("04", "evaluation passed", theme.live), ("05", "review required · 2 fields", theme.attention))
    trace_svg = "".join(f'<text x="38" y="{292 + i * 27}" font-family="{MONO}" font-size="11"><tspan fill="{theme.muted}">{n}</tspan><tspan x="70" fill="{color}">{text}</tspan></text>' for i, (n, text, color) in enumerate(trace))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="360" height="450" viewBox="0 0 360 450" role="img" aria-labelledby="title description"><title id="title">Ahmad's AI workshop</title><desc id="description">An AI system workshop with document input, model evaluation, and an illustrative review trace.</desc><defs><linearGradient id="surface" x2="1" y2="1"><stop stop-color="{theme.bg}"/><stop offset="1" stop-color="{theme.bg2}"/></linearGradient><linearGradient id="line"><stop stop-color="{theme.system}"/><stop offset="1" stop-color="{theme.accent}"/></linearGradient><pattern id="rules" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M0 31.5H32" stroke="{theme.border}" opacity=".22"/></pattern><style>{animation}</style></defs><rect x="1" y="1" width="358" height="448" rx="10" fill="url(#surface)" stroke="{theme.border}"/><rect x="1" y="1" width="358" height="448" rx="10" fill="url(#rules)"/><path d="M18 16v32" stroke="{theme.accent}" stroke-width="3"/><text x="31" y="37" fill="{theme.title}" font-family="{MONO}" font-size="10" font-weight="700">DATAINTUITIONIST IN</text><text x="340" y="37" text-anchor="end" fill="{theme.muted}" font-family="{MONO}" font-size="9" letter-spacing="1.2">AI WORKSHOP</text><path d="M18 54H342" stroke="{theme.border}"/><path d="M118 146h38" fill="none" stroke="{theme.system}" stroke-width="1.5"/><path class="flow" d="M118 146h38" fill="none" stroke="url(#line)" stroke-width="2.5" stroke-dasharray="10 90"/><g transform="translate(30 86)"><g class="paper"><rect x="7" y="2" width="70" height="112" rx="5" fill="{theme.bg2}" stroke="{theme.border}" transform="rotate(7 35 56)"/><rect width="70" height="112" rx="5" fill="{theme.bg2}" stroke="{theme.system}"/><path d="M14 27h36m-36 15h43m-43 15h43m-43 15h28" stroke="{theme.muted}" stroke-width="2"/><path d="M14 88h42" stroke="{theme.accent}" stroke-width="3"/></g></g><g transform="translate(156 86)"><rect width="170" height="120" rx="10" fill="{theme.bg2}" stroke="{theme.accent}" stroke-width="2"/><path d="M55 54l16-16 16 16-16 16zM77 54l16-16 16 16-16 16z" fill="none" stroke="{theme.accent}" stroke-width="3"/><circle cx="145" cy="20" r="4" fill="{theme.accent}"/><text x="85" y="98" text-anchor="middle" fill="{theme.title}" font-family="{MONO}" font-size="11" letter-spacing="1.4">BUILD / EVAL</text></g><g transform="translate(20 232)"><rect width="320" height="196" rx="6" fill="{theme.bg2}" stroke="{theme.border}" stroke-width="1.5"/><path d="M0 38h320" stroke="{theme.border}"/><circle cx="18" cy="19" r="4" fill="{theme.live}"/><text x="32" y="23" fill="{theme.muted}" font-family="{MONO}" font-size="10" letter-spacing="1.1">ILLUSTRATIVE TRACE</text></g>{trace_svg}</svg>\n'''


def main() -> None:
    output = Path(__file__).resolve().parents[1] / "assets" / "profile"
    output.mkdir(parents=True, exist_ok=True)
    written = 0
    for theme in THEMES:
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
        (output / f"contact-aurora.{theme.suffix}.svg").write_text(contact_aurora(theme), encoding="utf-8"); written += 1
        (output / f"contact-aurora-mobile.{theme.suffix}.svg").write_text(contact_aurora_mobile(theme), encoding="utf-8"); written += 1
    print(f"Generated {written} profile assets in {output}")


if __name__ == "__main__":
    main()
