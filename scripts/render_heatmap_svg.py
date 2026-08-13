"""
Generates contrib-heatmap.svg from data/contributions.json.

Palette and type match make_info_card.py. Cells use a warm violet -> pink
-> orange ramp instead of GitHub's green, and pop in on a staggered delay
via CSS so the whole grid animates in once when the image first loads.
Colors each cell from GitHub's own `data-level` (0-4) when present,
falling back to a count-based estimate for older data files that don't
have it.
"""
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

# ---- palette (matches make_info_card.py) ---------------------------------
PANEL_BG = "#0B1120"
BORDER = "rgba(255,255,255,0.10)"
TEXT = "#E5E7EB"
TEXT_MUTED = "rgba(229,231,235,0.55)"
LEVELS = ["rgba(255,255,255,0.05)", "#064E3B", "#047857", "#059669", "#34D399"]
BADGE_BG = "rgba(16,185,129,0.14)"
BADGE_FG = "#6EE7B7"
BADGE_BORDER = "rgba(52,211,153,0.4)"

FONT = ("'Segoe UI Rounded', 'SF Pro Rounded', 'Baloo 2', 'Quicksand', "
        "'Segoe UI', system-ui, -apple-system, sans-serif")

MONTH_ABBR = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
WEEKDAY_LABELS = {0: "Mon", 2: "Wed", 4: "Fri"}  # grid row 0 = Monday ... row 6 = Sunday

CELL = 10
GAP = 4
STEP = CELL + GAP

GRID_X0 = 46
GRID_Y0 = 62
LEGEND_Y = GRID_Y0 + 7 * STEP + 30

W = GRID_X0 + weeks * STEP + 20
H = LEGEND_Y + 26


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
parts.append(f'''
<defs>
  <clipPath id="clip"><rect width="{W}" height="{H}" rx="24"/></clipPath>
</defs>
<style>
  @keyframes pop {{ from {{ opacity: 0; transform: scale(.4); }} to {{ opacity: 1; transform: scale(1); }} }}
  .cell {{ transform-box: fill-box; transform-origin: center; animation: pop .5s ease-out backwards; }}
</style>
<g clip-path="url(#clip)"><rect width="{W}" height="{H}" fill="{PANEL_BG}"/></g>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="24" fill="none" stroke="{BORDER}"/>
''')

x_pad = 26
parts.append(
    f'<text x="{x_pad}" y="34" font-size="17" font-weight="800" fill="{TEXT}">🔥 Contribution streaks</text>'
)

# weekday labels
for wd, label in WEEKDAY_LABELS.items():
    ly = GRID_Y0 + wd * STEP + CELL - 1
    parts.append(f'<text x="{GRID_X0-8}" y="{ly}" font-size="9" fill="{TEXT_MUTED}" text-anchor="end">{label}</text>')

# grid + month labels
current = start - timedelta(days=start.weekday())
last_month = None
week_index = 0
for week in range(weeks):
    week_start_month = current.month
    if week_start_month != last_month:
        mx = GRID_X0 + week * STEP
        parts.append(f'<text x="{mx}" y="{GRID_Y0-10}" font-size="9" fill="{TEXT_MUTED}">{MONTH_ABBR[week_start_month]}</text>')
        last_month = week_start_month
    delay = min(week, 40) * 0.012
    for day in range(7):
        date_str = current.strftime('%Y-%m-%d')
        entry = grid.get(date_str)
        level = level_for(entry) if entry else 0
        x = GRID_X0 + week * STEP
        y = GRID_Y0 + day * STEP
        if start <= current <= end:
            parts.append(
                f'<rect class="cell" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" '
                f'fill="{LEVELS[level]}" style="animation-delay:{delay:.3f}s"/>'
            )
        current += timedelta(days=1)
    week_index += 1

# total badge + legend
total = sum(e.get('count', 0) for e in grid.values())
badge_label = f"{total:,} this year"
badge_w = 20 + len(badge_label) * 7.4
parts.append(
    f'<rect x="{W-x_pad-badge_w:.0f}" y="18" width="{badge_w:.0f}" height="26" rx="13" '
    f'fill="{BADGE_BG}" stroke="{BADGE_BORDER}"/>'
)
parts.append(
    f'<text x="{W-x_pad-badge_w/2:.0f}" y="35" font-size="12" font-weight="700" '
    f'fill="{BADGE_FG}" text-anchor="middle">{badge_label}</text>'
)

legend_grad_id = "legendGrad"
legend_w = 90
legend_x = W - x_pad - legend_w - 34
parts.append(
    f'<text x="{legend_x-6}" y="{LEGEND_Y+16}" font-size="9" fill="{TEXT_MUTED}" text-anchor="end">Less</text>'
)
parts.append(f'''<defs><linearGradient id="{legend_grad_id}" x1="0" y1="0" x2="1" y2="0">
  {''.join(f'<stop offset="{i/(len(LEVELS)-1)*100:.0f}%" stop-color="{c if not c.startswith("rgba") else "#022c22"}"/>' for i, c in enumerate(LEVELS))}
</linearGradient></defs>''')
parts.append(f'<rect x="{legend_x}" y="{LEGEND_Y+6}" width="{legend_w}" height="10" rx="5" fill="url(#{legend_grad_id})"/>')
parts.append(
    f'<text x="{legend_x+legend_w+6}" y="{LEGEND_Y+16}" font-size="9" fill="{TEXT_MUTED}">More</text>'
)

parts.append('</svg>')
with open('contrib-heatmap.svg', 'w') as f:
    f.write('\n'.join(parts))
print(f"Wrote contrib-heatmap.svg ({W}x{H}), {total} total contributions")