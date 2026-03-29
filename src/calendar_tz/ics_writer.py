"""RFC 5545 compliant .ics file generator with full VTIMEZONE support.

Generates calendar files that work correctly on:
- Apple Calendar (macOS / iOS / iPhone)
- Google Calendar (Android / Web)
- Microsoft Outlook (Windows / macOS / Web)
- Thunderbird / other RFC 5545 clients
"""

from __future__ import annotations

import textwrap
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import IO, Union
from zoneinfo import ZoneInfo

from calendar_tz.models import CalendarEntry, Attendee
from calendar_tz.timezone_utils import get_tz


_PRODID = "-//CalendarTZ//Cross-Platform Calendar//EN"
_VERSION = "2.0"
_CALSCALE = "GREGORIAN"


class ICSWriter:
    """Builds an .ics file from one or more CalendarEntry objects."""

    def __init__(self, calendar_name: str = "Calendar") -> None:
        self._entries: list[CalendarEntry] = []
        self._calendar_name = calendar_name

    def add(self, entry: CalendarEntry) -> "ICSWriter":
        self._entries.append(entry)
        return self

    def add_all(self, entries: list[CalendarEntry]) -> "ICSWriter":
        self._entries.extend(entries)
        return self

    # ------------------------------------------------------------------
    # Public output methods
    # ------------------------------------------------------------------

    def to_ics(self) -> str:
        """Return the full .ics content as a string."""
        lines: list[str] = []
        lines.append("BEGIN:VCALENDAR")
        lines.append(f"PRODID:{_PRODID}")
        lines.append(f"VERSION:{_VERSION}")
        lines.append(f"CALSCALE:{_CALSCALE}")
        lines.append("METHOD:PUBLISH")
        lines.append(f"X-WR-CALNAME:{_escape(self._calendar_name)}")

        tz_names = self._collect_timezones()
        for tz_name in sorted(tz_names):
            lines.extend(self._vtimezone(tz_name))

        for entry in self._entries:
            lines.extend(self._vevent(entry))

        lines.append("END:VCALENDAR")
        return "\r\n".join(lines) + "\r\n"

    def save(self, path: Union[str, Path]) -> Path:
        """Write the .ics file to disk and return the Path."""
        path = Path(path)
        path.write_text(self.to_ics(), encoding="utf-8")
        return path

    def write_to(self, fp: IO[str]) -> None:
        """Write the .ics content to an open file-like object."""
        fp.write(self.to_ics())

    # ------------------------------------------------------------------
    # VEVENT generation
    # ------------------------------------------------------------------

    def _vevent(self, entry: CalendarEntry) -> list[str]:
        lines: list[str] = []
        lines.append("BEGIN:VEVENT")
        lines.append(f"UID:{entry.uid}")
        lines.append(f"DTSTAMP:{_format_utc(datetime.now(timezone.utc))}")

        lines.append(
            f"DTSTART;TZID={entry.start_tz}:{_format_local(entry.start_local)}"
        )
        lines.append(
            f"DTEND;TZID={entry.end_tz}:{_format_local(entry.end_local)}"
        )

        lines.append(f"SUMMARY:{_escape(entry.summary)}")

        if entry.description:
            lines.extend(_fold_line(f"DESCRIPTION:{_escape(entry.description)}"))
        if entry.location:
            lines.append(f"LOCATION:{_escape(entry.location)}")
        if entry.url:
            lines.append(f"URL:{entry.url}")

        lines.append(f"STATUS:{entry.status.value}")
        lines.append(f"TRANSP:{entry.transparency.value}")

        for attendee in entry.attendees:
            lines.append(_attendee_line(attendee))

        for alarm_delta in entry.alarms:
            lines.extend(_valarm(alarm_delta))

        lines.append("END:VEVENT")
        return lines

    # ------------------------------------------------------------------
    # VTIMEZONE generation
    # ------------------------------------------------------------------

    def _collect_timezones(self) -> set[str]:
        """Gather all unique IANA timezone names referenced by entries."""
        tzs: set[str] = set()
        for e in self._entries:
            tzs.add(e.start_tz)
            tzs.add(e.end_tz)
        tzs.discard("UTC")
        return tzs

    @staticmethod
    def _vtimezone(tz_name: str) -> list[str]:
        """Generate a VTIMEZONE block with STANDARD and DAYLIGHT components.

        Uses 2024/2025 transition data from the IANA tz database to build
        representative rules. Most modern clients also do their own tz
        lookup by TZID, but including the block ensures maximum compat.
        """
        zi = get_tz(tz_name)
        lines: list[str] = []
        lines.append("BEGIN:VTIMEZONE")
        lines.append(f"TZID:{tz_name}")
        lines.append(f"X-LIC-LOCATION:{tz_name}")

        transitions = _get_tz_transitions(zi, tz_name)
        for component in transitions:
            lines.extend(component)

        lines.append("END:VTIMEZONE")
        return lines

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self._entries)


def _get_tz_transitions(zi: ZoneInfo, tz_name: str) -> list[list[str]]:
    """Compute STANDARD and optionally DAYLIGHT sub-components.

    For zones without DST, only a STANDARD component is emitted.
    For zones with DST, we probe a reference year to find transitions.
    """
    ref_year = 2025
    components: list[list[str]] = []

    jan = datetime(ref_year, 1, 15, tzinfo=zi)
    jul = datetime(ref_year, 7, 15, tzinfo=zi)

    jan_offset = jan.utcoffset()
    jul_offset = jul.utcoffset()

    if jan_offset is None or jul_offset is None:
        return [_standard_only(tz_name, zi)]

    if jan_offset == jul_offset:
        return [_standard_only(tz_name, zi)]

    jan_name = jan.tzname() or tz_name
    jul_name = jul.tzname() or tz_name

    if jul_offset > jan_offset:
        std_offset = jan_offset
        dst_offset = jul_offset
        std_name = jan_name
        dst_name = jul_name
        std_transition, dst_transition = _find_transitions(zi, ref_year, is_northern=True)
    else:
        std_offset = jul_offset
        dst_offset = jan_offset
        std_name = jul_name
        dst_name = jan_name
        std_transition, dst_transition = _find_transitions(zi, ref_year, is_northern=False)

    components.append(_tz_component(
        "STANDARD", std_transition, std_offset, dst_offset, std_name
    ))
    components.append(_tz_component(
        "DAYLIGHT", dst_transition, dst_offset, std_offset, dst_name
    ))

    return components


