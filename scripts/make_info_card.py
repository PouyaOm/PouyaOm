from datetime import datetime
from html import escape

HANDLE = "PouyaOm"
BRANCH = "main"
COMMIT_HASH = "9f3a1c7"
DATE = datetime.now().strftime("%a %b %-d %Y")

MESSAGE = "Building cool stuff, one commit at a time."

FIELDS = [
    ("role", "Self-taught developer"),
    ("stack", "Python · JavaScript · React"),
    ("focus", "Open source contributor"),
    ("status", "Shipping something new"),
]

DIFFSTAT = "4 fields changed, 4 insertions(+)"

# ---- design tokens (GitHub dark UI palette) -----------------------------
BG = "#0d1117"
BORDER = "#30363d"
TEXT = "#e6edf3"
MUTED = "#7d8590"
DIM = "#484f58"
GREEN = "#3fb950"
BLUE = "#58a6ff"
AMBER = "#d29922"
FONT = "ui-monospace, 'SFMono-Regular', 'SF Mono', Consolas, 'Liberation Mono', Menlo, monospace"

W = 480
FIELD_ROW_H = 24
field_rows = len(FIELDS)

# running layout cursor - each block below advances `y` and reads
# from these anchors so spacing stays consistent if fields are added
HEADER_Y0 = 32
HEADER_LINE_H = 20
MESSAGE_Y = HEADER_Y0 + 2 * HEADER_LINE_H + 32
RULE1_Y = MESSAGE_Y + 18
HUNK_Y = RULE1_Y + 24
FIELD_START_Y = HUNK_Y + 28
FIELDS_END_Y = FIELD_START_Y + (field_rows - 1) * FIELD_ROW_H
RULE2_Y = FIELDS_END_Y + 26
H = RULE2_Y + 40


def esc(s: str) -> str:
    return escape(s, quote=True)


parts = []
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" font-family="{FONT}">'
)
parts.append(
    '<style>text{shape-rendering:geometricPrecision;} '
    '.msg{font-style:italic;}</style>'
)

# panel
parts.append(
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="6" '
    f'fill="{BG}" stroke="{BORDER}"/>'
)

# commit header
x_pad = 24
y = HEADER_Y0
parts.append(f'<text x="{x_pad}" y="{y}" font-size="13" fill="{AMBER}">commit</text>')
parts.append(
    f'<text x="{x_pad+58}" y="{y}" font-size="13" fill="{BLUE}">{esc(COMMIT_HASH)}</text>'
)
parts.append(
    f'<text x="{x_pad+58+7*len(COMMIT_HASH)+10}" y="{y}" font-size="13" fill="{MUTED}">'
    f'(HEAD -&gt; {esc(BRANCH)})</text>'
)
y += HEADER_LINE_H
parts.append(f'<text x="{x_pad}" y="{y}" font-size="13" fill="{MUTED}">Author:</text>')
parts.append(f'<text x="{x_pad+64}" y="{y}" font-size="13" fill="{TEXT}">{esc(HANDLE)}</text>')
y += HEADER_LINE_H
parts.append(f'<text x="{x_pad}" y="{y}" font-size="13" fill="{MUTED}">Date:</text>')
parts.append(f'<text x="{x_pad+64}" y="{y}" font-size="13" fill="{TEXT}">{esc(DATE)}</text>')

# commit message
parts.append(
    f'<text class="msg" x="{x_pad+16}" y="{MESSAGE_Y}" font-size="14" fill="{TEXT}">'
    f'{esc(MESSAGE)}</text>'
)

# hunk header + rule
parts.append(f'<line x1="{x_pad}" y1="{RULE1_Y}" x2="{W-x_pad}" y2="{RULE1_Y}" stroke="{BORDER}"/>')
parts.append(
    f'<text x="{x_pad}" y="{HUNK_Y}" font-size="12" fill="{MUTED}">'
    f'@@ <tspan fill="{BLUE}">profile.card</tspan> @@</text>'
)

# diff-style fields
label_w = max(len(k) for k, _ in FIELDS)
fy = FIELD_START_Y
for key, val in FIELDS:
    parts.append(f'<text x="{x_pad}" y="{fy}" font-size="13" fill="{GREEN}">+</text>')
    parts.append(
        f'<text x="{x_pad+16}" y="{fy}" font-size="13" fill="{MUTED}">'
        f'{esc(key.ljust(label_w))}</text>'
    )
    parts.append(
        f'<text x="{x_pad+16+9*(label_w+2)}" y="{fy}" font-size="13" fill="{TEXT}">'
        f'{esc(val)}</text>'
    )
    fy += FIELD_ROW_H

# footer diffstat
parts.append(f'<line x1="{x_pad}" y1="{RULE2_Y}" x2="{W-x_pad}" y2="{RULE2_Y}" stroke="{BORDER}"/>')
parts.append(
    f'<text x="{x_pad}" y="{RULE2_Y+22}" font-size="11" fill="{DIM}">{esc(DIFFSTAT)}</text>'
)
parts.append(
    f'<text x="{W-x_pad}" y="{RULE2_Y+22}" font-size="11" fill="{BLUE}" text-anchor="end">'
    f'@{esc(HANDLE)}</text>'
)

parts.append('</svg>')

with open('info-card.svg', 'w') as f:
    f.write('\n'.join(parts))
print(f"Wrote info-card.svg ({W}x{H})")