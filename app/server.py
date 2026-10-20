"""
Orthodox Liturgical Calendar REST API Server.
Zero-dependency, pure Python standard library HTTP server.
Includes CORS, JSON responses, query parsing, and built-in interactive Swagger UI docs.
"""

from __future__ import annotations
import json
import re
from datetime import date
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Tuple, Dict, Any, Optional

from app.core.calendar_service import CalendarService


service = CalendarService()

OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "Orthodox Liturgical Calendar API (მართლმადიდებლური კალენდრის API)",
        "version": "1.0.0",
        "description": "Multilingual Orthodox Liturgical Calendar API supporting Georgian (ka), English (en), and Russian (ru). Provides Julian (Old Style) and Revised Julian (New Style) calculations, Paschal cycle, fasting rules, and saints commemorations.",
        "contact": {
            "name": "Orthodox Calendar API Project",
        },
        "license": {
            "name": "MIT",
        }
    },
    "paths": {
        "/api/v1/today": {
            "get": {
                "summary": "Get today's liturgical info",
                "parameters": [
                    {"name": "lang", "in": "query", "schema": {"type": "string", "enum": ["ka", "en", "ru"], "default": "ka"}},
                    {"name": "calendar", "in": "query", "schema": {"type": "string", "enum": ["old", "new"], "default": "old"}}
                ],
                "responses": {"200": {"description": "Today's commemorations, feasts, and fasting rules"}}
            }
        },
        "/api/v1/day": {
            "get": {
                "summary": "Get liturgical info for a specific date (via query param)",
                "parameters": [
                    {"name": "date", "in": "query", "required": True, "schema": {"type": "string", "example": "2026-10-14"}},
                    {"name": "lang", "in": "query", "schema": {"type": "string", "enum": ["ka", "en", "ru"], "default": "ka"}},
                    {"name": "calendar", "in": "query", "schema": {"type": "string", "enum": ["old", "new"], "default": "old"}}
                ],
                "responses": {"200": {"description": "Day commemorations, feasts, and fasting rules"}}
            }
        },
        "/api/v1/day/{year}/{month}/{day}": {
            "get": {
                "summary": "Get liturgical info for a specific date (via path)",
                "parameters": [
                    {"name": "year", "in": "path", "required": True, "schema": {"type": "integer", "example": 2026}},
                    {"name": "month", "in": "path", "required": True, "schema": {"type": "integer", "example": 10}},
                    {"name": "day", "in": "path", "required": True, "schema": {"type": "integer", "example": 14}},
                    {"name": "lang", "in": "query", "schema": {"type": "string", "enum": ["ka", "en", "ru"], "default": "ka"}},
                    {"name": "calendar", "in": "query", "schema": {"type": "string", "enum": ["old", "new"], "default": "old"}}
                ],
                "responses": {"200": {"description": "Day commemorations, feasts, and fasting rules"}}
            }
        },
        "/api/v1/month/{year}/{month}": {
            "get": {
                "summary": "Get liturgical info for an entire month",
                "parameters": [
                    {"name": "year", "in": "path", "required": True, "schema": {"type": "integer", "example": 2026}},
                    {"name": "month", "in": "path", "required": True, "schema": {"type": "integer", "example": 10}},
                    {"name": "lang", "in": "query", "schema": {"type": "string", "enum": ["ka", "en", "ru"], "default": "ka"}},
                    {"name": "calendar", "in": "query", "schema": {"type": "string", "enum": ["old", "new"], "default": "old"}}
                ],
                "responses": {"200": {"description": "Month calendar with all days"}}
            }
        },
        "/api/v1/pascha/{year}": {
            "get": {
                "summary": "Get Orthodox Pascha date and movable cycle",
                "parameters": [
                    {"name": "year", "in": "path", "required": True, "schema": {"type": "integer", "example": 2026}},
                    {"name": "lang", "in": "query", "schema": {"type": "string", "enum": ["ka", "en", "ru"], "default": "ka"}}
                ],
                "responses": {"200": {"description": "Pascha date and all movable cycle feast days"}}
            }
        },
        "/api/v1/feasts/{year}": {
            "get": {
                "summary": "Get all Major Feasts for a year",
                "parameters": [
                    {"name": "year", "in": "path", "required": True, "schema": {"type": "integer", "example": 2026}},
                    {"name": "lang", "in": "query", "schema": {"type": "string", "enum": ["ka", "en", "ru"], "default": "ka"}},
                    {"name": "calendar", "in": "query", "schema": {"type": "string", "enum": ["old", "new"], "default": "old"}}
                ],
                "responses": {"200": {"description": "List of Great Feasts for the year"}}
            }
        },
        "/health": {
            "get": {
                "summary": "Health check",
                "responses": {"200": {"description": "Service health status"}}
            }
        }
    }
}