def _standard_only(tz_name: str, zi: ZoneInfo) -> list[str]:
    dt = datetime(2025, 6, 15, tzinfo=zi)
    offset = dt.utcoffset() or timedelta(0)
    name = dt.tzname() or tz_name
    lines = [
        "BEGIN:STANDARD",
        f"DTSTART:19700101T000000",
        f"TZOFFSETFROM:{_offset_str(offset)}",
        f"TZOFFSETTO:{_offset_str(offset)}",
        f"TZNAME:{name}",
        "END:STANDARD",
    ]
    return lines


def _find_transitions(zi: ZoneInfo, year: int, is_northern: bool) -> tuple[datetime, datetime]:
    """Binary-search for the two DST transition moments in a given year."""
    if is_northern:
        spring_start = datetime(year, 1, 1, tzinfo=zi)
        spring_end = datetime(year, 6, 30, tzinfo=zi)
        fall_start = datetime(year, 7, 1, tzinfo=zi)
        fall_end = datetime(year, 12, 31, tzinfo=zi)
    else:
        spring_start = datetime(year, 7, 1, tzinfo=zi)
        spring_end = datetime(year, 12, 31, tzinfo=zi)
        fall_start = datetime(year, 1, 1, tzinfo=zi)
        fall_end = datetime(year, 6, 30, tzinfo=zi)

    dst_start = _binary_search_transition(zi, spring_start, spring_end)
    std_start = _binary_search_transition(zi, fall_start, fall_end)

    return std_start, dst_start


def _binary_search_transition(zi: ZoneInfo, start: datetime, end: datetime) -> datetime:
    """Find the moment the UTC offset changes between start and end."""
    start_offset = start.utcoffset()
    low = start.replace(tzinfo=None)
    high = end.replace(tzinfo=None)
    for _ in range(50):
        mid = low + (high - low) / 2
        mid_aware = mid.replace(tzinfo=zi)
        if mid_aware.utcoffset() == start_offset:
            low = mid
        else:
            high = mid
    return high.replace(tzinfo=zi)


def _tz_component(
    kind: str,
    transition: datetime,
    to_offset: timedelta,
    from_offset: timedelta,
    name: str,
) -> list[str]:
    local_time = transition.replace(tzinfo=None)
    return [
        f"BEGIN:{kind}",
        f"DTSTART:{local_time.strftime('%Y%m%dT%H%M%S')}",
        f"TZOFFSETFROM:{_offset_str(from_offset)}",
        f"TZOFFSETTO:{_offset_str(to_offset)}",
        f"TZNAME:{name}",
        f"END:{kind}",
    ]


def _offset_str(offset: timedelta) -> str:
    total = int(offset.total_seconds())
    sign = "+" if total >= 0 else "-"
    total = abs(total)
    h, rem = divmod(total, 3600)
    m = rem // 60
    return f"{sign}{h:02d}{m:02d}"


def _format_utc(dt: datetime) -> str:
    return dt.strftime("%Y%m%dT%H%M%SZ")


def _format_local(dt: datetime) -> str:
    return dt.strftime("%Y%m%dT%H%M%S")


def _escape(text: str) -> str:
    """Escape special characters per RFC 5545 §3.3.11."""
    text = text.replace("\\", "\\\\")
    text = text.replace(";", "\\;")
    text = text.replace(",", "\\,")
    text = text.replace("\n", "\\n")
    return text


def _fold_line(line: str, max_len: int = 75) -> list[str]:
    """RFC 5545 content line folding (§3.1): lines > 75 octets get folded."""
    if len(line.encode("utf-8")) <= max_len:
        return [line]
    result: list[str] = []
    encoded = line.encode("utf-8")
    result.append(encoded[:max_len].decode("utf-8", errors="ignore"))
    encoded = encoded[max_len:]
    while encoded:
        chunk = encoded[: max_len - 1]
        result.append(" " + chunk.decode("utf-8", errors="ignore"))
        encoded = encoded[max_len - 1 :]
    return result


def _attendee_line(attendee: Attendee) -> str:
    parts = ["ATTENDEE"]
    if attendee.name:
        parts.append(f'CN="{_escape(attendee.name)}"')
    parts.append(f"RSVP={'TRUE' if attendee.rsvp else 'FALSE'}")
    return ";".join(parts) + f":mailto:{attendee.email}"


def _valarm(before: timedelta) -> list[str]:
    total_seconds = int(before.total_seconds())
    if total_seconds <= 0:
        raise ValueError("Alarm timedelta must be positive (time before event).")
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours and not minutes and not seconds:
        trigger = f"-PT{hours}H"
    elif not hours and minutes and not seconds:
        trigger = f"-PT{minutes}M"
    else:
        trigger = f"-PT{total_seconds}S"

    return [
        "BEGIN:VALARM",
        "ACTION:DISPLAY",
        "DESCRIPTION:Reminder",
        f"TRIGGER:{trigger}",
        "END:VALARM",
    ]
