"""
Calendar Service.
Combines Julian/Gregorian conversions, Paschal movable cycle,
canonical saints and feasts, and fasting rules into structured responses.
"""

from __future__ import annotations
import json
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional

from .pascha import (
    calculate_orthodox_pascha,
    gregorian_to_julian,
    julian_to_gregorian,
    get_movable_event,
    get_movable_events_for_year,
)
from .fasting import get_fasting_status
from app.data.movable_feasts import MOVABLE_FEASTS


# Load full 366-day Julian fixed saints dataset
_DATA_PATH = Path(__file__).parent.parent / "data" / "saints_all.json"
with open(_DATA_PATH, "r", encoding="utf-8") as f:
    SAINTS_DATA: Dict[str, Any] = json.load(f)

WEEKDAYS = {
    "ka": ["ორშაბათი", "სამშაბათი", "ოთხშაბათი", "ხუთშაბათი", "პარასკევი", "შაბათი", "კვირა"],
    "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "ru": ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"],
}

MONTHS_NAMES = {
    "ka": ["იანვარი", "თებერვალი", "მარტი", "აპრილი", "მაისი", "ივნისი", "ივლისი", "აგვისტო", "სექტემბერი", "ოქტომბერი", "ნოემბერი", "დეკემბერი"],
    "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    "ru": ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
}


