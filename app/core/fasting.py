"""
Orthodox Fasting Rules Engine.
Determines the fasting level, reason, and allowed foods for any calendar day.
"""

from __future__ import annotations
from datetime import date, timedelta
from typing import Dict, Any, Tuple
from .pascha import calculate_orthodox_pascha, gregorian_to_julian


FAST_TYPES = {
    "no_fast": {
        "ka": "ხსნილი",
        "en": "Fast-free",
        "ru": "Сплошная / Поста нет",
        "description_ka": "ყველა საჭმელი ნებადართულია",
        "description_en": "All food allowed",
        "description_ru": "Разрешается любая пища",
    },
    "wine_oil": {
        "ka": "მარხვა (ზეთითა და ღვინით)",
        "en": "Fast: Wine & Oil allowed",
        "ru": "Пост с вином и елеем",
        "description_ka": "ნებადართულია მცენარეული ზეთი და ღვინო",
        "description_en": "Wine and vegetable oil allowed; no meat, dairy, eggs or fish",
        "description_ru": "Разрешается вино и елей; мясо, молочные продукты, яйца и рыба запрещены",
    },
    "fish": {
        "ka": "მარხვა (თევზით ხსნილი)",
        "en": "Fast: Fish allowed",
        "ru": "Пост с рыбой",
        "description_ka": "ნებადართულია თევზი, ზეთი და ღვინო",
        "description_en": "Fish, wine and oil allowed; no meat, dairy or eggs",
        "description_ru": "Разрешается рыба, вино и елей; мясо, молоко и яйца запрещены",
    },
    "dairy_allowed": {
        "ka": "ყველიერი (ხორცის გარეშე)",
        "en": "Cheesefare: Dairy & Fish allowed",
        "ru": "Сырная седмица (без мяса)",
        "description_ka": "ხორცი აკრძალულია; ნებადართულია რძის ნაწარმი, კვერცხი და თევზი",
        "description_en": "Meat is forbidden; dairy, eggs and fish allowed",
        "description_ru": "Мясо запрещено; разрешены молочные продукты, яйца и рыба",
    },
    "strict_fast": {
        "ka": "მკაცრი მარხვა (უზეთო)",
        "en": "Strict Fast (No oil)",
        "ru": "Строгий пост (без масла)",
        "description_ka": "მცენარეული საკვები ზეთისა და ღვინის გარეშე (მშრალი კვება)",
        "description_en": "Strict plant-based fast without wine or oil (xerophagy)",
        "description_ru": "Сухоядение или вареная пища без масла и вина",
    },
}


