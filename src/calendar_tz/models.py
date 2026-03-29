"""Core data models for calendar entries with timezone support."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

from calendar_tz.timezone_utils import ensure_aware, get_tz


class EventStatus(Enum):
    CONFIRMED = "CONFIRMED"
    TENTATIVE = "TENTATIVE"
    CANCELLED = "CANCELLED"


class Transparency(Enum):
    OPAQUE = "OPAQUE"          # time is blocked
    TRANSPARENT = "TRANSPARENT"  # time is free


@dataclass
class Attendee:
    email: str
    name: Optional[str] = None
    rsvp: bool = True


@dataclass
class CalendarEntry:
    """A single calendar event with full timezone support.

    Both *start* and *end* carry their own timezone, so a single event can
    represent a departure in one timezone and an arrival in another.

    Parameters
    ----------
    summary : str
        Event title.
    start : datetime
        Start time. If naive, *start_tz* is used; if aware, used as-is.
    end : datetime
        End time. Same naive/aware rules as *start*.
    start_tz : str
        IANA timezone for the start time (e.g. "Europe/Berlin").
    end_tz : str
        IANA timezone for the end time (e.g. "America/Los_Angeles").
    description : str
        Event body / notes.
    location : str
        Free-text location.
    uid : str
        Globally unique event ID (auto-generated if omitted).
    status : EventStatus
        CONFIRMED, TENTATIVE, or CANCELLED.
    transparency : Transparency
        OPAQUE (busy) or TRANSPARENT (free).
    attendees : list[Attendee]
        Optional invitees.
    alarms : list[timedelta]
        Each timedelta triggers a reminder *before* the start time.
        E.g. ``timedelta(minutes=30)`` = 30 min before.
    url : str
        Optional URL (e.g. booking confirmation link).
    """

    summary: str
    start: datetime
    end: datetime
    start_tz: str = "UTC"
    end_tz: str = "UTC"
    description: str = ""
    location: str = ""
    uid: str = field(default_factory=lambda: f"{uuid.uuid4()}@calendar-tz")
    status: EventStatus = EventStatus.CONFIRMED
    transparency: Transparency = Transparency.OPAQUE
    attendees: list[Attendee] = field(default_factory=list)
    alarms: list[timedelta] = field(default_factory=list)
    url: str = ""

    def __post_init__(self) -> None:
        self.start = ensure_aware(self.start, self.start_tz)
        self.end = ensure_aware(self.end, self.end_tz)
        get_tz(self.start_tz)
        get_tz(self.end_tz)

        if self.end <= self.start:
            raise ValueError("end must be after start (both are compared in UTC).")

    @property
    def duration(self) -> timedelta:
        return self.end - self.start

    @property
    def start_local(self) -> datetime:
        """Start time expressed in the start timezone."""
        return self.start.astimezone(get_tz(self.start_tz))

    @property
    def end_local(self) -> datetime:
        """End time expressed in the end timezone."""
        return self.end.astimezone(get_tz(self.end_tz))


@dataclass
class TravelCalendarEntry(CalendarEntry):
    """Convenience subclass for travel itineraries.

    Adds structured departure / arrival info on top of the base CalendarEntry.
    The *start* maps to departure and *end* maps to arrival.
    """

    departure_airport: str = ""
    arrival_airport: str = ""
    flight_number: str = ""
    airline: str = ""
    booking_reference: str = ""
    departure_city: str = ""
    arrival_city: str = ""

    def __post_init__(self) -> None:
        super().__post_init__()
        if not self.description:
            self.description = self._build_description()

    def _build_description(self) -> str:
        lines: list[str] = []
        if self.flight_number:
            label = f"{self.airline} {self.flight_number}" if self.airline else self.flight_number
            lines.append(f"Flight: {label}")
        if self.departure_airport or self.arrival_airport:
            lines.append(f"Route: {self.departure_airport} → {self.arrival_airport}")
        if self.departure_city or self.arrival_city:
            lines.append(f"Cities: {self.departure_city} → {self.arrival_city}")
        lines.append(
            f"Departure: {self.start_local.strftime('%Y-%m-%d %H:%M %Z')} ({self.start_tz})"
        )
        lines.append(
            f"Arrival:   {self.end_local.strftime('%Y-%m-%d %H:%M %Z')} ({self.end_tz})"
        )
        dur = self.duration
        hours, remainder = divmod(int(dur.total_seconds()), 3600)
        minutes = remainder // 60
        lines.append(f"Duration: {hours}h {minutes}m")
        if self.booking_reference:
            lines.append(f"Booking: {self.booking_reference}")
        return "\n".join(lines)