SWAGGER_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Orthodox Calendar API Documentation</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" />
  <link rel="icon" type="image/png" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/favicon-32x32.png" />
  <style>
    body { margin: 0; padding: 0; background-color: #fafafa; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .topbar { background-color: #1a1a2e; color: white; padding: 12px 24px; display: flex; align-items: center; justify-content: space-between; }
    .topbar h1 { margin: 0; font-size: 1.25rem; font-weight: 600; }
    .badge { background: #e94560; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; }
  </style>
</head>
<body>
  <div class="topbar">
    <h1>☦️ მართლმადიდებლური კალენდრის API / Orthodox Calendar API</h1>
    <span class="badge">v1.0.0</span>
  </div>
  <div id="swagger-ui"></div>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    window.onload = function() {
      SwaggerUIBundle({
        url: '/openapi.json',
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout"
      });
    };
  </script>
</body>
</html>
"""

INDEX_HTML = """<!DOCTYPE html>
<html lang="ka">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>მართლმადიდებლური კალენდრის API | Orthodox Calendar API</title>
  <style>
    :root {
      --bg: #0f172a;
      --card-bg: #1e293b;
      --accent: #d97706;
      --accent-light: #fbbf24;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --border: #334155;
      --code-bg: #090d16;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      padding: 24px;
    }
    .container { max-width: 900px; margin: 0 auto; }
    header { text-align: center; margin-bottom: 36px; padding: 24px 0; border-bottom: 1px solid var(--border); }
    h1 { font-size: 2.2rem; color: var(--accent-light); margin-bottom: 8px; }
    .subtitle { color: var(--text-muted); font-size: 1.1rem; }
    .card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 24px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    h2 { font-size: 1.4rem; color: var(--accent-light); margin-bottom: 16px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }
    ul { list-style: none; }
    li { margin-bottom: 12px; }
    .method { background: #059669; color: white; font-weight: bold; padding: 2px 8px; border-radius: 4px; font-size: 0.85rem; margin-right: 8px; }
    .url { font-family: monospace; color: #38bdf8; text-decoration: none; font-size: 1rem; }
    .url:hover { text-decoration: underline; }
    .desc { color: var(--text-muted); font-size: 0.95rem; margin-top: 4px; margin-left: 56px; }
    pre {
      background: var(--code-bg);
      border: 1px solid var(--border);
      padding: 16px;
      border-radius: 8px;
      overflow-x: auto;
      font-family: monospace;
      color: #34d399;
      font-size: 0.95rem;
    }
    .links { display: flex; gap: 16px; justify-content: center; margin-top: 24px; }
    .btn {
      background: var(--accent);
      color: white;
      text-decoration: none;
      padding: 10px 20px;
      border-radius: 8px;
      font-weight: 600;
      transition: background 0.2s;
    }
    .btn:hover { background: var(--accent-light); color: #000; }
    .btn-secondary { background: var(--border); }
    .btn-secondary:hover { background: #475569; color: white; }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>☦️ მართლმადიდებლური კალენდრის API</h1>
      <p class="subtitle">Orthodox Liturgical Calendar API (ქართული • English • Русский)</p>
      <div class="links">
        <a href="/docs" class="btn">📖 Swagger UI / დოკუმენტაცია</a>
        <a href="/api/v1/today" class="btn btn-secondary">📅 დღევანდელი დღე (JSON)</a>
        <a href="/health" class="btn btn-secondary">💚 Health Check</a>
      </div>
    </header>

    <div class="card">
      <h2>📌 ძირითადი API ენდფოინთები</h2>
      <ul>
        <li>
          <span class="method">GET</span><a class="url" href="/api/v1/today">/api/v1/today?lang=ka&calendar=old</a>
          <div class="desc">დღევანდელი დღის ინფორმაცია: წმინდანები, დღესასწაული, მარხვის წესი</div>
        </li>
        <li>
          <span class="method">GET</span><a class="url" href="/api/v1/day?date=2026-10-14&lang=ka">/api/v1/day?date=YYYY-MM-DD&lang=ka</a>
          <div class="desc">კონკრეტული თარიღის ინფორმაცია (მაგ: სვეტიცხოვლობა, გიორგობა, შობა)</div>
        </li>
        <li>
          <span class="method">GET</span><a class="url" href="/api/v1/day/2026/10/14?lang=ka">/api/v1/day/{year}/{month}/{day}?lang=ka</a>
          <div class="desc">კონკრეტული თარიღის ინფორმაცია URL მისამართში</div>
        </li>
        <li>
          <span class="method">GET</span><a class="url" href="/api/v1/month/2026/10?lang=ka">/api/v1/month/{year}/{month}?lang=ka</a>
          <div class="desc">მთლიანი თვის კალენდარი ყველა დღის ჩამონათვალით</div>
        </li>
        <li>
          <span class="method">GET</span><a class="url" href="/api/v1/pascha/2026?lang=ka">/api/v1/pascha/{year}?lang=ka</a>
          <div class="desc">აღდგომის თარიღი და მთელი მოძრავი ციკლი (დიდმარხვა, ბზობა, ამაღლება, სამება)</div>
        </li>
        <li>
          <span class="method">GET</span><a class="url" href="/api/v1/feasts/2026?lang=ka">/api/v1/feasts/{year}?lang=ka</a>
          <div class="desc">წლის უდიდესი საუფლო, საღვთისმშობლო და ქართული დღესასწაულები</div>
        </li>
      </ul>
    </div>

    <div class="card">
      <h2>💡 გამოყენების მაგალითი (cURL)</h2>
      <pre><code>curl -s "http://localhost:8000/api/v1/day?date=2026-10-14&lang=ka" | jq .</code></pre>
    </div>

    <div class="card">
      <h2>🌐 ენების მხარდაჭერა</h2>
      <p style="color: var(--text-muted); margin-bottom: 8px;">პარამეტრი <code>?lang=</code> იღებს:</p>
      <ul style="margin-left: 20px; list-style: disc; color: var(--text-muted);">
        <li><code>ka</code> — ქართული (ნაგულისხმევი)</li>
        <li><code>en</code> — English</li>
        <li><code>ru</code> — Русский</li>
      </ul>
    </div>
  </div>
</body>
</html>
"""


class CalendarAPIHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS pre-flight requests."""
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        lang = query.get("lang", ["ka"])[0]
        calendar_style = query.get("calendar", ["old"])[0]

        # 1. Landing Page
        if path == "/":
            self._send_html(INDEX_HTML)
            return

        # 2. Interactive Documentation (Swagger UI)
        if path in ("/docs", "/swagger"):
            self._send_html(SWAGGER_HTML)
            return

        # 3. OpenAPI specification
        if path == "/openapi.json":
            self._send_json(OPENAPI_SPEC)
            return

        # 4. Health Check
        if path == "/health":
            self._send_json({"status": "healthy", "service": "orthodox-calendar-api", "version": "1.0.0"})
            return

        # 5. /api/v1/today
        if path == "/api/v1/today":
            today = date.today()
            data = service.get_day(today, lang=lang, calendar_style=calendar_style)
            self._send_json(data)
            return

        # 6. /api/v1/day?date=YYYY-MM-DD
        if path == "/api/v1/day":
            date_param = query.get("date", [None])[0]
            if not date_param:
                self._send_error_json(400, "Missing required query parameter: 'date' (format: YYYY-MM-DD)")
                return
            try:
                target_d = date.fromisoformat(date_param)
            except ValueError:
                self._send_error_json(400, f"Invalid date format: '{date_param}'. Expected YYYY-MM-DD")
                return
            data = service.get_day(target_d, lang=lang, calendar_style=calendar_style)
            self._send_json(data)
            return

        # 7. /api/v1/day/{year}/{month}/{day}
        match_day = re.match(r"^/api/v1/day/(\d{4})/(\d{1,2})/(\d{1,2})$", path)
        if match_day:
            y, m, d = int(match_day.group(1)), int(match_day.group(2)), int(match_day.group(3))
            try:
                target_d = date(y, m, d)
            except ValueError as e:
                self._send_error_json(400, f"Invalid date components: {e}")
                return
            data = service.get_day(target_d, lang=lang, calendar_style=calendar_style)
            self._send_json(data)
            return

        # 8. /api/v1/month/{year}/{month}
        match_month = re.match(r"^/api/v1/month/(\d{4})/(\d{1,2})$", path)
        if match_month:
            y, m = int(match_month.group(1)), int(match_month.group(2))
            if not (1 <= m <= 12):
                self._send_error_json(400, f"Invalid month: {m}. Must be between 1 and 12")
                return
            data = service.get_month(y, m, lang=lang, calendar_style=calendar_style)
            self._send_json(data)
            return

        # 9. /api/v1/pascha/{year}
        match_pascha = re.match(r"^/api/v1/pascha/(\d{4})$", path)
        if match_pascha:
            y = int(match_pascha.group(1))
            data = service.get_pascha_info(y, lang=lang)
            self._send_json(data)
            return

        # 10. /api/v1/feasts/{year}
        match_feasts = re.match(r"^/api/v1/feasts/(\d{4})$", path)
        if match_feasts:
            y = int(match_feasts.group(1))
            data = service.get_year_feasts(y, lang=lang, calendar_style=calendar_style)
            self._send_json(data)
            return

        # 404 Not Found
        self._send_error_json(404, f"Endpoint not found: {path}. Visit /docs for documentation.")

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def _send_json(self, data: Any, status: int = 200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html_str: str, status: int = 200):
        body = html_str.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _send_error_json(self, status: int, message: str):
        self._send_json({"error": message, "status_code": status}, status=status)

    def log_message(self, format, *args):
        # Override to keep logs clean
        return


def run_server(host: str = "0.0.0.0", port: int = 8000):
    server = HTTPServer((host, port), CalendarAPIHandler)
    print(f"☦️ Orthodox Calendar API server running on http://{host}:{port}")
    print(f"📖 Documentation available at http://{host}:{port}/docs")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.server_close()


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port=port)
