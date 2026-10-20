"""
Example Python client for Orthodox Calendar API (using only standard library).
"""

import urllib.request
import json

def get_day_info(date_str: str = "2026-10-14", lang: str = "ka"):
    url = f"http://localhost:8000/api/v1/day?date={date_str}&lang={lang}"
    req = urllib.request.Request(url, headers={"User-Agent": "OrthodoxClient/1.0"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print(f"☦️ {data['title']}")
        print(f"📅 გრიგორიანული: {data['gregorian_date']} | ძველი სტილი: {data['julian_date']}")
        print(f"🍽️ მარხვა: {data['fasting']['name']} ({data['fasting']['reason']})")
        print("✨ წმინდანები:")
        for s in data["saints"]:
            print(f"   • {s}")
        return data

if __name__ == "__main__":
    get_day_info()
