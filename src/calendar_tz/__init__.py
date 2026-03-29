"""
calendar_tz - Cross-platform calendar entry creation with full timezone support.

Generates RFC 5545 compliant .ics files that work on iPhone (Apple Calendar),
Android (Google Calendar), and desktop clients (Outlook, Thunderbird, etc.).

Designed for travel apps where events span multiple timezones (e.g., departure
in Europe/Berlin, arrival in America/Los_Angeles).
"""

from calendar_tz.models import CalendarEntry, TravelCalendarEntry, Attendee
from calendar_tz.ics_writer import ICSWriter
from calendar_tz.timezone_utils import convert_timezone, localize, now_in_tz

__all__ = [
    "CalendarEntry",
    "TravelCalendarEntry",
    "Attendee",
    "ICSWriter",
    "convert_timezone",
    "localize",
    "now_in_tz",
]
