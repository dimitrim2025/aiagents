"""Timezone utility helpers built on the stdlib zoneinfo module."""

from __future__ import annotations

from datetime import datetime, timezone
from zoneinfo import ZoneInfo, available_timezones


def get_tz(tz_name: str) -> ZoneInfo:
    """Return a ZoneInfo object, raising ValueError for unknown zones."""
    if tz_name == "UTC":
        return ZoneInfo("UTC")
    if tz_name not in available_timezones():
        raise ValueError(
            f"Unknown timezone: {tz_name!r}. "
            f"Use IANA timezone names like 'Europe/Berlin' or 'America/Los_Angeles'."
        )
    return ZoneInfo(tz_name)


def localize(dt: datetime, tz_name: str) -> datetime:
    """Attach a timezone to a naive datetime. Raises if already aware."""
    if dt.tzinfo is not None:
        raise ValueError("datetime is already timezone-aware; use convert_timezone() instead.")
    return dt.replace(tzinfo=get_tz(tz_name))


def convert_timezone(dt: datetime, target_tz: str) -> datetime:
    """Convert a timezone-aware datetime to another timezone."""
    if dt.tzinfo is None:
        raise ValueError("datetime is naive; use localize() first.")
    return dt.astimezone(get_tz(target_tz))


def now_in_tz(tz_name: str) -> datetime:
    """Return the current moment in the given timezone."""
    return datetime.now(tz=get_tz(tz_name))


def ensure_aware(dt: datetime, default_tz: str = "UTC") -> datetime:
    """If *dt* is naive, localize it to *default_tz*; otherwise return as-is."""
    if dt.tzinfo is None:
        return localize(dt, default_tz)
    return dt


def format_utc_offset(dt: datetime) -> str:
    """Return the UTC offset string like '+0100' or '-0700' for a tz-aware datetime."""
    if dt.tzinfo is None:
        raise ValueError("datetime must be timezone-aware")
    offset = dt.utcoffset()
    if offset is None:
        return "+0000"
    total_seconds = int(offset.total_seconds())
    sign = "+" if total_seconds >= 0 else "-"
    total_seconds = abs(total_seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes = remainder // 60
    return f"{sign}{hours:02d}{minutes:02d}"
