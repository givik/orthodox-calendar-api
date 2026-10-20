"""
Command Line Interface (CLI) for Orthodox Liturgical Calendar.
Allows querying dates, today's commemoration, Pascha, and feasts from the terminal.
"""

import sys
import argparse
import json
from datetime import date

from app.core.calendar_service import CalendarService


def main():
    parser = argparse.ArgumentParser(
        description="Orthodox Liturgical Calendar CLI (მართლმადიდებლური კალენდარი)"
    )
    parser.add_argument(
        "query",
        nargs="?",
        default="today",
        help="Date in YYYY-MM-DD format, 'today', 'pascha [year]', or 'feasts [year]'",
    )
    parser.add_argument(
        "year",
        nargs="?",
        type=int,
        default=None,
        help="Year for 'pascha' or 'feasts' command",
    )
    parser.add_argument(
        "--lang",
        choices=["ka", "en", "ru"],
        default="ka",
        help="Language: ka (Georgian), en (English), ru (Russian)",
    )
    parser.add_argument(
        "--calendar",
        choices=["old", "new"],
        default="old",
        help="Calendar style: old (Julian, default) or new (Revised Julian)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON instead of formatted text",
    )

    args = parser.parse_args()
    service = CalendarService()

    # Sub-command: pascha
    if args.query == "pascha":
        year = args.year or date.today().year
        data = service.get_pascha_info(year, lang=args.lang)
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(f"☦️ აღდგომა / Pascha ({year}):")
            print(f"   გრიგორიანული თარიღი: {data['orthodox_pascha']['gregorian_date']}")
            print(f"   ძველი სტილი (Julian): {data['orthodox_pascha']['julian_date']}")
            print("\n📅 მოძრავი დღესასწაულები:")
            for ev in data["movable_cycle_events"]:
                print(f"   • {ev['date']} ({ev['offset']:+3d} დღე): {ev['title']}")
        return

    # Sub-command: feasts
    if args.query == "feasts":
        year = args.year or date.today().year
        data = service.get_year_feasts(year, lang=args.lang, calendar_style=args.calendar)
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(f"☦️ {year} წლის უდიდესი დღესასწაულები ({args.calendar.upper()} კალენდარი):")
            for f in data["feasts"]:
                print(f"   • {f['gregorian_date']} — {f['title']}")
        return

    # Date query: today or YYYY-MM-DD
    if args.query == "today":
        target_date = date.today()
    else:
        try:
            target_date = date.fromisoformat(args.query)
        except ValueError:
            print(f"Error: Invalid date '{args.query}'. Use YYYY-MM-DD, 'today', 'pascha', or 'feasts'.", file=sys.stderr)
            sys.exit(1)

    data = service.get_day(target_date, lang=args.lang, calendar_style=args.calendar)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print("=" * 60)
        print(f"☦️  მართლმადიდებლური კალენდარი | {data['gregorian_date']} ({data['weekday']['name']})")
        print(f"   ძველი სტილით (იულიუსის): {data['julian_date']}")
        print("=" * 60)
        print(f"📖 {data['title']}")
        print("-" * 60)
        print(f"🍽️  მარხვა: {data['fasting']['name']}")
        print(f"    აღწერა: {data['fasting']['description']}")
        print(f"    მიზეზი: {data['fasting']['reason']}")
        print("-" * 60)
        if data["saints"]:
            print("✨ წმინდანთა ხსენება:")
            for s in data["saints"]:
                print(f"   • {s}")
        if data["movable_feast"]:
            print("-" * 60)
            print(f"🕊️ მოძრავი ციკლი: {data['movable_feast']['title']}")
            if data["movable_feast"]["description"]:
                print(f"   {data['movable_feast']['description']}")
        print("=" * 60)


if __name__ == "__main__":
    main()