class CalendarService:
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        self.data = data or SAINTS_DATA

    def get_day(self, target_date: date, lang: str = "ka", calendar_style: str = "old") -> Dict[str, Any]:
        """
        Retrieves complete liturgical information for a specific Gregorian date.
        
        Args:
            target_date: Gregorian date object
            lang: "ka" (Georgian), "en" (English), "ru" (Russian)
            calendar_style: "old" (Julian, default for Georgian & Slavic churches) or "new" (Revised Julian)
        """
        if lang not in ("ka", "en", "ru"):
            lang = "ka"
        if calendar_style not in ("old", "new"):
            calendar_style = "old"

        # 1. Calculate Julian Date
        j_year, j_month, j_day = gregorian_to_julian(target_date)
        julian_date_str = f"{j_year:04d}-{j_month:02d}-{j_day:02d}"

        # 2. Key for fixed feasts
        if calendar_style == "old":
            fixed_key = f"{j_month:02d}-{j_day:02d}"
        else:
            fixed_key = f"{target_date.month:02d}-{target_date.day:02d}"

        fixed_info = self.data.get(fixed_key, {
            "feasts": [],
            "title_ka": "წმინდანთა ხსენება",
            "title_en": "Commemoration of Saints",
            "title_ru": "Память святых",
            "saints_ka": [],
            "saints_en": [],
            "saints_ru": [],
        })

        # 3. Check Movable Cycle Feast
        movable_ev = get_movable_event(target_date)
        movable_info = None
        if movable_ev:
            code = movable_ev["code"]
            m_data = MOVABLE_FEASTS.get(code, {})
            movable_info = {
                "code": code,
                "type": movable_ev["type"],
                "offset_from_pascha": movable_ev["offset"],
                "pascha_gregorian": movable_ev["pascha_date"].isoformat(),
                "title": m_data.get(f"title_{lang}", code),
                "description": m_data.get(f"description_{lang}", ""),
            }

        # 4. Fasting Status
        fasting = get_fasting_status(target_date)
        fasting_resp = {
            "is_fast": fasting["is_fast"],
            "type": fasting["fast_type"],
            "name": fasting[f"name_{lang}"],
            "description": fasting[f"description_{lang}"],
            "reason": fasting[f"reason_{lang}"],
        }

        # 5. Determine Primary Day Title
        fixed_title = fixed_info.get(f"title_{lang}") or fixed_info.get("title_ka", "")
        if movable_info:
            if movable_ev["type"] in ("feast_of_feasts", "holy_week"):
                primary_title = movable_info["title"]
            else:
                if fixed_title:
                    primary_title = f"{movable_info['title']}. {fixed_title}"
                else:
                    primary_title = movable_info["title"]
        else:
            primary_title = fixed_title

        saints_list = fixed_info.get(f"saints_{lang}") or fixed_info.get("saints_ka", [])

        weekday_idx = target_date.weekday()
        weekday_name = WEEKDAYS[lang][weekday_idx]

        return {
            "gregorian_date": target_date.isoformat(),
            "julian_date": julian_date_str,
            "weekday": {
                "index": weekday_idx,
                "name": weekday_name,
            },
            "calendar_style": calendar_style,
            "language": lang,
            "title": primary_title,
            "feasts": fixed_info.get("feasts", []),
            "movable_feast": movable_info,
            "saints": saints_list,
            "fasting": fasting_resp,
        }

    def get_month(self, year: int, month: int, lang: str = "ka", calendar_style: str = "old") -> Dict[str, Any]:
        """Returns liturgical days for an entire month."""
        if lang not in ("ka", "en", "ru"):
            lang = "ka"

        # Determine number of days in month
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)

        days: List[Dict[str, Any]] = []
        curr = start_date
        while curr < end_date:
            days.append(self.get_day(curr, lang=lang, calendar_style=calendar_style))
            curr += timedelta(days=1)

        return {
            "year": year,
            "month": month,
            "month_name": MONTHS_NAMES[lang][month - 1],
            "days_count": len(days),
            "calendar_style": calendar_style,
            "language": lang,
            "days": days,
        }

    def get_pascha_info(self, year: int, lang: str = "ka") -> Dict[str, Any]:
        """Calculates Pascha date and movable cycle details for a given year."""
        if lang not in ("ka", "en", "ru"):
            lang = "ka"

        greg_pascha, (jy, jm, jd) = calculate_orthodox_pascha(year)
        movable_events = get_movable_events_for_year(year)

        events_list = []
        for d, info in sorted(movable_events.items()):
            code = info["code"]
            m_data = MOVABLE_FEASTS.get(code, {})
            events_list.append({
                "date": d.isoformat(),
                "offset": info["offset"],
                "code": code,
                "type": info["type"],
                "title": m_data.get(f"title_{lang}", code),
                "description": m_data.get(f"description_{lang}", ""),
            })

        return {
            "year": year,
            "orthodox_pascha": {
                "gregorian_date": greg_pascha.isoformat(),
                "julian_date": f"{jy:04d}-{jm:02d}-{jd:02d}",
            },
            "movable_cycle_events": events_list,
        }

    def get_year_feasts(self, year: int, lang: str = "ka", calendar_style: str = "old") -> Dict[str, Any]:
        """Lists the Great Feasts and major holidays for a given year."""
        if lang not in ("ka", "en", "ru"):
            lang = "ka"

        # Fixed feasts in Julian dates
        FIXED_GREAT_FEASTS_JULIAN = [
            ("01-01", "circumcision", "ხორციელი წინადაცვეთა უფლისა ჩვენისა. წმ. ბასილი დიდი", "Circumcision of Christ. St. Basil the Great", "Обрезание Господне"),
            ("01-06", "theophany", "ნათლისღება უფლისა (ღმრთისგამოცხადება)", "The Holy Theophany of Christ", "Крещение Господне (Богоявление)"),
            ("01-14", "st_nino", "წმ. ნინოს ხსენება (ნინოობა)", "St. Nino, Enlightener of Georgia", "Равноапостольной Нины Грузии"),
            ("01-26", "david_builder", "წმ. დავით აღმაშენებელი (დავითობა)", "St. David the Builder of Georgia", "Благоверного царя Давида Строителя"),
            ("02-02", "meeting_lord", "მირქმა უფლისა ჩვენისა იესო ქრისტესი", "Meeting of the Lord in the Temple", "Сретение Господне"),
            ("03-25", "annunciation", "ხარება ყოვლადწმიდისა ღვთისმშობლისა", "Annunciation of the Theotokos", "Благовещение Пресвятой Богородицы"),
            ("04-23", "st_george", "წმ. დიდმოწამე გიორგი (გიორგობა)", "Holy Great Martyr George", "Святого великомученика Георгия"),
            ("05-01", "st_tamar", "წმ. თამარ მეფე (თამარობა)", "Holy Queen Tamar of Georgia", "Благоверной царицы Тамары"),
            ("06-24", "nativity_baptist", "შობა წმ. იოანე ნათლისმცემლისა", "Nativity of St. John the Baptist", "Рождество Иоанна Предтечи"),
            ("06-29", "peter_and_paul", "წმ. მოციქულები პეტრე და პავლე (პეტრე-პავლობა)", "Holy Apostles Peter and Paul", "Святых апостолов Петра и Павла"),
            ("07-20", "prophet_elijah", "წმ. ელია წინასწარმეტყველი (ელიაობა) და წმ. ილია მართალი", "Holy Prophet Elijah & St. Ilia the Righteous", "Святого пророка Илии"),
            ("08-06", "transfiguration", "ფერისცვალება უფლისა ჩვენისა იესო ქრისტესი", "Transfiguration of our Lord", "Преображение Господне"),
            ("08-15", "dormition", "მიძინება ყოვლადწმიდისა ღვთისმშობლისა (მარიამობა)", "Dormition of the Theotokos (Mariamoba)", "Успение Пресвятой Богородицы"),
            ("08-29", "beheading_baptist", "იოანე ნათლისმცემლის თავისკვეთა", "Beheading of St. John the Baptist", "Усекновение главы Иоанна Предтечи"),
            ("09-08", "nativity_theotokos", "შობა ყოვლადწმიდისა ღვთისმშობლისა (ღვთისმშობლობა)", "Nativity of the Theotokos", "Рождество Пресвятой Богородицы"),
            ("09-14", "elevation_cross", "ჯვართამაღლება", "Elevation of the Holy Cross", "Воздвижение Креста Господня"),
            ("10-01", "svetitskhovloba", "სვეტიცხოვლობა (მცხეთობა) და საფარველი ღვთისმშობლისა", "Svetitskhovloba (Mtskhetoba) & Pokrov", "Светицховлоба и Покров Богородицы"),
            ("10-31", "hundred_thousand", "ას წამებულთა ხსენება (ასი ათასი ქართველი მოწამე)", "100,000 Holy Martyrs of Tbilisi", "100 000 святых мучеников Тбилисских"),
            ("11-10", "st_george_wheeling", "წმ. გიორგის ბორბალზე წამება (გიორგობა)", "Wheeling of St. George", "Колесование святого великомученика Георгия"),
            ("11-21", "entry_theotokos", "ტაძრად მიყვანება ყოვლადწმიდისა ღვთისმშობლისა", "Entry of the Theotokos into the Temple", "Введение во храм Пресвятой Богородицы"),
            ("11-30", "st_andrew_vakhtang", "წმ. ანდრია პირველწოდებული და წმ. ვახტანგ გორგასალი", "St. Andrew the First-Called & St. Vakhtang Gorgasali", "Апостола Андрея и царя Вахтанга Горгасали"),
            ("12-04", "st_barbara", "წმ. დიდმოწამე ბარბარე (ბარბარობა)", "Holy Great Martyr Barbara", "Святой великомученицы Варвары"),
            ("12-06", "st_nicholas", "წმ. ნიკოლოზ საკვირველთმოქმედი (ნიკოლოზობა)", "St. Nicholas the Wonderworker", "Святителя Николая Чудотворца"),
            ("12-25", "nativity_christ", "შობა უფლისა ჩვენისა იესო ქრისტესი (ქრისტეშობა)", "The Nativity of our Lord Jesus Christ (Christmas)", "Рождество Христово"),
        ]

        feasts_result = []

        # 1. Add Movable Great Feasts
        pascha_info = self.get_pascha_info(year, lang=lang)
        for ev in pascha_info["movable_cycle_events"]:
            if ev["code"] in ("palm_sunday", "pascha", "ascension", "pentecost"):
                feasts_result.append({
                    "type": "movable",
                    "code": ev["code"],
                    "title": ev["title"],
                    "gregorian_date": ev["date"],
                })

        # 2. Add Fixed Great Feasts
        for j_key, code, title_ka, title_en, title_ru in FIXED_GREAT_FEASTS_JULIAN:
            jm, jd = map(int, j_key.split("-"))
            if calendar_style == "old":
                # Convert Julian date to Gregorian date
                g_d = julian_to_gregorian(year, jm, jd)
            else:
                g_d = date(year, jm, jd)

            title_map = {"ka": title_ka, "en": title_en, "ru": title_ru}
            feasts_result.append({
                "type": "fixed",
                "code": code,
                "title": title_map[lang],
                "gregorian_date": g_d.isoformat(),
            })

        # Sort by date
        feasts_result.sort(key=lambda x: x["gregorian_date"])

        return {
            "year": year,
            "calendar_style": calendar_style,
            "language": lang,
            "feasts_count": len(feasts_result),
            "feasts": feasts_result,
        }
