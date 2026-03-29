"""Flask web app serving the travel flight dashboard with .ics downloads."""

from __future__ import annotations

import io
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, send_file, abort

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from calendar_tz import TravelCalendarEntry, ICSWriter
from flights_data import FLIGHTS
from airports_data import AIRPORTS, search_airports

app = Flask(__name__, template_folder="templates", static_folder="static")


def _parse_dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M")


def _build_ics(flight: dict) -> str:
    entry = TravelCalendarEntry(
        summary=f"{flight['flight_number']} {flight['departure_city']} → {flight['arrival_city']}",
        start=_parse_dt(flight["departure_time"]),
        end=_parse_dt(flight["arrival_time"]),
        start_tz=flight["departure_tz"],
        end_tz=flight["arrival_tz"],
        departure_airport=flight["departure_airport"],
        arrival_airport=flight["arrival_airport"],
        departure_city=flight["departure_city"],
        arrival_city=flight["arrival_city"],
        flight_number=flight["flight_number"],
        airline=flight["airline"],
        location=f"{flight['departure_airport']} → {flight['arrival_airport']}",
        alarms=[],
    )
    writer = ICSWriter(calendar_name="Travel Flights")
    writer.add(entry)
    return writer.to_ics()


def _get_flight(flight_id: str) -> dict | None:
    for f in FLIGHTS:
        if f["id"] == flight_id:
            return f
    return None


@app.route("/")
def index():
    groups: dict[str, list] = {}
    for f in FLIGHTS:
        group = f["route_group"]
        groups.setdefault(group, []).append(f)
    return render_template("index.html", groups=groups)


@app.route("/download/<flight_id>.ics")
def download_ics(flight_id: str):
    flight = _get_flight(flight_id)
    if not flight:
        abort(404)
    ics_content = _build_ics(flight)
    buf = io.BytesIO(ics_content.encode("utf-8"))
    filename = f"{flight['flight_number']}_{flight['departure_time'][:10]}.ics"
    return send_file(
        buf,
        mimetype="text/calendar",
        as_attachment=True,
        download_name=filename,
    )


@app.route("/preview/<flight_id>.ics")
def preview_ics(flight_id: str):
    flight = _get_flight(flight_id)
    if not flight:
        abort(404)
    ics_content = _build_ics(flight)
    return ics_content, 200, {"Content-Type": "text/plain; charset=utf-8"}


@app.route("/airports")
def airports_page():
    airport_count = len(AIRPORTS)
    terminal_count = sum(len(a["terminals"]) for a in AIRPORTS)
    return render_template(
        "airports.html",
        airports_json=json.dumps(AIRPORTS),
        airport_count=airport_count,
        terminal_count=terminal_count,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
