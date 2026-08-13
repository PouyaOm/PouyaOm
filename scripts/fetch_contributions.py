import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

username = "PouyaOm"
url = f"https://github.com/users/{username}/contributions"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

days = soup.select('td.ContributionCalendar-day')
data = []
for day in days:
    date = day.get('data-date')
    count = day.get('data-count', '0')
    if date:
        data.append({'date': date, 'count': int(count)})

with open('data/contributions.json', 'w') as f:
    json.dump(data, f)
