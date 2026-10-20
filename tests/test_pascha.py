import unittest
from datetime import date
from app.core.pascha import (
    calculate_orthodox_pascha,
    julian_to_gregorian,
    gregorian_to_julian,
    get_movable_events_for_year,
    get_movable_event,
)


class TestPaschaCalculations(unittest.TestCase):
    def test_canonical_pascha_dates(self):
        # Known historical and future Orthodox Pascha dates (Gregorian)
        expected = {
            2020: (2020, 4, 19),
            2021: (2021, 5, 2),
            2022: (2022, 4, 24),
            2023: (2023, 4, 16),
            2024: (2024, 5, 5),
            2025: (2025, 4, 20),
            2026: (2026, 4, 12),
            2027: (2027, 5, 2),
            2028: (2028, 4, 16),
            2029: (2029, 4, 8),
            2030: (2030, 4, 28),
        }
        for year, (ey, em, ed) in expected.items():
            g_pascha, _ = calculate_orthodox_pascha(year)
            self.assertEqual(g_pascha, date(ey, em, ed), f"Failed for year {year}")

    def test_julian_gregorian_conversion_roundtrip(self):
        # Test 13-day offset in 20th-21st century
        test_dates = [
            date(2026, 1, 7),
            date(2026, 1, 14),
            date(2026, 4, 12),
            date(2026, 10, 14),
            date(2026, 11, 23),
            date(2026, 12, 19),
        ]
        for gd in test_dates:
            jy, jm, jd = gregorian_to_julian(gd)
            back_gd = julian_to_gregorian(jy, jm, jd)
            self.assertEqual(gd, back_gd, f"Roundtrip failed for {gd}")

    def test_movable_events_for_year(self):
        events_2026 = get_movable_events_for_year(2026)
        # Pascha in 2026 is April 12
        pascha_d = date(2026, 4, 12)
        self.assertIn(pascha_d, events_2026)
        self.assertEqual(events_2026[pascha_d]["code"], "pascha")

        # Palm Sunday is April 5 (Pascha - 7)
        self.assertIn(date(2026, 4, 5), events_2026)
        self.assertEqual(events_2026[date(2026, 4, 5)]["code"], "palm_sunday")

        # Ascension is May 21 (Pascha + 39)
        self.assertIn(date(2026, 5, 21), events_2026)
        self.assertEqual(events_2026[date(2026, 5, 21)]["code"], "ascension")

        # Pentecost is May 31 (Pascha + 49)
        self.assertIn(date(2026, 5, 31), events_2026)
        self.assertEqual(events_2026[date(2026, 5, 31)]["code"], "pentecost")

    def test_get_movable_event_on_single_day(self):
        ev = get_movable_event(date(2026, 4, 12))
        self.assertIsNotNone(ev)
        self.assertEqual(ev["code"], "pascha")

        ev_ordinary = get_movable_event(date(2026, 8, 1))
        self.assertIsNone(ev_ordinary)


if __name__ == "__main__":
    unittest.main()
