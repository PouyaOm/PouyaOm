import json
from datetime import datetime, timedelta

with open('data/contributions.json') as f:
    data = json.load(f)

grid = {}
for entry in data:
    grid[entry['date']] = entry

dates = sorted(grid.keys())
if not dates:
    print("No data found!")
    raise SystemExit(1)

start = datetime.strptime(dates[0], '%Y-%m-%d')
end = datetime.strptime(dates[-1], '%Y-%m-%d')
total_days = (end - start).days + 1
weeks = (total_days + start.weekday()) // 7 + 1

# ---- design tokens (matches make_info_card.py) --------------------------
BG = "#0d1117"
BORDER = "#30363d"
TEXT = "#e6edf3"
MUTED = "#7d8590"
DIM = "#484f58"
BLUE = "#58a6ff"
LEVELS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
FONT = "ui-monospace, 'SFMono-Regular', 'SF Mono', Consolas, 'Liberation Mono', Menlo, monospace"

MONTH_ABBR = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
WEEKDAY_LABELS = {0: "Mon", 2: "Wed", 4: "Fri"}  # grid row 0 = Monday ... row 6 = Sunday

CELL = 10
GAP = 3
STEP = CELL + GAP

GRID_X0 = 44
GRID_Y0 = 58
LEGEND_Y = GRID_Y0 + 7 * STEP + 26

W = GRID_X0 + weeks * STEP + 20
H = LEGEND_Y + 24


def level_for(entry: dict) -> int:
    if 'level' in entry:
        return max(0, min(4, int(entry['level'])))
    count = entry.get('count', 0)
    if count <= 0:
        return 0
    if count < 3:
        return 1
    if count < 6:
        return 2
    if count < 10:
        return 3
    return 4


parts = []
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" font-family="{FONT}">'
)
parts.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="6" fill="{BG}" stroke="{BORDER}"/>')

# hunk-header title
x_pad = 24
parts.append(
    f'<text x="{x_pad}" y="28" font-size="12" fill="{MUTED}">'
    f'@@ <tspan fill="{BLUE}">contributions.calendar</tspan> @@</text>'
)
parts.append(f'<line x1="{x_pad}" y1="38" x2="{W-x_pad}" y2="38" stroke="{BORDER}"/>')

# weekday labels
for wd, label in WEEKDAY_LABELS.items():
    ly = GRID_Y0 + wd * STEP + CELL - 2
    parts.append(f'<text x="{GRID_X0-8}" y="{ly}" font-size="9" fill="{DIM}" text-anchor="end">{label}</text>')

# grid + month labels
current = start - timedelta(days=start.weekday())
last_month = None
for week in range(weeks):
    week_start_month = current.month
    if week_start_month != last_month:
        mx = GRID_X0 + week * STEP
        parts.append(f'<text x="{mx}" y="{GRID_Y0-8}" font-size="9" fill="{DIM}">{MONTH_ABBR[week_start_month]}</text>')
        last_month = week_start_month
    for day in range(7):
        date_str = current.strftime('%Y-%m-%d')
        entry = grid.get(date_str)
        level = level_for(entry) if entry else 0
        x = GRID_X0 + week * STEP
        y = GRID_Y0 + day * STEP
        if start <= current <= end:
            parts.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{LEVELS[level]}"/>')
        current += timedelta(days=1)

# total + legend
total = sum(e.get('count', 0) for e in grid.values())
parts.append(
    f'<text x="{x_pad}" y="{LEGEND_Y+16}" font-size="11" fill="{DIM}">'
    f'{total:,} contributions in the last year</text>'
)

legend_x = W - x_pad - (len(LEVELS) * (CELL + 4) + 60)
parts.append(f'<text x="{legend_x}" y="{LEGEND_Y+16}" font-size="9" fill="{DIM}">Less</text>')
for i, color in enumerate(LEVELS):
    lx = legend_x + 26 + i * (CELL + 4)
    parts.append(f'<rect x="{lx}" y="{LEGEND_Y+6}" width="{CELL}" height="{CELL}" rx="2" fill="{color}"/>')
parts.append(f'<text x="{legend_x + 26 + len(LEVELS)*(CELL+4) + 6}" y="{LEGEND_Y+16}" font-size="9" fill="{DIM}">More</text>')

parts.append('</svg>')
with open('contrib-heatmap.svg', 'w') as f:
    f.write('\n'.join(parts))
print(f"Wrote contrib-heatmap.svg ({W}x{H}), {total} total contributions")