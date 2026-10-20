"""
FastAPI application for Orthodox Liturgical Calendar.
Provides interactive OpenAPI/Swagger docs at /docs and Redoc at /redoc.
"""

from datetime import date
from typing import Optional
try:
    from fastapi import FastAPI, Query, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

from app.core.calendar_service import CalendarService

service = CalendarService()

if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="Orthodox Liturgical Calendar API",
        description="☦️ Multilingual Orthodox Liturgical Calendar API (ქართული • English • Русский). Julian and Revised Julian calendars, Paschal cycle, fasting rules, and saints commemorations.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    def root():
        return {
            "message": "☦️ Orthodox Liturgical Calendar API",
            "docs": "/docs",
            "today": "/api/v1/today",
        }

    @app.get("/health")
    def health():
        return {"status": "healthy", "service": "orthodox-calendar-api"}

    @app.get("/api/v1/today")
    def get_today(
        lang: str = Query("ka", regex="^(ka|en|ru)$", description="Language: ka, en, or ru"),
        calendar: str = Query("old", regex="^(old|new)$", description="Calendar style: old (Julian) or new (Revised Julian)"),
    ):
        return service.get_day(date.today(), lang=lang, calendar_style=calendar)

    @app.get("/api/v1/day")
    def get_day_by_query(
        date_str: str = Query(..., alias="date", description="Target date in YYYY-MM-DD format"),
        lang: str = Query("ka", regex="^(ka|en|ru)$"),
        calendar: str = Query("old", regex="^(old|new)$"),
    ):
        try:
            target_d = date.fromisoformat(date_str)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid date format: '{date_str}'. Expected YYYY-MM-DD")
        return service.get_day(target_d, lang=lang, calendar_style=calendar)

    @app.get("/api/v1/day/{year}/{month}/{day}")
    def get_day_by_path(
        year: int,
        month: int,
        day: int,
        lang: str = Query("ka", regex="^(ka|en|ru)$"),
        calendar: str = Query("old", regex="^(old|new)$"),
    ):
        try:
            target_d = date(year, month, day)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return service.get_day(target_d, lang=lang, calendar_style=calendar)

    @app.get("/api/v1/month/{year}/{month}")
    def get_month(
        year: int,
        month: int,
        lang: str = Query("ka", regex="^(ka|en|ru)$"),
        calendar: str = Query("old", regex="^(old|new)$"),
    ):
        if not (1 <= month <= 12):
            raise HTTPException(status_code=400, detail="Month must be between 1 and 12")
        return service.get_month(year, month, lang=lang, calendar_style=calendar)

    @app.get("/api/v1/pascha/{year}")
    def get_pascha(
        year: int,
        lang: str = Query("ka", regex="^(ka|en|ru)$"),
    ):
        return service.get_pascha_info(year, lang=lang)

    @app.get("/api/v1/feasts/{year}")
    def get_feasts(
        year: int,
        lang: str = Query("ka", regex="^(ka|en|ru)$"),
        calendar: str = Query("old", regex="^(old|new)$"),
    ):
        return service.get_year_feasts(year, lang=lang, calendar_style=calendar)

else:
    app = None
