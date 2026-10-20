"""
Generates a static API structure in `dist/` that can be hosted on GitHub Pages,
Cloudflare Pages, Vercel, or any static CDN with 0 server requirements.
"""

import json
from pathlib import Path
from datetime import date, timedelta
from app.core.pascha import gregorian_to_julian, julian_to_gregorian

DATA_PATH = Path(__file__).parent.parent / "data" / "saints_all.json"
with open(DATA_PATH, "r", encoding="utf-8") as f:
    SAINTS_DATA = json.load(f)

DIST_DIR = Path(__file__).parent.parent.parent / "dist"

def generate():
    print("Building static API in dist/...")
    
    # Create directories
    for lang in ("ka", "en", "ru"):
        (DIST_DIR / "api" / lang).mkdir(parents=True, exist_ok=True)
        (DIST_DIR / "api" / "julian" / lang).mkdir(parents=True, exist_ok=True)
    (DIST_DIR / "api" / "day").mkdir(parents=True, exist_ok=True)

    # 1. Generate Julian-based files (366 days)
    julian_all = {"ka": {}, "en": {}, "ru": {}}
    for j_key, val in SAINTS_DATA.items():
        jm, jd = map(int, j_key.split("-"))
        for lang in ("ka", "en", "ru"):
            day_obj = {
                "julian_day": j_key,
                "title": val.get(f"title_{lang}") or val.get("title_ka", ""),
                "feasts": val.get("feasts", []),
                "saints": val.get(f"saints_{lang}") or val.get("saints_ka", []),
            }
            julian_all[lang][j_key] = day_obj
            with open(DIST_DIR / "api" / "julian" / lang / f"{j_key}.json", "w", encoding="utf-8") as f:
                json.dump(day_obj, f, ensure_ascii=False, indent=2)

    # 2. Generate Gregorian civil day files (Standard 365/366 civil calendar year mapping)
    # Using a leap year (e.g. 2024 or 2028) to cover all 366 days (including Feb 29)
    gregorian_all = {"ka": {}, "en": {}, "ru": {}}
    gregorian_combined_all = {}

    start_date = date(2024, 1, 1)
    for day_idx in range(366):
        curr_date = start_date + timedelta(days=day_idx)
        g_key = f"{curr_date.month:02d}-{curr_date.day:02d}"
        
        # Calculate Julian date for this civil Gregorian date (+13 days offset in 1900-2099)
        jy, jm, jd = gregorian_to_julian(curr_date)
        j_key = f"{jm:02d}-{jd:02d}"
        raw_val = SAINTS_DATA.get(j_key, {})

        multi_lang_day = {
            "gregorian_day": g_key,
            "julian_day": j_key,
            "feasts": raw_val.get("feasts", []),
            "ka": {
                "title": raw_val.get("title_ka", ""),
                "saints": raw_val.get("saints_ka", []),
            },
            "en": {
                "title": raw_val.get("title_en", ""),
                "saints": raw_val.get("saints_en", []),
            },
            "ru": {
                "title": raw_val.get("title_ru", ""),
                "saints": raw_val.get("saints_ru", []),
            }
        }
        gregorian_combined_all[g_key] = multi_lang_day

        with open(DIST_DIR / "api" / "day" / f"{g_key}.json", "w", encoding="utf-8") as f:
            json.dump(multi_lang_day, f, ensure_ascii=False, indent=2)

        for lang in ("ka", "en", "ru"):
            lang_obj = {
                "gregorian_day": g_key,
                "julian_day": j_key,
                "title": raw_val.get(f"title_{lang}") or raw_val.get("title_ka", ""),
                "feasts": raw_val.get("feasts", []),
                "saints": raw_val.get(f"saints_{lang}") or raw_val.get("saints_ka", []),
            }
            gregorian_all[lang][g_key] = lang_obj
            with open(DIST_DIR / "api" / lang / f"{g_key}.json", "w", encoding="utf-8") as f:
                json.dump(lang_obj, f, ensure_ascii=False, indent=2)

    # 3. Save bundled full-year JSON files
    for lang in ("ka", "en", "ru"):
        with open(DIST_DIR / "api" / lang / "all.json", "w", encoding="utf-8") as f:
            json.dump(gregorian_all[lang], f, ensure_ascii=False, indent=2)
        with open(DIST_DIR / "api" / "julian" / lang / "all.json", "w", encoding="utf-8") as f:
            json.dump(julian_all[lang], f, ensure_ascii=False, indent=2)

    with open(DIST_DIR / "api" / "all.json", "w", encoding="utf-8") as f:
        json.dump(gregorian_combined_all, f, ensure_ascii=False, indent=2)

    # 4. Generate Feast Category Files (საუფლო, საღვთისმშობლო, წმინდანთა)
    from app.core.calendar_service import CalendarService
    svc = CalendarService()
    feasts_dir = DIST_DIR / "api" / "feasts"
    feasts_dir.mkdir(parents=True, exist_ok=True)

    # Default year: current civil year
    current_year = date.today().year

    for cat in ("lords", "theotokos", "saints"):
        cat_data = {}
        for lang in ("ka", "en", "ru"):
            res = svc.get_year_feasts(current_year, lang=lang, category=cat)
            cat_data[lang] = res
            with open(DIST_DIR / "api" / lang / f"feasts_{cat}.json", "w", encoding="utf-8") as f:
                json.dump(res, f, ensure_ascii=False, indent=2)
        with open(feasts_dir / f"{cat}.json", "w", encoding="utf-8") as f:
            json.dump(cat_data, f, ensure_ascii=False, indent=2)

    all_feasts_data = {}
    for lang in ("ka", "en", "ru"):
        all_feasts_data[lang] = svc.get_year_feasts(current_year, lang=lang)
    with open(feasts_dir / "all.json", "w", encoding="utf-8") as f:
        json.dump(all_feasts_data, f, ensure_ascii=False, indent=2)

    print("Static JSON files generated successfully!")

if __name__ == "__main__":
    generate()
