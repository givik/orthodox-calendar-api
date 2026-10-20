import unittest
from datetime import date
from app.core.calendar_service import CalendarService


class TestCalendarService(unittest.TestCase):
    def setUp(self):
        self.service = CalendarService()

    def test_svetitskhovloba_georgian(self):
        # Svetitskhovloba: Oct 14 Gregorian (Oct 1 Julian)
        day = self.service.get_day(date(2026, 10, 14), lang="ka")
        self.assertEqual(day["julian_date"], "2026-10-01")
        self.assertIn("სვეტიცხოვლობა", day["title"])
        self.assertIn("საფარველი", day["title"])
        self.assertEqual(day["language"], "ka")
        self.assertTrue(len(day["saints"]) > 0)

    def test_multilingual_titles(self):
        # Nativity of Christ: Jan 7 Gregorian
        d = date(2026, 1, 7)
        ka = self.service.get_day(d, lang="ka")
        en = self.service.get_day(d, lang="en")
        ru = self.service.get_day(d, lang="ru")

        self.assertIn("შობა", ka["title"])
        self.assertIn("Nativity", en["title"])
        self.assertIn("Рождество", ru["title"])

        self.assertEqual(ka["weekday"]["name"], "ოთხშაბათი")
        self.assertEqual(en["weekday"]["name"], "Wednesday")
        self.assertEqual(ru["weekday"]["name"], "Среда")

    def test_st_george_day(self):
        # St. George's Wheeling: Nov 23 Gregorian (Nov 10 Julian)
        d = date(2026, 11, 23)
        day = self.service.get_day(d, lang="ka")
        self.assertEqual(day["julian_date"], "2026-11-10")
        self.assertIn("გიორგი", day["title"])

    def test_st_nino_day(self):
        # St. Nino's day: Jan 27 Gregorian (Jan 14 Julian)
        d = date(2026, 1, 27)
        day = self.service.get_day(d, lang="ka")
        self.assertEqual(day["julian_date"], "2026-01-14")
        self.assertIn("ნინო", day["title"])

    def test_st_david_the_builder(self):
        # St. David the Builder: Feb 8 Gregorian (Jan 26 Julian)
        d = date(2026, 2, 8)
        day = self.service.get_day(d, lang="ka")
        self.assertEqual(day["julian_date"], "2026-01-26")
        self.assertIn("დავით აღმაშენებელი", day["title"])

    def test_month_overview(self):
        m = self.service.get_month(2026, 10, lang="ka")
        self.assertEqual(m["year"], 2026)
        self.assertEqual(m["month"], 10)
        self.assertEqual(m["month_name"], "ოქტომბერი")
        self.assertEqual(m["days_count"], 31)
        self.assertEqual(len(m["days"]), 31)

    def test_year_feasts(self):
        feasts = self.service.get_year_feasts(2026, lang="ka")
        self.assertGreater(feasts["feasts_count"], 15)
        codes = [f["code"] for f in feasts["feasts"]]
        self.assertIn("pascha", codes)
        self.assertIn("nativity_christ", codes)
        self.assertIn("svetitskhovloba", codes)
        self.assertIn("st_george", codes)

    def test_dominical_feasts_lords(self):
        lords = self.service.get_dominical_feasts(2026, lang="ka")
        self.assertEqual(lords["category"], "lords")
        self.assertEqual(lords["feasts_count"], 10)
        codes = [f["code"] for f in lords["feasts"]]
        self.assertIn("pascha", codes)
        self.assertIn("nativity_christ", codes)
        self.assertIn("theophany", codes)
        self.assertIn("transfiguration", codes)
        self.assertIn("elevation_cross", codes)
        self.assertIn("ascension", codes)
        self.assertIn("pentecost", codes)
        self.assertIn("palm_sunday", codes)

    def test_theotokos_feasts(self):
        marian = self.service.get_theotokos_feasts(2026, lang="ka")
        self.assertEqual(marian["category"], "theotokos")
        codes = [f["code"] for f in marian["feasts"]]
        self.assertIn("dormition", codes)
        self.assertIn("nativity_theotokos", codes)
        self.assertIn("annunciation", codes)


if __name__ == "__main__":
    unittest.main()
