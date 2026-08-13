from PIL import Image
import numpy as np

RAMP = " .`:-=+*cs#%@"
img = Image.open('source-prepped.png').convert('L')
w, h = 100, 53
img = img.resize((w, h))
pixels = np.array(img)

svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="400" height="212">']
svg.append('<style>text { font: 4px monospace; fill: #d4d4d4; }</style>')

for y in range(h):
    row = []
    for x in range(w):
        idx = int(pixels[y][x] / 255 * (len(RAMP)-1))
        row.append(RAMP[idx] if idx > 0 else ' ')
    svg.append(f'<text x="0" y="{y*4+4}">{"".join(row)}</text>')

svg.append('</svg>')
with open('avi-ascii.svg', 'w') as f:
    f.write('\n'.join(svg))
