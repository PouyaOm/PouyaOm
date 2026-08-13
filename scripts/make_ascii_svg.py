"""
Generates avi-ascii.svg from source-prepped.png (output of prep_photo.py).

The old version drew bare ASCII text at 40% gray with no background - on
a white page that's almost invisible, and next to the other two cards it
just looked broken/unfinished. This version wraps it in the same dark
rounded card as make_info_card.py / render_heatmap_svg.py, boosts
contrast, and adds a soft light-sweep animation that loops across the
portrait (CSS-only, so it still animates when GitHub embeds this as an
<img>).
"""
from PIL import Image
import numpy as np
from html import escape

RAMP = " .`:-=+*cs#%@"
GRID_W, GRID_H = 100, 53
CHAR_W, CHAR_H = 4, 4  # px per character cell, must match font-size below

# ---- palette (matches make_info_card.py / render_heatmap_svg.py) --------
PANEL_BG = "#0B1120"
BORDER = "rgba(255,255,255,0.10)"
BASE_COLOR = "#4C5C82"      # dim structure, always visible
SWEEP_COLOR = "#93C5FD"     # bright accent revealed as the light passes
CAPTION_COLOR = "rgba(229,231,235,0.55)"
DOT_COLOR = "#34D399"
HANDLE = "PouyaOm"

FONT = ("'Segoe UI Rounded', 'SF Pro Rounded', 'Baloo 2', 'Quicksand', "
        "'Segoe UI', system-ui, -apple-system, sans-serif")

PAD_X, PAD_TOP = 24, 24
GRID_PX_W, GRID_PX_H = GRID_W * CHAR_W, GRID_H * CHAR_H
CAPTION_H = 40
W = GRID_PX_W + PAD_X * 2
H = PAD_TOP + GRID_PX_H + CAPTION_H


def image_to_matrix(path: str) -> list[str]:
    img = Image.open(path).convert('L').resize((GRID_W, GRID_H))
    pixels = np.array(img)
    rows = []
    for y in range(GRID_H):
        row = []
        for x in range(GRID_W):
            idx = int(pixels[y][x] / 255 * (len(RAMP) - 1))
            row.append(RAMP[idx] if idx > 0 else ' ')
        rows.append(''.join(row))
    return rows


def render_svg(rows: list[str], out_path: str = 'avi-ascii.svg') -> None:
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" font-family="{FONT}">'
    )
    parts.append(f'''
<defs>
  <clipPath id="cardclip"><rect width="{W}" height="{H}" rx="24"/></clipPath>
  <clipPath id="gridclip"><rect x="{PAD_X}" y="{PAD_TOP}" width="{GRID_PX_W}" height="{GRID_PX_H}"/></clipPath>
  <linearGradient id="sweepGrad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{SWEEP_COLOR}" stop-opacity="0"/>
    <stop offset="50%" stop-color="{SWEEP_COLOR}" stop-opacity="0.9"/>
    <stop offset="100%" stop-color="{SWEEP_COLOR}" stop-opacity="0"/>
  </linearGradient>
  <mask id="sweepMask">
    <rect class="sweep" y="{PAD_TOP}" width="{GRID_PX_W*0.35:.0f}" height="{GRID_PX_H}" fill="url(#sweepGrad)"/>
  </mask>
</defs>
<style>
  text {{ font: {CHAR_H}px monospace; white-space: pre; }}
  .base {{ fill: {BASE_COLOR}; }}
  .sweep-text {{ fill: {SWEEP_COLOR}; }}
  .sweep {{ animation: sweep 5s linear infinite; }}
  @keyframes sweep {{
    from {{ transform: translateX(-{GRID_PX_W*0.35:.0f}px); }}
    to   {{ transform: translateX({GRID_PX_W}px); }}
  }}
  .dot {{ animation: pulse 1.6s ease-in-out infinite; transform-origin: center; }}
  @keyframes pulse {{ 0%,100% {{ opacity: 1; transform: scale(1); }} 50% {{ opacity: .35; transform: scale(1.7); }} }}
</style>
<g clip-path="url(#cardclip)"><rect width="{W}" height="{H}" fill="{PANEL_BG}"/></g>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="24" fill="none" stroke="{BORDER}"/>
''')

    # base layer (always-visible dim portrait)
    parts.append(f'<g class="base" clip-path="url(#gridclip)">')
    for y, row in enumerate(rows):
        ty = PAD_TOP + y * CHAR_H + CHAR_H
        parts.append(f'<text x="{PAD_X}" y="{ty}">{escape(row)}</text>')
    parts.append('</g>')

    # bright layer, masked to the moving sweep gradient
    parts.append(f'<g class="sweep-text" clip-path="url(#gridclip)" mask="url(#sweepMask)">')
    for y, row in enumerate(rows):
        ty = PAD_TOP + y * CHAR_H + CHAR_H
        parts.append(f'<text x="{PAD_X}" y="{ty}">{escape(row)}</text>')
    parts.append('</g>')

    # caption row, matching the other two cards' footer style
    cap_y = PAD_TOP + GRID_PX_H + 26
    parts.append(f'<circle class="dot" cx="{PAD_X+5}" cy="{cap_y-4}" r="4" fill="{DOT_COLOR}"/>')
    parts.append(
        f'<text x="{PAD_X+16}" y="{cap_y}" font-size="12" fill="{CAPTION_COLOR}" '
        f'font-family="{FONT}">rendered in ASCII · @{escape(HANDLE)}</text>'
    )

    parts.append('</svg>')
    with open(out_path, 'w') as f:
        f.write('\n'.join(parts))
    print(f"Wrote {out_path} ({W}x{H})")


if __name__ == '__main__':
    matrix = image_to_matrix('source-prepped.png')
    render_svg(matrix)