import unittest
import json
from io import BytesIO
from app.server import CalendarAPIHandler


class MockSocket:
    def __init__(self, request_bytes: bytes):
        self.rfile = BytesIO(request_bytes)
        self.wfile = BytesIO()

    def makefile(self, mode, *args, **kwargs):
        if "r" in mode:
            return self.rfile
        return self.wfile

    def sendall(self, data):
        self.wfile.write(data)


class DummyServer:
    server_name = "localhost"
    server_port = 8000


class TestCalendarAPI(unittest.TestCase):
    def _request(self, path: str):
        raw_req = f"GET {path} HTTP/1.1\r\nHost: localhost\r\n\r\n".encode("utf-8")
        sock = MockSocket(raw_req)
        CalendarAPIHandler(sock, ("127.0.0.1", 12345), DummyServer())
        raw_resp = sock.wfile.getvalue().decode("utf-8")

        # Split headers and body
        parts = raw_resp.split("\r\n\r\n", 1)
        headers_part = parts[0]
        body = parts[1] if len(parts) > 1 else ""

        status_line = headers_part.splitlines()[0]
        status_code = int(status_line.split(" ")[1])

        try:
            parsed_json = json.loads(body)
        except Exception:
            parsed_json = None

        return status_code, parsed_json, body

    def test_health_check(self):
        status, data, _ = self._request("/health")
        self.assertEqual(status, 200)
        self.assertEqual(data["status"], "healthy")

    def test_landing_page(self):
        status, _, body = self._request("/")
        self.assertEqual(status, 200)
        self.assertIn("მართლმადიდებლური კალენდრის API", body)

    def test_swagger_docs(self):
        status, _, body = self._request("/docs")
        self.assertEqual(status, 200)
        self.assertIn("swagger-ui", body)

    def test_openapi_json(self):
        status, data, _ = self._request("/openapi.json")
        self.assertEqual(status, 200)
        self.assertEqual(data["openapi"], "3.0.3")

    def test_today_endpoint(self):
        status, data, _ = self._request("/api/v1/today?lang=ka")
        self.assertEqual(status, 200)
        self.assertIn("gregorian_date", data)
        self.assertIn("julian_date", data)
        self.assertIn("fasting", data)

    def test_day_query_endpoint(self):
        status, data, _ = self._request("/api/v1/day?date=2026-10-14&lang=ka")
        self.assertEqual(status, 200)
        self.assertEqual(data["gregorian_date"], "2026-10-14")
        self.assertEqual(data["julian_date"], "2026-10-01")
        self.assertIn("სვეტიცხოვლობა", data["title"])

    def test_day_path_endpoint(self):
        status, data, _ = self._request("/api/v1/day/2026/10/14?lang=en")
        self.assertEqual(status, 200)
        self.assertEqual(data["language"], "en")
        self.assertEqual(data["weekday"]["name"], "Wednesday")

    def test_month_endpoint(self):
        status, data, _ = self._request("/api/v1/month/2026/10?lang=ka")
        self.assertEqual(status, 200)
        self.assertEqual(data["month"], 10)
        self.assertEqual(data["days_count"], 31)
        self.assertEqual(len(data["days"]), 31)

    def test_pascha_endpoint(self):
        status, data, _ = self._request("/api/v1/pascha/2026?lang=ka")
        self.assertEqual(status, 200)
        self.assertEqual(data["orthodox_pascha"]["gregorian_date"], "2026-04-12")
        self.assertTrue(len(data["movable_cycle_events"]) > 20)

    def test_feasts_endpoint(self):
        status, data, _ = self._request("/api/v1/feasts/2026?lang=ka")
        self.assertEqual(status, 200)
        self.assertTrue(data["feasts_count"] > 10)

    def test_feasts_lords_endpoint(self):
        status, data, _ = self._request("/api/v1/feasts/lords/2026?lang=ka")
        self.assertEqual(status, 200)
        self.assertEqual(data["category"], "lords")
        self.assertEqual(data["feasts_count"], 10)
        titles = [f["title"] for f in data["feasts"]]
        self.assertTrue(any("აღდგომა" in t for t in titles))
        self.assertTrue(any("შობა" in t for t in titles))

    def test_invalid_date_error(self):
        status, data, _ = self._request("/api/v1/day?date=invalid-date")
        self.assertEqual(status, 400)
        self.assertIn("error", data)

    def test_not_found(self):
        status, data, _ = self._request("/api/v1/nonexistent")
        self.assertEqual(status, 404)
        self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()
