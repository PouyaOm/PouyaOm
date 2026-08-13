import json
from datetime import datetime, timedelta
import calendar

with open('data/contributions.json') as f:
    data = json.load(f)

grid = {}
for entry in data:
    grid[entry['date']] = entry['count']

dates = sorted(grid.keys())
if not dates:
    print("No data found!")
    exit()

start = datetime.strptime(dates[0], '%Y-%m-%d')
end = datetime.strptime(dates[-1], '%Y-%m-%d')
total_days = (end - start).days + 1
weeks = (total_days + start.weekday()) // 7 + 1

colors = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="860" height="200">']
svg.append('<style>rect { rx: 3; }</style>')

current = start - timedelta(days=start.weekday())
for week in range(weeks):
    for day in range(7):
        date_str = current.strftime('%Y-%m-%d')
        count = grid.get(date_str, 0)
        level = min(count // 5, 5) if count > 0 else 0
        x = week * 15 + 20
        y = day * 15 + 20
        svg.append(f'<rect x="{x}" y="{y}" width="12" height="12" fill="{colors[level]}"/>')
        current += timedelta(days=1)

total = sum(grid.values())
svg.append(f'<text x="20" y="180" font-family="monospace" font-size="14" fill="#f0e6d0">{total} contributions in the last year</text>')

for i, color in enumerate(colors):
    x = 500 + i * 30
    svg.append(f'<rect x="{x}" y="170" width="12" height="12" fill="{color}"/>')
    if i == 0:
        svg.append(f'<text x="{x+16}" y="182" font-family="monospace" font-size="10" fill="#8b949e">Less</text>')
    elif i == 5:
        svg.append(f'<text x="{x-20}" y="182" font-family="monospace" font-size="10" fill="#8b949e">More</text>')

svg.append('</svg>')
with open('contrib-heatmap.svg', 'w') as f:
    f.write('\n'.join(svg))
