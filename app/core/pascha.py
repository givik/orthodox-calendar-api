"""
Orthodox Paschalion & Calendar Calculations.
Computes the date of Orthodox Pascha (Easter) using the Meeus Julian algorithm
and calculates all movable feasts of the liturgical year.
Supports conversions between Julian (Old Style) and Gregorian (New Style) calendars.
"""

from __future__ import annotations
from datetime import date, timedelta
from typing import Dict, Any, List, Tuple


def gregorian_to_jdn(year: int, month: int, day: int) -> int:
    """Converts a Gregorian date to Julian Day Number (JDN)."""
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    return day + ((153 * m + 2) // 5) + 365 * y + (y // 4) - (y // 100) + (y // 400) - 32045


def jdn_to_gregorian(jdn: int) -> Tuple[int, int, int]:
    """Converts a Julian Day Number (JDN) to Gregorian date (year, month, day)."""
    l = jdn + 68569
    n = (4 * l) // 146097
    l = l - (146097 * n + 3) // 4
    i = (4000 * (l + 1)) // 1461001
    l = l - (1461 * i) // 4 + 31
    j = (80 * l) // 2447
    day = l - (2447 * j) // 80
    l = j // 11
    month = j + 2 - (12 * l)
    year = 100 * (n - 49) + i + l
    return year, month, day


def julian_to_jdn(year: int, month: int, day: int) -> int:
    """Converts a Julian (Old Style) date to Julian Day Number (JDN)."""
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    return day + ((153 * m + 2) // 5) + 365 * y + (y // 4) - 32083


def jdn_to_julian(jdn: int) -> Tuple[int, int, int]:
    """Converts a Julian Day Number (JDN) to Julian date (year, month, day)."""
    b = 0
    c = jdn + 32082
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    day = e - (153 * m + 2) // 5 + 1
    month = m + 3 - 12 * (m // 10)
    year = d - 4800 + (m // 10)
    return year, month, day


def julian_to_gregorian(j_year: int, j_month: int, j_day: int) -> date:
    """Converts a Julian date to Gregorian date object."""
    jdn = julian_to_jdn(j_year, j_month, j_day)
    gy, gm, gd = jdn_to_gregorian(jdn)
    return date(gy, gm, gd)


def gregorian_to_julian(g_date: date) -> Tuple[int, int, int]:
    """Converts a Gregorian date object to Julian date tuple (year, month, day)."""
    jdn = gregorian_to_jdn(g_date.year, g_date.month, g_date.day)
    return jdn_to_julian(jdn)


def calculate_orthodox_pascha(year: int) -> Tuple[date, Tuple[int, int, int]]:
    """
    Computes Orthodox Pascha (Easter) for a given Gregorian year.
    Returns:
        (gregorian_pascha_date, (julian_year, julian_month, julian_day))
    Uses Meeus' Julian algorithm.
    """
    a = year % 4
    b = year % 7
    c = year % 19
    d = (19 * c + 15) % 30
    e = (2 * a + 4 * b - d + 34) % 7
    julian_month = (d + e + 114) // 31
    julian_day = ((d + e + 114) % 31) + 1
    julian_year = year

    gregorian_pascha = julian_to_gregorian(julian_year, julian_month, julian_day)
    return gregorian_pascha, (julian_year, julian_month, julian_day)


# Relative offset of movable days from Pascha (0 = Pascha Sunday)
MOVABLE_CYCLE_OFFSETS: Dict[int, Dict[str, Any]] = {
    -70: {"code": "triodion_begins", "type": "sunday"},      # Sunday of Publican and Pharisee
    -63: {"code": "prodigal_son", "type": "sunday"},          # Sunday of Prodigal Son
    -56: {"code": "meatfare_sunday", "type": "sunday"},       # Sunday of Last Judgment (Meatfare)
    -55: {"code": "cheesefare_week_begins", "type": "fast"},  # Cheesefare week begins (no meat, dairy ok)
    -49: {"code": "forgiveness_sunday", "type": "sunday"},    # Cheesefare / Forgiveness Sunday
    -48: {"code": "clean_monday", "type": "fast_start"},      # Beginning of Great Lent (Clean Monday)
    -42: {"code": "sunday_orthodoxy", "type": "sunday"},      # 1st Sunday of Great Lent (Triumph of Orthodoxy)
    -35: {"code": "sunday_palamas", "type": "sunday"},        # 2nd Sunday of Great Lent (St. Gregory Palamas)
    -28: {"code": "sunday_cross", "type": "sunday"},          # 3rd Sunday of Great Lent (Veneration of the Cross)
    -21: {"code": "sunday_climacus", "type": "sunday"},       # 4th Sunday of Great Lent (St. John Climacus)
    -14: {"code": "sunday_mary_egypt", "type": "sunday"},     # 5th Sunday of Great Lent (St. Mary of Egypt)
    -8:  {"code": "lazarus_saturday", "type": "feast"},       # Lazarus Saturday
    -7:  {"code": "palm_sunday", "type": "twelve_feast"},     # Entry of the Lord into Jerusalem (Palm Sunday)
    -6:  {"code": "holy_monday", "type": "holy_week"},
    -5:  {"code": "holy_tuesday", "type": "holy_week"},
    -4:  {"code": "holy_wednesday", "type": "holy_week"},
    -3:  {"code": "holy_thursday", "type": "holy_week"},
    -2:  {"code": "holy_friday", "type": "holy_week"},        # Great and Holy Friday (Crucifixion)
    -1:  {"code": "holy_saturday", "type": "holy_week"},
    0:   {"code": "pascha", "type": "feast_of_feasts"},       # Bright Resurrection of Christ (Pascha)
    1:   {"code": "bright_monday", "type": "bright_week"},
    2:   {"code": "bright_tuesday", "type": "bright_week"},
    3:   {"code": "bright_wednesday", "type": "bright_week"},
    4:   {"code": "bright_thursday", "type": "bright_week"},
    5:   {"code": "bright_friday", "type": "bright_week"},
    6:   {"code": "bright_saturday", "type": "bright_week"},
    7:   {"code": "thomas_sunday", "type": "sunday"},         # Thomas Sunday (Antipascha)
    39:  {"code": "ascension", "type": "twelve_feast"},       # Ascension of the Lord (Thursday)
    49:  {"code": "pentecost", "type": "twelve_feast"},       # Pentecost / Holy Trinity (Sunday)
    50:  {"code": "holy_spirit_day", "type": "feast"},        # Day of the Holy Spirit (Monday)
    56:  {"code": "all_saints_sunday", "type": "sunday"},     # All Saints Sunday
    57:  {"code": "apostles_fast_begins", "type": "fast_start"}, # Apostles' Fast starts Monday
}


def get_movable_events_for_year(year: int) -> Dict[date, Dict[str, Any]]:
    """Calculates all movable events for the year keyed by Gregorian date."""
    pascha_gregorian, _ = calculate_orthodox_pascha(year)
    events: Dict[date, Dict[str, Any]] = {}
    for offset, info in MOVABLE_CYCLE_OFFSETS.items():
        ev_date = pascha_gregorian + timedelta(days=offset)
        events[ev_date] = {
            "offset": offset,
            "code": info["code"],
            "type": info["type"],
            "pascha_date": pascha_gregorian,
        }
    return events


def get_movable_event(d: date) -> Dict[str, Any] | None:
    """Checks if a given Gregorian date is a movable cycle event."""
    pascha_this_year, _ = calculate_orthodox_pascha(d.year)
    offset = (d - pascha_this_year).days
    if offset in MOVABLE_CYCLE_OFFSETS:
        info = MOVABLE_CYCLE_OFFSETS[offset]
        return {
            "offset": offset,
            "code": info["code"],
            "type": info["type"],
            "pascha_date": pascha_this_year,
        }
    # Check if late in the previous year or early next year in edge cases
    if d.month == 1:
        pascha_prev, _ = calculate_orthodox_pascha(d.year - 1)
        offset_prev = (d - pascha_prev).days
        if offset_prev in MOVABLE_CYCLE_OFFSETS:
            info = MOVABLE_CYCLE_OFFSETS[offset_prev]
            return {
                "offset": offset_prev,
                "code": info["code"],
                "type": info["type"],
                "pascha_date": pascha_prev,
            }
    return None
