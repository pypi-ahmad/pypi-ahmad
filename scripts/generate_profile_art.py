"""Build deterministic, network-free artwork for the profile README.

Run from the repository root: uv run python scripts/generate_profile_art.py
Live repository statistics still come from generate_repo_cards.py and its workflow.
"""

from pathlib import Path

from generate_repo_cards import FEATURED, THEMES, RepoInfo, Theme, _render_svg


SECTIONS = {
    "featured-projects": ("Get-ChildItem .\\featured-projects", "SELECTED WORK"),
    "case-studies": ("Get-Content .\\case-studies.md", "ENGINEERING DECISIONS"),
    "public-projects": ("Get-ChildItem .\\projects -Directory", "OPEN SOURCE"),
    "about": ("Get-Content .\\about.json", "BACKGROUND"),
    "measured-outcomes": ("uv run pytest .\\outcomes -q", "EVIDENCE"),
    "professional-experience": ("git log -- .\\experience", "EXPERIENCE"),
    "skills": ("Get-ChildItem .\\capabilities -Recurse", "TOOLKIT"),
    "fde": (".\\learn.ps1 -Track ForwardDeployed", "LEARNING PATH"),
    "education": ("Get-Content .\\education.yaml", "CREDENTIALS"),
    "activity": ("git log --graph --oneline", "ACTIVITY"),
    "github-statistics": (".\\metrics.ps1 -Provider GitHub", "LIVE SNAPSHOT"),
    "repository-showcase": ("Get-ChildItem .\\repositories\\featured", "MORE WORK"),
    "repository": ("Get-Content .\\CONTRIBUTING.md", "GOVERNANCE"),
    "contact": ("Start-Process .\\contact.url", "AVAILABLE"),
}


def section_divider(theme: Theme, command: str, label: str) -> str:
    cyan = "#67E8F9" if theme.name == "dark" else "#0E7490"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="72" viewBox="0 0 960 72" role="img" aria-labelledby="title desc">
  <title id="title">{label.title()} terminal divider</title>
  <desc id="desc">A Windows Terminal section divider showing a PowerShell command for this section.</desc>
  <defs>
    <linearGradient id="surface" x2="1"><stop stop-color="{theme.bg}"/><stop offset="1" stop-color="{theme.bg2}"/></linearGradient>
    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{theme.muted}" opacity=".12"/></pattern>
  </defs>
  <rect x=".75" y=".75" width="958.5" height="70.5" rx="14" fill="url(#surface)" stroke="{theme.border}" stroke-width="1.5"/>
  <path d="M1 34h958" stroke="{theme.border}"/>
  <path d="M14 34V10q0-5 5-5h158q5 0 5 5v24" fill="{theme.bg}" stroke="{theme.border}"/>
  <path d="m29 15 8 6-8 6m12 0h9" fill="none" stroke="{theme.accent}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="61" y="24" fill="{theme.text}" font-family="Segoe UI,Arial,sans-serif" font-size="11">PowerShell</text>
  <text x="198" y="24" fill="{theme.muted}" font-family="Segoe UI,Arial,sans-serif" font-size="16">+</text>
  <g fill="none" stroke="{theme.muted}" stroke-width="1.3"><path d="M860 18h12M898 14h10v9h-10zM934 14l9 9m0-9-9 9"/></g>
  <rect x="12" y="38" width="936" height="24" rx="7" fill="url(#grid)"/>
  <text x="24" y="55" font-family="Cascadia Code,Consolas,monospace" font-size="11.5"><tspan fill="{theme.accent}">PS C:\\Users\\Ahmad\\profile&gt; </tspan><tspan fill="{cyan}">{command}</tspan></text>
  <text x="928" y="55" text-anchor="end" fill="{theme.muted}" font-family="Cascadia Code,Consolas,monospace" font-size="9" font-weight="700" letter-spacing="1.2">{label}</text>
