import unittest
from datetime import date
from app.core.fasting import get_fasting_status


class TestFastingRules(unittest.TestCase):
    def test_bright_week_fast_free(self):
        # In 2026, Pascha is April 12. Bright Monday is April 13, Wednesday April 15, Friday April 17
        bright_wednesday = date(2026, 4, 15)
        res = get_fasting_status(bright_wednesday)
        self.assertFalse(res["is_fast"])
        self.assertEqual(res["fast_type"], "no_fast")
        self.assertEqual(res["reason_code"], "bright_week")

    def test_holy_friday_strict_fast(self):
        # Holy Friday 2026 is April 10
        holy_friday = date(2026, 4, 10)
        res = get_fasting_status(holy_friday)
        self.assertTrue(res["is_fast"])
        self.assertEqual(res["fast_type"], "strict_fast")

    def test_palm_sunday_fish_allowed(self):
        # Palm Sunday 2026 is April 5
        palm_sunday = date(2026, 4, 5)
        res = get_fasting_status(palm_sunday)
        self.assertTrue(res["is_fast"])
        self.assertEqual(res["fast_type"], "fish")

    def test_great_lent_weekday_vs_weekend(self):
        # Clean Monday 2026 is Feb 23 (weekday)
        clean_monday = date(2026, 2, 23)
        res_mon = get_fasting_status(clean_monday)
        self.assertEqual(res_mon["fast_type"], "strict_fast")

        # 1st Sunday of Great Lent (Triumph of Orthodoxy) is March 1 (weekend)
        sunday_orthodoxy = date(2026, 3, 1)
        res_sun = get_fasting_status(sunday_orthodoxy)
        self.assertEqual(res_sun["fast_type"], "wine_oil")

    def test_dormition_fast(self):
        # Dormition Fast: August 1 to 14 Julian -> August 14 to 27 Gregorian
        dorm_day = date(2026, 8, 17) # Monday
        res = get_fasting_status(dorm_day)
        self.assertTrue(res["is_fast"])
        self.assertEqual(res["fast_type"], "strict_fast")

        # Transfiguration (Aug 6 Julian / Aug 19 Gregorian) -> fish allowed
        transfig = date(2026, 8, 19)
        res_trans = get_fasting_status(transfig)
        self.assertEqual(res_trans["fast_type"], "fish")

    def test_svyatki_fast_free(self):
        # Svyatki: Jan 7 to Jan 17 Gregorian (Dec 25 to Jan 4 Julian)
        # Even on Wednesday or Friday, it is fast-free
        svyatki_wed = date(2026, 1, 14) # Wednesday
        res = get_fasting_status(svyatki_wed)
        self.assertFalse(res["is_fast"])
        self.assertEqual(res["fast_type"], "no_fast")

    def test_regular_wed_fri(self):
        # Regular Wednesday outside fast seasons, e.g. Oct 21, 2026 (Wednesday)
        wed = date(2026, 10, 21)
        res = get_fasting_status(wed)
        self.assertTrue(res["is_fast"])
        self.assertEqual(res["reason_code"], "wed_fri_fast")


if __name__ == "__main__":
    unittest.main()
