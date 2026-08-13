"""
Generates profile-links.svg for the GitHub README.

Wide horizontal version designed to fill the README width.
"""

from html import escape


# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------

TECH_STACK = [
    ("Python", "#3776AB"),
    ("C++", "#00599C"),
    ("Go", "#00ADD8"),
    ("Linux", "#FCC624"),
    ("Git", "#F05032"),
    ("Docker", "#2496ED"),
    ("PostgreSQL", "#4169E1"),
    ("TensorFlow", "#FF6F00"),
]

LINKEDIN = "https://linkedin.com/in/pouya-omidi"
EMAIL = "mailto:Pouya.omidi05@gmail.com"


# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------

BG_START = "#0B1120"
BG_MID = "#111827"
BG_END = "#1E1B4B"

TEXT = "#E5E7EB"
MUTED = "rgba(229,231,235,0.60)"
BORDER = "rgba(255,255,255,0.10)"
CARD_BG = "rgba(255,255,255,0.035)"

LINKEDIN_COLOR = "#60A5FA"
EMAIL_COLOR = "#F87171"

FONT = (
    "'Segoe UI Rounded', 'SF Pro Rounded', 'Baloo 2', "
    "'Quicksand', 'Segoe UI', system-ui, sans-serif"
)


# Wide banner
W = 1200
H = 300


def esc(value: str) -> str:
    return escape(value, quote=True)


# ---------------------------------------------------------------------------
# Tech pill
# ---------------------------------------------------------------------------

def tech_pill(x, y, name, accent, index):

    width = 108 + len(name) * 5.2
    height = 42

    delay = index * 0.12

    return f"""
    <g
      class="tech"
      style="animation-delay:{delay:.2f}s">

      <rect
        x="{x:.0f}"
        y="{y:.0f}"
        width="{width:.0f}"
        height="{height}"
        rx="21"
        fill="{CARD_BG}"
        stroke="{accent}"
        stroke-opacity="0.35"
      />

      <circle
        cx="{x + 22:.0f}"
        cy="{y + 21:.0f}"
        r="6"
        fill="{accent}"
        opacity="0.9"
      />

      <text
        x="{x + 38:.0f}"
        y="{y + 26:.0f}"
        font-size="14"
        font-weight="700"
        fill="{TEXT}">
        {esc(name)}
      </text>

    </g>
    """, width


# ---------------------------------------------------------------------------
# Social button
# ---------------------------------------------------------------------------

def social_button(x, y, width, label, url, accent):

    return f"""
    <a href="{esc(url)}">

      <g class="social">

        <rect
          x="{x}"
          y="{y}"
          width="{width}"
          height="44"
          rx="22"
          fill="rgba(255,255,255,0.04)"
          stroke="{accent}"
          stroke-opacity="0.35"
        />

        <circle
          cx="{x + 22}"
          cy="{y + 22}"
          r="9"
          fill="{accent}"
        />

        <text
          x="{x + 22}"
          y="{y + 26}"
          text-anchor="middle"
          font-size="11"
          font-weight="900"
          fill="#0B1120">
          {label[0]}
        </text>

        <text
          x="{x + 42}"
          y="{y + 27}"
          font-size="13"
          font-weight="700"
          fill="{TEXT}">
          {esc(label)}
        </text>

      </g>

    </a>
    """


# ---------------------------------------------------------------------------
# SVG
# ---------------------------------------------------------------------------

parts = []

parts.append(
    f'''<svg
      xmlns="http://www.w3.org/2000/svg"
      width="{W}"
      height="{H}"
      viewBox="0 0 {W} {H}"
      font-family="{FONT}">
'''
)


# ---------------------------------------------------------------------------
# Definitions + animation
# ---------------------------------------------------------------------------

