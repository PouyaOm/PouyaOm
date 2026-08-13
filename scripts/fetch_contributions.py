import re
import json
import requests
from bs4 import BeautifulSoup

USERNAME = "PouyaOm"
URL = f"https://github.com/users/{USERNAME}/contributions"

COUNT_RE = re.compile(r"(\d+|No)\s+contributions?")


def fetch(username: str = USERNAME) -> list[dict]:
    resp = requests.get(
        f"https://github.com/users/{username}/contributions",
        headers={"User-Agent": "Mozilla/5.0 (contribution-card-fetcher)"},
        timeout=15,
    )
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    days = soup.select("td.ContributionCalendar-day, rect.ContributionCalendar-day")
    data = []
    for day in days:
        date = day.get("data-date")
        if not date:
            continue

        level = int(day.get("data-level", 0))

        text = day.get_text(strip=True) or day.get("aria-label", "")
        match = COUNT_RE.search(text)
        if match:
            count = 0 if match.group(1) == "No" else int(match.group(1))
        else:
            count = level

        data.append({"date": date, "count": count, "level": level})

    return data


if __name__ == "__main__":
    data = fetch()
    if not data:
        raise SystemExit(
            "No contribution cells found - GitHub may be rate-limiting "
            "unauthenticated requests, or the markup changed again."
        )
    with open("data/contributions.json", "w") as f:
        json.dump(data, f)
    print(f"Saved {len(data)} days ({sum(d['count'] for d in data)} total contributions)")