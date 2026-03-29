#!/usr/bin/env python3
"""Example: Create a calendar entry for a Berlin → Los Angeles flight.

The departure is in German time (Europe/Berlin) and the arrival is in
LA time (America/Los_Angeles). The generated .ics file will show the
correct local time on every device regardless of the user's timezone.

Usage:
    python examples/travel_flight.py

This creates 'berlin_to_la.ics' which you can:
  - Double-click to open in Apple Calendar / Outlook / Thunderbird
  - Import into Google Calendar (Settings → Import & Export)
  - Email to yourself and open on iPhone / Android
"""

from datetime import datetime, timedelta

from calendar_tz import TravelCalendarEntry, ICSWriter, Attendee


def main() -> None:
    flight = TravelCalendarEntry(
        summary="LH456 Berlin → Los Angeles",
        start=datetime(2025, 7, 15, 14, 0),     # 14:00 Berlin time (CEST)
        end=datetime(2025, 7, 15, 17, 30),       # 17:30 LA time (PDT)
        start_tz="Europe/Berlin",
        end_tz="America/Los_Angeles",
        departure_airport="BER",
        arrival_airport="LAX",
        departure_city="Berlin",
        arrival_city="Los Angeles",
        flight_number="LH456",
        airline="Lufthansa",
        booking_reference="ABC123",
        location="Berlin Brandenburg Airport (BER)",
        url="https://www.lufthansa.com",
        alarms=[timedelta(hours=3), timedelta(minutes=30)],
        attendees=[
            Attendee(email="traveler@example.com", name="Alex Traveler"),
        ],
    )

    writer = ICSWriter(calendar_name="Travel Itinerary")
    writer.add(flight)

    path = writer.save("berlin_to_la.ics")
    print(f"Calendar file saved to: {path.resolve()}")
    print()
    print(f"Departure: {flight.start_local.strftime('%Y-%m-%d %H:%M %Z')} (Berlin)")
    print(f"Arrival:   {flight.end_local.strftime('%Y-%m-%d %H:%M %Z')} (LA)")
    print(f"Duration:  {flight.duration}")
    print()
    print("Open this .ics file on any device:")
    print("  - iPhone / Mac: tap/double-click to add to Apple Calendar")
    print("  - Android: open with Google Calendar")
    print("  - Windows: open with Outlook or import into Google Calendar")


if __name__ == "__main__":
    main()