parts.append(
    f"""
<defs>

  <linearGradient
    id="bg"
    x1="0%"
    y1="0%"
    x2="100%"
    y2="100%">

    <stop offset="0%" stop-color="{BG_START}"/>
    <stop offset="55%" stop-color="{BG_MID}"/>
    <stop offset="100%" stop-color="{BG_END}"/>

  </linearGradient>

  <filter id="blur">
    <feGaussianBlur stdDeviation="30"/>
  </filter>

  <clipPath id="clip">
    <rect width="{W}" height="{H}" rx="26"/>
  </clipPath>

</defs>

<style>

  .background {{
    animation: backgroundMove 10s ease-in-out infinite alternate;
    transform-origin: center;
  }}

  @keyframes backgroundMove {{

    from {{
      transform: scale(1);
    }}

    to {{
      transform: scale(1.035);
    }}

  }}


  .orb1 {{
    animation: orb1 9s ease-in-out infinite;
  }}

  .orb2 {{
    animation: orb2 11s ease-in-out infinite;
  }}

  @keyframes orb1 {{

    0%,100% {{
      transform: translate(0,0);
    }}

    50% {{
      transform: translate(-25px,20px);
    }}

  }}

  @keyframes orb2 {{

    0%,100% {{
      transform: translate(0,0);
    }}

    50% {{
      transform: translate(25px,-20px);
    }}

  }}


  .tech {{
    animation: float 4s ease-in-out infinite;
  }}

  @keyframes float {{

    0%,100% {{
      transform: translateY(0);
    }}

    50% {{
      transform: translateY(-4px);
    }}

  }}


  .social {{
    animation: socialFloat 5s ease-in-out infinite;
  }}

  @keyframes socialFloat {{

    0%,100% {{
      transform: translateY(0);
    }}

    50% {{
      transform: translateY(-2px);
    }}

  }}

  text {{
    shape-rendering: geometricPrecision;
  }}

</style>


<g clip-path="url(#clip)">

  <rect
    class="background"
    width="{W}"
    height="{H}"
    fill="url(#bg)"
  />

  <circle
    class="orb1"
    cx="1080"
    cy="50"
    r="150"
    fill="#312E81"
    opacity="0.35"
    filter="url(#blur)"
  />

  <circle
    class="orb2"
    cx="80"
    cy="260"
    r="150"
    fill="#1D4ED8"
    opacity="0.20"
    filter="url(#blur)"
  />

</g>


<rect
  x="0.5"
  y="0.5"
  width="{W-1}"
  height="{H-1}"
  rx="26"
  fill="none"
  stroke="{BORDER}"
/>
"""
)


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

parts.append(
    f"""
<text
  x="36"
  y="48"
  font-size="21"
  font-weight="800"
  fill="{TEXT}">
  Tech Stack
</text>

<text
  x="36"
  y="72"
  font-size="13"
  fill="{MUTED}">
  Tools and technologies I work with
</text>
"""
)


# ---------------------------------------------------------------------------
# Tech stack - single horizontal row
# ---------------------------------------------------------------------------

x = 36
y = 95
gap = 10

for i, (name, accent) in enumerate(TECH_STACK):

    markup, width = tech_pill(
        x,
        y,
        name,
        accent,
        i
    )

    parts.append(markup)

    x += width + gap


# ---------------------------------------------------------------------------
# Divider
# ---------------------------------------------------------------------------

divider_y = 165

parts.append(
    f"""
<line
  x1="36"
  y1="{divider_y}"
  x2="{W - 36}"
  y2="{divider_y}"
  stroke="{BORDER}"
/>
"""
)


# ---------------------------------------------------------------------------
# Connect section
# ---------------------------------------------------------------------------

parts.append(
    f"""
<text
  x="36"
  y="204"
  font-size="21"
  font-weight="800"
  fill="{TEXT}">
  Connect
</text>

<text
  x="36"
  y="228"
  font-size="13"
  fill="{MUTED}">
  Find me online
</text>
"""
)


# ---------------------------------------------------------------------------
# Social buttons on the same horizontal line
# ---------------------------------------------------------------------------

parts.append(
    social_button(
        36,
        244,
        170,
        "LinkedIn",
        LINKEDIN,
        LINKEDIN_COLOR
    )
)

parts.append(
    social_button(
        218,
        244,
        170,
        "Email",
        EMAIL,
        EMAIL_COLOR
    )
)


# ---------------------------------------------------------------------------
# Right-side footer
# ---------------------------------------------------------------------------

parts.append(
    f"""
<text
  x="{W - 36}"
  y="269"
  text-anchor="end"
  font-size="12"
  fill="{MUTED}">
  Building • Learning • Contributing
</text>
"""
)


parts.append("</svg>")


# ---------------------------------------------------------------------------
# Write
# ---------------------------------------------------------------------------

with open("profile-links.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(parts))

print(f"Wrote profile-links.svg ({W}x{H})")