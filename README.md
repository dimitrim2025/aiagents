# calendar-tz

Cross-platform calendar entry creation with full timezone support. Built for travel apps where events span multiple timezones — e.g., a flight departing Berlin at 14:00 CEST and arriving in Los Angeles at 17:30 PDT.

Generates RFC 5545 compliant `.ics` files that work on:

- **iPhone** — Apple Calendar (tap to add)
- **Android** — Google Calendar (open / import)
- **Desktop** — Outlook, Thunderbird, macOS Calendar, Google Calendar web

## Quick Start

```python
from datetime import datetime, timedelta
from calendar_tz import TravelCalendarEntry, ICSWriter, Attendee

flight = TravelCalendarEntry(
    summary="LH456 Berlin → Los Angeles",
    start=datetime(2025, 7, 15, 14, 0),       # 14:00 Berlin time
    end=datetime(2025, 7, 15, 17, 30),         # 17:30 LA time
    start_tz="Europe/Berlin",
    end_tz="America/Los_Angeles",
    departure_airport="BER",
    arrival_airport="LAX",
    flight_number="LH456",
    airline="Lufthansa",
    booking_reference="ABC123",
    location="Berlin Brandenburg Airport (BER)",
    alarms=[timedelta(hours=3), timedelta(minutes=30)],
)

writer = ICSWriter(calendar_name="Travel Itinerary")
writer.add(flight)
writer.save("flight.ics")
```

The resulting `flight.ics` will show 14:00 to anyone viewing in Berlin and 17:30 to anyone viewing in LA, regardless of the device's local timezone.

## Installation

```bash
pip install -e .

# With dev/test dependencies:
pip install -e ".[dev]"
```

Requires Python 3.9+ (uses `zoneinfo` from the standard library — no external dependencies).

## Core Concepts

### CalendarEntry

A single calendar event where `start` and `end` can each have their own IANA timezone:

```python
from calendar_tz import CalendarEntry

meeting = CalendarEntry(
    summary="Cross-timezone standup",
    start=datetime(2025, 7, 15, 9, 0),
    end=datetime(2025, 7, 15, 10, 0),
    start_tz="America/New_York",
    end_tz="America/New_York",
    description="Daily sync",
    location="Zoom",
)
```

### TravelCalendarEntry

Extends `CalendarEntry` with travel-specific fields. Auto-generates a rich description with flight info, route, and duration:

```python
from calendar_tz import TravelCalendarEntry

flight = TravelCalendarEntry(
    summary="UA100 SFO → NRT",
    start=datetime(2025, 8, 1, 11, 0),
    end=datetime(2025, 8, 2, 14, 30),
    start_tz="America/Los_Angeles",
    end_tz="Asia/Tokyo",
    departure_airport="SFO",
    arrival_airport="NRT",
    flight_number="UA100",
    airline="United",
)
```

### ICSWriter

Builds `.ics` output from one or more entries with full VTIMEZONE support:

```python
from calendar_tz import ICSWriter

writer = ICSWriter(calendar_name="My Calendar")
writer.add(entry1)
writer.add(entry2)

# Save to file
writer.save("calendar.ics")

# Get as string (for HTTP response, email attachment, etc.)
ics_string = writer.to_ics()
```

### Timezone Utilities

```python
from calendar_tz import localize, convert_timezone, now_in_tz

# Attach timezone to naive datetime
dt = localize(datetime(2025, 7, 15, 14, 0), "Europe/Berlin")

# Convert between timezones
la_time = convert_timezone(dt, "America/Los_Angeles")  # 05:00 PDT

# Current time in a timezone
tokyo_now = now_in_tz("Asia/Tokyo")
```

## How Timezone Handling Works

Each `.ics` file includes:

1. **VTIMEZONE blocks** — Full DST transition rules for every referenced timezone, so even offline calendar apps can compute the correct local time.
2. **TZID-qualified DTSTART/DTEND** — Start and end times reference their respective timezones by IANA name (e.g., `DTSTART;TZID=Europe/Berlin:20250715T140000`).

This means a Berlin→LA flight correctly shows:
- Departure: 14:00 CEST on the traveler's Berlin calendar
- Arrival: 17:30 PDT on the traveler's LA calendar
- The correct absolute duration (12h 30m) on any device

## Running Tests

```bash
pytest tests/ -v
```

## Examples

See `examples/travel_flight.py` for a complete working example.

## Project Structure

```
src/calendar_tz/
├── __init__.py           # Public API exports
├── models.py             # CalendarEntry, TravelCalendarEntry, Attendee
├── ics_writer.py         # RFC 5545 .ics file generation with VTIMEZONE
└── timezone_utils.py     # Timezone helpers (localize, convert, etc.)
tests/
├── test_models.py        # Model creation, validation, cross-tz behavior
├── test_ics_writer.py    # .ics output, VTIMEZONE, file I/O
└── test_timezone_utils.py # Timezone utility functions
examples/
└── travel_flight.py      # Berlin→LA flight example
```
