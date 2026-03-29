"""Tests for timezone utility helpers."""

import pytest
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

from calendar_tz.timezone_utils import (
    get_tz,
    localize,
    convert_timezone,
    now_in_tz,
    ensure_aware,
    format_utc_offset,
)


class TestGetTz:
    def test_known_timezone(self):
        tz = get_tz("Europe/Berlin")
        assert isinstance(tz, ZoneInfo)

    def test_utc(self):
        tz = get_tz("UTC")
        assert isinstance(tz, ZoneInfo)

    def test_unknown_timezone_raises(self):
        with pytest.raises(ValueError, match="Unknown timezone"):
            get_tz("Mars/Olympus_Mons")


class TestLocalize:
    def test_naive_datetime(self):
        dt = datetime(2025, 7, 15, 10, 0)
        result = localize(dt, "Europe/Berlin")
        assert result.tzinfo is not None
        assert str(result.tzinfo) == "Europe/Berlin"

    def test_already_aware_raises(self):
        dt = datetime(2025, 7, 15, 10, 0, tzinfo=ZoneInfo("UTC"))
        with pytest.raises(ValueError, match="already timezone-aware"):
            localize(dt, "Europe/Berlin")


class TestConvertTimezone:
    def test_berlin_to_la(self):
        berlin = datetime(2025, 7, 15, 14, 0, tzinfo=ZoneInfo("Europe/Berlin"))
        la = convert_timezone(berlin, "America/Los_Angeles")
        assert la.hour == 5  # CEST is UTC+2, PDT is UTC-7 → 14-9=5

    def test_naive_raises(self):
        with pytest.raises(ValueError, match="naive"):
            convert_timezone(datetime(2025, 1, 1), "UTC")


class TestNowInTz:
    def test_returns_aware_datetime(self):
        result = now_in_tz("Asia/Tokyo")
        assert result.tzinfo is not None


class TestEnsureAware:
    def test_naive_gets_default(self):
        dt = datetime(2025, 1, 1, 12, 0)
        result = ensure_aware(dt, "America/New_York")
        assert str(result.tzinfo) == "America/New_York"

    def test_aware_passes_through(self):
        dt = datetime(2025, 1, 1, 12, 0, tzinfo=ZoneInfo("Asia/Tokyo"))
        result = ensure_aware(dt)
        assert str(result.tzinfo) == "Asia/Tokyo"


class TestFormatUtcOffset:
    def test_berlin_summer(self):
        dt = datetime(2025, 7, 15, 12, 0, tzinfo=ZoneInfo("Europe/Berlin"))
        assert format_utc_offset(dt) == "+0200"

    def test_la_summer(self):
        dt = datetime(2025, 7, 15, 12, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
        assert format_utc_offset(dt) == "-0700"

    def test_utc(self):
        dt = datetime(2025, 7, 15, 12, 0, tzinfo=ZoneInfo("UTC"))
        assert format_utc_offset(dt) == "+0000"

    def test_naive_raises(self):
        with pytest.raises(ValueError):
            format_utc_offset(datetime(2025, 1, 1))