def get_fasting_status(g_date: date, major_feasts: set[str] | None = None) -> Dict[str, Any]:
    """
    Computes the fasting status for a given Gregorian date under Julian liturgical tradition.
    """
    weekday = g_date.weekday()  # Monday is 0, Sunday is 6, Wed is 2, Fri is 4
    j_year, j_month, j_day = gregorian_to_julian(g_date)
    pascha_this_year, _ = calculate_orthodox_pascha(g_date.year)
    offset = (g_date - pascha_this_year).days

    # Check previous/next year pascha boundary if needed
    if g_date.month == 1:
        pascha_prev, _ = calculate_orthodox_pascha(g_date.year - 1)
        offset_prev = (g_date - pascha_prev).days
    else:
        offset_prev = -999

    # 1. Fast-free weeks (Сплошные седмицы / ხსნილი შვიდეულები)
    # Bright Week (Pascha to Pascha + 6)
    if 0 <= offset <= 6:
        return _make_result("no_fast", "bright_week", "ბრწყინვალე შვიდეული (ხსნილი)", "Bright Week (Fast-free)", "Светлая седмица")

    # Trinity Week (Pascha + 50 to Pascha + 56)
    if 50 <= offset <= 56:
        return _make_result("no_fast", "trinity_week", "სულთმოფენობის შვიდეული (ხსნილი)", "Trinity Week (Fast-free)", "Троицкая седмица")

    # Week of Publican and Pharisee (Pascha - 69 to Pascha - 63)
    if -69 <= offset <= -63:
        return _make_result("no_fast", "publican_pharisee", "მეზვერისა და ფარისევლის შვიდეული (ხსნილი)", "Publican & Pharisee Week (Fast-free)", "Седмица о мытаре и фарисее")

    # Svyatki (Christmas to Theophany Eve: Dec 25 to Jan 4 Julian)
    if (j_month == 12 and j_day >= 25) or (j_month == 1 and j_day <= 4):
        return _make_result("no_fast", "svyatki", "შობის შემდგომი დღეები / ნათლისღებამდე (ხსნილი)", "Post-Feast of Nativity (Fast-free)", "Святки")

    # 2. Cheesefare Week (Pascha - 55 to Pascha - 49)
    if -55 <= offset <= -49:
        return _make_result("dairy_allowed", "cheesefare", "ყველიერის შვიდეული", "Cheesefare Week", "Сырная седмица (Масленица)")

    # 3. Single-day strict fasts (Julian calendar dates)
    # Eve of Theophany (Jan 5 Julian)
    if j_month == 1 and j_day == 5:
        return _make_result("strict_fast", "theophany_eve", "ნათლისღების წინა დღე (მკაცრი მარხვა)", "Eve of Theophany (Strict Fast)", "Навечерие Богоявления")
    # Beheading of St. John the Baptist (Aug 29 Julian)
    if j_month == 8 and j_day == 29:
        return _make_result("strict_fast", "beheading_baptist", "იოანე ნათლისმცემლის თავისკვეთა (მკაცრი მარხვა)", "Beheading of St. John the Baptist", "Усекновение главы Иоанна Предтечи")
    # Elevation of the Holy Cross (Sept 14 Julian)
    if j_month == 9 and j_day == 14:
        return _make_result("strict_fast", "elevation_cross", "ჯვართამაღლება (მკაცრი მარხვა)", "Elevation of the Holy Cross", "Воздвижение Креста Господня")

    # 4. Great Lent and Holy Week (Pascha - 48 to Pascha - 1)
    if -48 <= offset <= -1:
        # Palm Sunday (Pascha - 7)
        if offset == -7:
            return _make_result("fish", "palm_sunday", "ბზობა (თევზით ხსნილი)", "Palm Sunday (Fish allowed)", "Вход Господень в Иерусалим (Рыба)")
        # Lazarus Saturday (Pascha - 8)
        if offset == -8:
            return _make_result("wine_oil", "lazarus_saturday", "ლაზარეს შაბათი (ზეთითა და ღვინით)", "Lazarus Saturday (Caviar/Wine/Oil)", "Лазарева суббота")
        # Annunciation (March 25 Julian) during Great Lent
        if j_month == 3 and j_day == 25:
            if offset < -6:  # Not during Holy Week
                return _make_result("fish", "annunciation_lent", "ხარება (თევზით ხსნილი)", "Annunciation (Fish allowed)", "Благовещение (Рыба)")
            else:
                return _make_result("wine_oil", "annunciation_holy_week", "ხარება ვნების კვირაში (ზეთითა და ღვინით)", "Annunciation in Holy Week", "Благовещение на Страстной")
        # Holy Friday (Pascha - 2) & Holy Saturday (Pascha - 1)
        if offset == -2:
            return _make_result("strict_fast", "holy_friday", "დიდი პარასკევი (მკაცრი მარხვა)", "Great and Holy Friday (Strict Fast)", "Великая Пятница")
        # Weekend in Great Lent
        if weekday in (5, 6):
            return _make_result("wine_oil", "great_lent_weekend", "დიდმარხვის შაბათი/კვირა (ზეთითა და ღვინით)", "Great Lent Weekend (Wine & Oil)", "Великий пост (Суббота/Воскресенье)")
        return _make_result("strict_fast", "great_lent_weekday", "დიდმარხვა (მკაცრი მარხვა / უზეთო)", "Great Lent Weekday (Strict Fast)", "Великий пост")

    # 5. Dormition Fast (August 1 to 14 Julian)
    if j_month == 8 and 1 <= j_day <= 14:
        # Transfiguration (Aug 6 Julian)
        if j_day == 6:
            return _make_result("fish", "transfiguration", "ფერისცვალება (თევზით ხსნილი)", "Transfiguration (Fish allowed)", "Преображение Господне (Рыба)")
        if weekday in (5, 6):
            return _make_result("wine_oil", "dormition_fast_weekend", "მარიამობის მარხვა (ზეთითა და ღვინით)", "Dormition Fast Weekend (Wine & Oil)", "Успенский пост (Суббота/Воскресенье)")
        return _make_result("strict_fast", "dormition_fast_weekday", "მარიამობის მარხვა (უზეთო)", "Dormition Fast Weekday (Strict Fast)", "Успенский пост")

    # 6. Apostles' Fast (From Pascha + 57 until July 11 Julian)
    # Apostles' Fast starts on Monday after All Saints Sunday
    apostles_fast_end = (7, 11)  # July 11 Julian
    is_apostles_fast = False
    if offset >= 57:
        if j_month < 7 or (j_month == 7 and j_day <= 11):
            is_apostles_fast = True
    if is_apostles_fast:
        if weekday in (5, 6):  # Sat, Sun: Fish allowed
            return _make_result("fish", "apostles_fast_weekend", "პეტრე-პავლობის მარხვა (თევზით ხსნილი)", "Apostles' Fast Weekend (Fish allowed)", "Петров пост (Рыба)")
        elif weekday in (1, 3):  # Tue, Thu: Wine & Oil / Fish if feast
            return _make_result("wine_oil", "apostles_fast_weekday", "პეტრე-პავლობის მარხვა (ზეთითა და ღვინით)", "Apostles' Fast (Wine & Oil)", "Петров пост (Вино и елей)")
        else:  # Mon, Wed, Fri
            return _make_result("strict_fast", "apostles_fast_wed_fri", "პეტრე-პავლობის მარხვა (უზეთო / მკაცრი)", "Apostles' Fast (Strict Fast)", "Петров пост (Без масла)")

    # 7. Nativity Fast (Nov 15 to Dec 24 Julian)
    is_nativity_fast = (j_month == 11 and j_day >= 15) or (j_month == 12 and j_day <= 24)
    if is_nativity_fast:
        # Paramon / Nativity Eve (Dec 24 Julian)
        if j_month == 12 and j_day == 24:
            return _make_result("strict_fast", "nativity_eve", "შობის წინა დღე (მკაცრი მარხვა)", "Eve of the Nativity (Paramon)", "Рождественский сочельник")
        # Entry of the Theotokos (Nov 21 Julian)
        if j_month == 11 and j_day == 21:
            return _make_result("fish", "entry_theotokos", "ტაძრად მიყვანება (თევზით ხსნილი)", "Entry of the Theotokos (Fish allowed)", "Введение во храм (Рыба)")
        # St. Nicholas (Dec 6 Julian)
        if j_month == 12 and j_day == 6:
            return _make_result("fish", "st_nicholas", "წმ. ნიკოლოზის ხსენება (თევზით ხსნილი)", "St. Nicholas Feast (Fish allowed)", "Святителя Николая (Рыба)")
        # Before Dec 19 Julian: fish allowed on Sat/Sun
        if (j_month == 11) or (j_month == 12 and j_day < 20):
            if weekday in (5, 6):
                return _make_result("fish", "nativity_fast_weekend", "საშობაო მარხვა (თევზით ხსნილი)", "Nativity Fast Weekend (Fish allowed)", "Рождественский пост (Рыба)")
            elif weekday in (1, 3):  # Tue, Thu
                return _make_result("wine_oil", "nativity_fast_weekday", "საშობაო მარხვა (ზეთითა და ღვინით)", "Nativity Fast (Wine & Oil)", "Рождественский пост (Вино и елей)")
            else:  # Wed, Fri
                return _make_result("strict_fast", "nativity_fast_wed_fri", "საშობაო მარხვა (უზეთო)", "Nativity Fast (No Oil)", "Рождественский пост (Без масла)")
        else:
            # Last days of Nativity Fast (Dec 20 - 23 Julian)
            if weekday in (5, 6):
                return _make_result("wine_oil", "nativity_fast_strict_weekend", "საშობაო მარხვა (ზეთითა და ღვინით)", "Nativity Fast (Wine & Oil)", "Рождественский пост (Вино и елей)")
            return _make_result("strict_fast", "nativity_fast_strict", "საშობაო მარხვა (უზეთო)", "Nativity Fast (Strict Fast)", "Рождественский пост")

    # 8. Regular Wednesdays and Fridays outside fasting seasons
    if weekday in (2, 4):  # Wednesday (2) and Friday (4)
        # Check major feast exceptions
        return _make_result("wine_oil", "wed_fri_fast", "ოთხშაბათისა და პარასკევის მარხვა", "Wednesday/Friday Fast (Wine & Oil)", "Пост в среду и пятницу")

    # 9. Regular day (no fast)
    return _make_result("no_fast", "ordinary_day", "ხსნილი", "No fast (All foods allowed)", "Поста нет (Все разрешено)")


def _make_result(fast_type: str, reason_code: str, reason_ka: str, reason_en: str, reason_ru: str) -> Dict[str, Any]:
    info = FAST_TYPES.get(fast_type, FAST_TYPES["no_fast"])
    return {
        "is_fast": fast_type != "no_fast",
        "fast_type": fast_type,
        "name_ka": info["ka"],
        "name_en": info["en"],
        "name_ru": info["ru"],
        "description_ka": info["description_ka"],
        "description_en": info["description_en"],
        "description_ru": info["description_ru"],
        "reason_code": reason_code,
        "reason_ka": reason_ka,
        "reason_en": reason_en,
        "reason_ru": reason_ru,
    }
