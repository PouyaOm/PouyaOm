"""
Generates info-card.svg: a bright, rounded, gently-animated profile card.
Animation here is plain CSS (@keyframes) declared inside the SVG's own
<style> block - that still runs when GitHub embeds the file as an <img>,
even though inline <script> would not.

Edit HANDLE / TAGLINE / SKILLS / STATUS below - no SVG markup needed for
routine updates.
"""
from html import escape

# ---- content -------------------------------------------------------------
HANDLE = "Pouya Omidi"
GREETING = f"Hey, I'm {HANDLE}"
TAGLINE = "University Student Interested In AI"
SKILLS = ["Python", "SQL", "Math"]
FOCUS = "Open source contributor"
STATUS = "Currently working on research"

# ---- palette (dark, muted jewel tones) ------------------------------------
GRAD_STOPS = [("0%", "#0B1120"), ("55%", "#111827"), ("100%", "#1E1B4B")]
TEXT = "#E5E7EB"
TEXT_MUTED = "rgba(229,231,235,0.62)"
HANDLE_COLOR = "#60A5FA"
BLOB_COLOR = "#312E81"

# translucent fill + matching border + bright-on-dark text, dashboard style
PILLS = [
    {"bg": "rgba(59,130,246,0.14)", "border": "rgba(96,165,250,0.4)", "fg": "#93C5FD"},
    {"bg": "rgba(16,185,129,0.14)", "border": "rgba(52,211,153,0.4)", "fg": "#6EE7B7"},
    {"bg": "rgba(244,63,94,0.14)", "border": "rgba(251,113,133,0.4)", "fg": "#FDA4AF"},
    {"bg": "rgba(217,119,6,0.14)", "border": "rgba(251,191,36,0.4)", "fg": "#FCD34D"},
    {"bg": "rgba(139,92,246,0.14)", "border": "rgba(167,139,250,0.4)", "fg": "#C4B5FD"},
]

FONT = ("'Segoe UI Rounded', 'SF Pro Rounded', 'Baloo 2', 'Quicksand', "
        "'Segoe UI', system-ui, -apple-system, sans-serif")

W, H = 480, 300


def esc(s: str) -> str:
    return escape(s, quote=True)


def pill(x, y, label, color, font_size=13, height=30, pad=14):
    width = pad * 2 + len(label) * (font_size * 0.62)
    rect = (f'<rect x="{x}" y="{y}" width="{width:.0f}" height="{height}" rx="{height/2}" '
            f'fill="{color["bg"]}" stroke="{color["border"]}"/>')
    text = (f'<text x="{x+width/2:.0f}" y="{y+height/2+4.5:.0f}" font-size="{font_size}" '
            f'font-weight="700" fill="{color["fg"]}" text-anchor="middle">{esc(label)}</text>')
    return rect + text, width


parts = []
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" font-family="{FONT}">'
)

parts.append(f'''
<defs>
  <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
    {''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in GRAD_STOPS)}
  </linearGradient>
  <clipPath id="clip"><rect width="{W}" height="{H}" rx="24"/></clipPath>
  <filter id="soft"><feGaussianBlur stdDeviation="18"/></filter>
</defs>
<style>
  text {{ shape-rendering: geometricPrecision; }}
  .bg-anim {{ animation: hue 10s ease-in-out infinite alternate; }}
  @keyframes hue {{ from {{ filter: hue-rotate(-6deg); }} to {{ filter: hue-rotate(6deg); }} }}
  .blob {{ opacity: .45; }}
  .blob1 {{ animation: float1 9s ease-in-out infinite; }}
  .blob2 {{ animation: float2 11s ease-in-out infinite; }}
  @keyframes float1 {{ 0%,100% {{ transform: translate(0,0); }} 50% {{ transform: translate(16px,-14px); }} }}
  @keyframes float2 {{ 0%,100% {{ transform: translate(0,0); }} 50% {{ transform: translate(-14px,12px); }} }}
  .wave {{ display: inline-block; transform-origin: 70% 75%; animation: wave 2.4s ease-in-out infinite; }}
  @keyframes wave {{
    0%, 100% {{ transform: rotate(0deg); }}
    15% {{ transform: rotate(14deg); }}
    30% {{ transform: rotate(-8deg); }}
    45% {{ transform: rotate(14deg); }}
    60% {{ transform: rotate(-4deg); }}
    75% {{ transform: rotate(10deg); }}
  }}
  .dot {{ animation: pulse 1.6s ease-in-out infinite; transform-origin: center; }}
  @keyframes pulse {{ 0%,100% {{ opacity: 1; transform: scale(1); }} 50% {{ opacity: .35; transform: scale(1.7); }} }}
  .underline {{ stroke-dasharray: 220; animation: draw 2.4s ease-out forwards; }}
  @keyframes draw {{ from {{ stroke-dashoffset: 220; }} to {{ stroke-dashoffset: 0; }} }}
</style>
<g clip-path="url(#clip)">
  <g class="bg-anim"><rect width="{W}" height="{H}" fill="url(#bg)"/></g>
  <circle class="blob blob1" cx="{W-60}" cy="50" r="90" fill="{BLOB_COLOR}" filter="url(#soft)"/>
  <circle class="blob blob2" cx="40" cy="{H-40}" r="110" fill="{BLOB_COLOR}" filter="url(#soft)"/>
</g>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="24" fill="none" stroke="rgba(255,255,255,0.10)"/>
''')

x_pad = 28

# greeting
parts.append(
    f'<text x="{x_pad}" y="52" font-size="24" font-weight="800" fill="{TEXT}">'
    f'<tspan class="wave">👋</tspan> {esc(GREETING)}</text>'
)

# tagline
parts.append(
    f'<text x="{x_pad}" y="80" font-size="14" fill="{TEXT_MUTED}">{esc(TAGLINE)}</text>'
)

# skill pills (wrap onto rows as needed)
py = 108
px = x_pad
row_h = 40
max_w = W - x_pad
i = 0
for skill in SKILLS:
    color = PILLS[i % len(PILLS)]
    markup, width = pill(px, py, skill, color)
    if px + width > max_w:
        px = x_pad
        py += row_h
        markup, width = pill(px, py, skill, color)
    parts.append(markup)
    px += width + 10
    i += 1

py += row_h + 4
focus_color = PILLS[i % len(PILLS)]
markup, width = pill(x_pad, py, f"🌱 {FOCUS}", focus_color, font_size=13)
parts.append(markup)

# status row with pulsing dot
sy = py + 52
parts.append(f'<circle class="dot" cx="{x_pad+5}" cy="{sy-4}" r="5" fill="#34D399"/>')
parts.append(
    f'<text x="{x_pad+20}" y="{sy}" font-size="13" fill="{TEXT_MUTED}">{esc(STATUS)}</text>'
)

# footer: handle with animated underline
fy = H - 26
parts.append(f'<text x="{x_pad}" y="{fy}" font-size="14" font-weight="700" fill="{HANDLE_COLOR}">@{esc(HANDLE)}</text>')
underline_w = 16 + len(HANDLE) * 8.5
parts.append(
    f'<path class="underline" d="M{x_pad} {fy+6} q {underline_w/2:.0f} 8 {underline_w:.0f} 0" '
    f'stroke="{HANDLE_COLOR}" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
)

parts.append('</svg>')

with open('info-card.svg', 'w') as f:
    f.write('\n'.join(parts))
print(f"Wrote info-card.svg ({W}x{H})")