</svg>
'''


def contact_aurora(theme: Theme) -> str:
    cyan = "#67E8F9" if theme.name == "dark" else "#0E7490"
    title = "#F5F3FF" if theme.name == "dark" else "#211C3B"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="160" viewBox="0 0 960 160" role="img" aria-labelledby="title desc">
  <title id="title">Let’s work together</title>
  <desc id="desc">A Windows Terminal PowerShell session inviting collaboration in production AI.</desc>
  <defs>
    <linearGradient id="surface" x2="1" y2="1"><stop stop-color="{theme.bg}"/><stop offset="1" stop-color="{theme.bg2}"/></linearGradient>
    <radialGradient id="violet"><stop stop-color="{theme.accent}" stop-opacity=".32"/><stop offset="1" stop-color="{theme.accent}" stop-opacity="0"/></radialGradient>
    <radialGradient id="aqua"><stop stop-color="{cyan}" stop-opacity=".22"/><stop offset="1" stop-color="{cyan}" stop-opacity="0"/></radialGradient>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="{theme.muted}" opacity=".13"/></pattern>
  </defs>
  <rect x=".75" y=".75" width="958.5" height="158.5" rx="18" fill="url(#surface)" stroke="{theme.border}" stroke-width="1.5"/>
  <path d="M1 35h958" stroke="{theme.border}"/>
  <path d="M14 35V10q0-5 5-5h166q5 0 5 5v25" fill="{theme.bg}" stroke="{theme.border}"/>
  <path d="m29 15 8 6-8 6m12 0h9" fill="none" stroke="{theme.accent}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="61" y="24" fill="{theme.text}" font-family="Segoe UI,Arial,sans-serif" font-size="11">PowerShell · Contact</text>
  <g fill="none" stroke="{theme.muted}" stroke-width="1.3"><path d="M860 18h12M898 14h10v9h-10zM934 14l9 9m0-9-9 9"/></g>
  <rect x="14" y="42" width="932" height="104" rx="12" fill="url(#grid)"/>
  <ellipse cx="390" cy="97" rx="260" ry="90" fill="url(#violet)"/><ellipse cx="610" cy="102" rx="250" ry="85" fill="url(#aqua)"/>
  <text x="32" y="60" font-family="Cascadia Code,Consolas,monospace" font-size="10"><tspan fill="{theme.accent}">PS C:\\Users\\Ahmad\\profile&gt; </tspan><tspan fill="{cyan}">Start-Process .\\contact.url</tspan></text>
  <text x="480" y="91" text-anchor="middle" fill="{theme.accent}" font-family="Cascadia Code,Consolas,monospace" font-size="11" font-weight="700" letter-spacing="2.5">OPEN TO COLLABORATION</text>
  <text x="480" y="119" text-anchor="middle" fill="{title}" font-family="Cascadia Code,Consolas,monospace" font-size="24" font-weight="700">LET’S WORK TOGETHER</text>
  <text x="480" y="139" text-anchor="middle" fill="{theme.muted}" font-family="Cascadia Code,Consolas,monospace" font-size="11">Production AI · Document Intelligence · Agentic Systems</text>
</svg>
'''


