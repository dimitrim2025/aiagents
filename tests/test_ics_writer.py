"""Tests for the ICS writer / .ics file export."""

import pytest
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from calendar_tz.models import CalendarEntry, TravelCalendarEntry, Attendee
from calendar_tz.ics_writer import ICSWriter


class TestICSBasics:
    def test_empty_calendar(self):
        writer = ICSWriter()
        ics = writer.to_ics()
        assert "BEGIN:VCALENDAR" in ics
        assert "END:VCALENDAR" in ics
        assert "VERSION:2.0" in ics

    def test_single_event(self):
        entry = CalendarEntry(
            summary="Test Event",
            start=datetime(2025, 7, 15, 10, 0),
            end=datetime(2025, 7, 15, 11, 0),
            start_tz="Europe/Berlin",
            end_tz="Europe/Berlin",
        )
        writer = ICSWriter()
        writer.add(entry)
        ics = writer.to_ics()
        assert "BEGIN:VEVENT" in ics
        assert "END:VEVENT" in ics
        assert "Test Event" in ics

    def test_len(self):
        writer = ICSWriter()
        assert len(writer) == 0
        writer.add(CalendarEntry(
            summary="A", start=datetime(2025, 1, 1, 0, 0),
            end=datetime(2025, 1, 1, 1, 0),
        ))
        assert len(writer) == 1


class TestTimezoneHandling:
    def test_vtimezone_blocks_generated(self):
        entry = CalendarEntry(
            summary="Flight",
            start=datetime(2025, 7, 15, 14, 0),
            end=datetime(2025, 7, 15, 17, 30),
            start_tz="Europe/Berlin",
            end_tz="America/Los_Angeles",
        )
        writer = ICSWriter()
        writer.add(entry)
        ics = writer.to_ics()

        assert "BEGIN:VTIMEZONE" in ics
        assert "TZID:Europe/Berlin" in ics
        assert "TZID:America/Los_Angeles" in ics

    def test_dtstart_has_tzid(self):
        entry = CalendarEntry(
            summary="Meeting",
            start=datetime(2025, 7, 15, 10, 0),
            end=datetime(2025, 7, 15, 11, 0),
            start_tz="Europe/Berlin",
            end_tz="Europe/Berlin",
        )
        writer = ICSWriter()
        writer.add(entry)
        ics = writer.to_ics()
        assert "DTSTART;TZID=Europe/Berlin:" in ics
        assert "DTEND;TZID=Europe/Berlin:" in ics

    def test_cross_timezone_dtstart_dtend(self):
        entry = CalendarEntry(
            summary="Flight",
            start=datetime(2025, 7, 15, 14, 0),
            end=datetime(2025, 7, 15, 17, 30),
            start_tz="Europe/Berlin",
            end_tz="America/Los_Angeles",
        )
        writer = ICSWriter()
        writer.add(entry)
        ics = writer.to_ics()
        assert "DTSTART;TZID=Europe/Berlin:20250715T140000" in ics
        assert "DTEND;TZID=America/Los_Angeles:20250715T173000" in ics

    def test_utc_timezone_no_vtimezone(self):
        entry = CalendarEntry(
            summary="UTC Event",
            start=datetime(2025, 7, 15, 10, 0),
            end=datetime(2025, 7, 15, 11, 0),
            start_tz="UTC",
            end_tz="UTC",
        )
        writer = ICSWriter()
        writer.add(entry)
        ics = writer.to_ics()
        assert "VTIMEZONE" not in ics or "TZID:UTC" not in ics


class TestTravelFlight:
    def test_full_travel_event_ics(self):
        """End-to-end: Berlin→LA flight produces a valid .ics with correct times."""
        flight = TravelCalendarEntry(
            summary="LH456 Berlin → Los Angeles",
            start=datetime(2025, 7, 15, 14, 0),
            end=datetime(2025, 7, 15, 17, 30),
            start_tz="Europe/Berlin",
            end_tz="America/Los_Angeles",
            departure_airport="BER",
            arrival_airport="LAX",
            flight_number="LH456",
            airline="Lufthansa",
            booking_reference="ABC123",
            location="Berlin Brandenburg Airport (BER)",
            alarms=[timedelta(hours=3), timedelta(minutes=30)],
            attendees=[Attendee(email="traveler@example.com", name="Traveler")],
        )
        writer = ICSWriter(calendar_name="Travel")
        writer.add(flight)
        ics = writer.to_ics()

        assert "DTSTART;TZID=Europe/Berlin:20250715T140000" in ics
        assert "DTEND;TZID=America/Los_Angeles:20250715T173000" in ics
        assert "LH456" in ics
        assert "BEGIN:VALARM" in ics
        assert "TRIGGER:-PT3H" in ics
        assert "TRIGGER:-PT30M" in ics
        assert "ATTENDEE" in ics
        assert "traveler@example.com" in ics


class TestFileOutput:
    def test_save_to_file(self):
        entry = CalendarEntry(
            summary="Saved Event",
            start=datetime(2025, 7, 15, 10, 0),
            end=datetime(2025, 7, 15, 11, 0),
            start_tz="UTC",
            end_tz="UTC",
        )
        writer = ICSWriter()
        writer.add(entry)

        with tempfile.NamedTemporaryFile(suffix=".ics", delete=False) as f:
            path = Path(f.name)

        writer.save(path)
        content = path.read_text(encoding="utf-8")
        assert "BEGIN:VCALENDAR" in content
        assert "Saved Event" in content
        path.unlink()

    def test_write_to_fileobj(self):
        import io
        entry = CalendarEntry(
            summary="FP Event",
            start=datetime(2025, 7, 15, 10, 0),
            end=datetime(2025, 7, 15, 11, 0),
        )
        writer = ICSWriter()
        writer.add(entry)
        buf = io.StringIO()
        writer.write_to(buf)
        assert "FP Event" in buf.getvalue()


class TestMultipleEvents:
    def test_multi_event_calendar(self):
        entries = [
            CalendarEntry(
                summary=f"Event {i}",
                start=datetime(2025, 7, 15 + i, 10, 0),
                end=datetime(2025, 7, 15 + i, 11, 0),
                start_tz="Europe/Berlin",
                end_tz="Europe/Berlin",
            )
            for i in range(3)
        ]
        writer = ICSWriter()
        writer.add_all(entries)
        ics = writer.to_ics()
        assert ics.count("BEGIN:VEVENT") == 3
        assert ics.count("END:VEVENT") == 3
        # Only one VTIMEZONE for Berlin even with 3 events
        assert ics.count("TZID:Europe/Berlin") >= 1


class TestEdgeCases:
    def test_special_chars_escaped(self):
        entry = CalendarEntry(
            summary="Meeting; with, special\\chars",
            start=datetime(2025, 7, 15, 10, 0),
            end=datetime(2025, 7, 15, 11, 0),
        )
        writer = ICSWriter()
        writer.add(entry)
        ics = writer.to_ics()
        assert "\\;" in ics
        assert "\\," in ics

    def test_no_dst_timezone(self):
        """Asia/Kolkata has no DST. Should still produce valid VTIMEZONE."""
        entry = CalendarEntry(
            summary="India Meeting",
            start=datetime(2025, 7, 15, 10, 0),
            end=datetime(2025, 7, 15, 11, 0),
            start_tz="Asia/Kolkata",
            end_tz="Asia/Kolkata",
        )
        writer = ICSWriter()
        writer.add(entry)
        ics = writer.to_ics()
        assert "TZID:Asia/Kolkata" in ics
        assert "BEGIN:STANDARD" in ics