def workshop(theme: Theme, *, animated: bool) -> str:
    cyan = "#67E8F9" if theme.name == "dark" else "#0E7490"
    amber = "#FCD34D" if theme.name == "dark" else "#92400E"
    animation = """
      .flow { animation: flow 12s linear infinite; }
      .paper { animation: float 12s ease-in-out infinite; }
      @keyframes flow { to { stroke-dashoffset: -800; } }
      @keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-6px); } }
      @media (prefers-reduced-motion: reduce) { .flow,.paper { animation: none; } }
    """ if animated else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="260" viewBox="0 0 960 260" role="img" aria-labelledby="title description">
  <title id="title">Ahmad's AI workshop</title>
  <desc id="description">An illustrated workspace: document pages, retrieval nodes, a model chip, and review tools connected by colored paths. A visual metaphor for separate AI projects.</desc>
  <defs>
    <linearGradient id="surface" x2="1" y2="1"><stop stop-color="{theme.bg}"/><stop offset="1" stop-color="{theme.bg2}"/></linearGradient>
    <linearGradient id="line"><stop stop-color="{cyan}"/><stop offset=".5" stop-color="{theme.accent}"/><stop offset="1" stop-color="{amber}"/></linearGradient>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{theme.muted}" opacity=".16"/></pattern>
    <style>{animation}</style>
  </defs>
  <rect x="1" y="1" width="958" height="258" rx="24" fill="url(#surface)" stroke="{theme.border}"/>
  <path d="M1 40h958" stroke="{theme.border}"/>
  <path d="M14 40V11q0-6 6-6h174q6 0 6 6v29" fill="{theme.bg}" stroke="{theme.border}"/>
  <path d="m30 16 8 6-8 6m12 0h10" fill="none" stroke="{theme.accent}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="63" y="25" fill="{theme.text}" font-family="Segoe UI,Arial,sans-serif" font-size="11">PowerShell · AI Workshop</text>
  <g fill="none" stroke="{theme.muted}" stroke-width="1.3"><path d="M860 20h12M898 15h10v10h-10zM934 15l9 9m0-9-9 9"/></g>
  <rect x="14" y="45" width="932" height="201" rx="14" fill="url(#grid)"/>
  <ellipse cx="479" cy="139" rx="160" ry="104" fill="{theme.accent}" opacity=".045"/>
  <g font-family="Segoe UI,Arial,sans-serif" font-size="12" letter-spacing="2" font-weight="600">
    <text x="32" y="58" fill="{theme.accent}">PS C:\\USERS\\AHMAD&gt; DATAINTUITIONIST IN</text>
    <text x="928" y="58" text-anchor="end" fill="{theme.muted}">THE AI WORKSHOP</text>
  </g>
  <g fill="none" stroke="{theme.border}" stroke-width="2">
    <path d="M185 130h95q24 0 24-24V84q0-20 22-20h94"/>
    <path d="M185 150h99q20 0 20 20v28q0 20 22 20h94"/>
    <path d="M539 88h69q22 0 22 22v12q0 20 22 20h88"/>
    <path d="M539 188h69q22 0 22-22v-4q0-20 22-20h88"/>
  </g>
  <g class="flow" fill="none" stroke="url(#line)" stroke-width="3" stroke-linecap="round" stroke-dasharray="12 388">
    <path d="M185 130h95q24 0 24-24V84q0-20 22-20h94"/>
    <path d="M185 150h99q20 0 20 20v28q0 20 22 20h94"/>
    <path d="M539 88h69q22 0 22 22v12q0 20 22 20h88"/>
    <path d="M539 188h69q22 0 22-22v-4q0-20 22-20h88"/>
  </g>
  <g transform="translate(80 67)">
    <g class="paper">
      <rect x="15" y="4" width="91" height="128" rx="9" fill="{theme.bg2}" stroke="{theme.border}" transform="rotate(9 60 70)"/>
      <rect x="0" y="12" width="91" height="128" rx="9" fill="{theme.bg}" stroke="{cyan}" stroke-width="1.5" transform="rotate(-6 45 75)"/>
      <path d="M18 39h42m-42 12h54m-54 15h54m-54 10h32" stroke="{theme.muted}" stroke-width="2" stroke-linecap="round"/>
      <rect x="16" y="94" width="60" height="25" rx="4" fill="{cyan}" opacity=".12"/>
      <path d="M23 103h23m-23 8h44" stroke="{cyan}" stroke-width="2" stroke-linecap="round"/>
    </g>
  </g>
  <g fill="{theme.bg}" stroke="{cyan}" stroke-width="2">
    <circle cx="300" cy="91" r="10"/><circle cx="264" cy="202" r="6"/>
    <circle cx="356" cy="64" r="6"/><circle cx="362" cy="218" r="9"/>
  </g>
  <g transform="translate(413 73)">
    <rect x="-12" y="-12" width="156" height="156" rx="30" fill="{theme.accent}" opacity=".07"/>
    <rect width="132" height="132" rx="24" fill="{theme.bg}" stroke="{theme.accent}" stroke-width="2"/>
    <g stroke="{theme.accent}" stroke-width="2" stroke-linecap="round">
      <path d="M34-8v8m32-8v8m32-8v8M34 132v8m32-8v8m32-8v8M-8 34h8m-8 32h8m-8 32h8M132 34h8m-8 32h8m-8 32h8"/>
    </g>
    <path d="M37 65l18-18 18 18-18 18z M60 65l18-18 18 18-18 18z" fill="none" stroke="{theme.accent}" stroke-width="3" stroke-linejoin="round"/>
    <circle cx="111" cy="22" r="4" fill="{cyan}"/>
    <text x="66" y="111" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="12" letter-spacing="2" fill="{theme.text}">BUILD / EVAL</text>
  </g>
  <g transform="translate(744 78)">
    <rect width="138" height="123" rx="12" fill="{theme.bg}" stroke="{theme.border}" stroke-width="1.5"/>
    <path d="M0 28h138" stroke="{theme.border}"/>
    <g fill="{theme.accent}"><circle cx="14" cy="14" r="3"/><circle cx="25" cy="14" r="3" opacity=".6"/><circle cx="36" cy="14" r="3" opacity=".3"/></g>
    <path d="M17 49l8 7-8 7m17 0h17" fill="none" stroke="{cyan}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M17 83h59m-59 12h42" stroke="{theme.muted}" stroke-width="2" stroke-linecap="round"/>
    <circle cx="112" cy="91" r="13" fill="{amber}" opacity=".12"/>
    <path d="M105 91l5 5 9-11" stroke="{amber}" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <g fill="{amber}"><circle cx="665" cy="86" r="5"/><circle cx="691" cy="192" r="4"/></g>
  <path d="M683 64v10m-5-5h10M229 63v8m-4-4h8" stroke="{theme.accent}" stroke-width="1.5"/>
</svg>
'''


def main() -> None:
    output = Path(__file__).resolve().parents[1] / "assets" / "profile"
    output.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        for animated in (True, False):
            name = "workshop" if animated else "workshop-static"
            (output / f"{name}.{theme.suffix}.svg").write_text(
                workshop(theme, animated=animated), encoding="utf-8"
            )
        for repo, (title, _, description, _) in FEATURED.items():
            info = RepoInfo("pypi-ahmad", repo, description, 0, 0, "", "", f"https://github.com/pypi-ahmad/{repo}")
            (output / f"{repo}.{theme.suffix}.svg").write_text(
                _render_svg(info, theme, show_metrics=False), encoding="utf-8"
            )
        for name, (command, label) in SECTIONS.items():
            (output / f"section-{name}.{theme.suffix}.svg").write_text(
                section_divider(theme, command, label), encoding="utf-8"
            )
        (output / f"contact-aurora.{theme.suffix}.svg").write_text(
            contact_aurora(theme), encoding="utf-8"
        )
    print(f"Generated {14 + len(SECTIONS) * 2} profile assets in {output}")


if __name__ == "__main__":
    main()
