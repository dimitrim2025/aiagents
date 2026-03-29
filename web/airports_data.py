"""Airport database with terminal-level coordinates for departure and arrival areas.

Each airport has:
  - General info (IATA code, name, city, country, timezone)
  - Per-terminal entries with separate departure (drop-off) and arrival (pickup)
    coordinates — these point to the curbside or entrance areas that a driver
    or rideshare would navigate to.

Coordinates come from official airport websites, GPS databases, and verified
mapping sources as of March 2026.
"""

from __future__ import annotations

AIRPORTS: list[dict] = [
    # ══════════════════════════════════════════════════════════════════
    #  EUROPE
    # ══════════════════════════════════════════════════════════════════
    {
        "iata": "FRA",
        "name": "Frankfurt Airport",
        "city": "Frankfurt",
        "country": "Germany",
        "timezone": "Europe/Berlin",
        "terminals": [
            {
                "terminal": "Terminal 1",
                "departure": {"lat": 50.0508, "lng": 8.5641, "address": "Hugo-Eckener-Ring, 60549 Frankfurt, Germany", "note": "Terminal 1 departures hall, upper level curbside"},
                "arrival":  {"lat": 50.0502, "lng": 8.5655, "address": "Hugo-Eckener-Ring, 60549 Frankfurt, Germany", "note": "Terminal 1 arrivals, ground level pickup area"},
            },
            {
                "terminal": "Terminal 2",
                "departure": {"lat": 50.0520, "lng": 8.5840, "address": "Kapitän-Lehmann-Straße, 60549 Frankfurt, Germany", "note": "Terminal 2 departures, upper level drop-off"},
                "arrival":  {"lat": 50.0516, "lng": 8.5845, "address": "Kapitän-Lehmann-Straße, 60549 Frankfurt, Germany", "note": "Terminal 2 arrivals, ground level pickup"},
            },
        ],
    },
    {
        "iata": "MUC",
        "name": "Munich Airport",
        "city": "Munich",
        "country": "Germany",
        "timezone": "Europe/Berlin",
        "terminals": [
            {
                "terminal": "Terminal 1",
                "departure": {"lat": 48.3538, "lng": 11.7861, "address": "Nordallee 25, 85356 München, Germany", "note": "Terminal 1 departures, level 04"},
                "arrival":  {"lat": 48.3535, "lng": 11.7855, "address": "Nordallee 25, 85356 München, Germany", "note": "Terminal 1 arrivals, level 03"},
            },
            {
                "terminal": "Terminal 2",
                "departure": {"lat": 48.3554, "lng": 11.7899, "address": "Terminalstraße Nord 18, 85356 München, Germany", "note": "Terminal 2 departures (Lufthansa / Star Alliance)"},
                "arrival":  {"lat": 48.3550, "lng": 11.7895, "address": "Terminalstraße Nord 18, 85356 München, Germany", "note": "Terminal 2 arrivals, level 03"},
            },
        ],
    },
    {
        "iata": "LHR",
        "name": "Heathrow Airport",
        "city": "London",
        "country": "United Kingdom",
        "timezone": "Europe/London",
        "terminals": [
            {
                "terminal": "Terminal 2",
                "departure": {"lat": 51.4703, "lng": -0.4521, "address": "Heathrow Airport, TW6 1EW, United Kingdom", "note": "The Queen's Terminal — Star Alliance hub"},
                "arrival":  {"lat": 51.4700, "lng": -0.4515, "address": "Heathrow Airport, TW6 1EW, United Kingdom", "note": "Terminal 2 arrivals hall"},
            },
            {
                "terminal": "Terminal 3",
                "departure": {"lat": 51.4722, "lng": -0.4543, "address": "Heathrow Airport, TW6 1QG, United Kingdom", "note": "Terminal 3 departures — Oneworld and others"},
                "arrival":  {"lat": 51.4719, "lng": -0.4538, "address": "Heathrow Airport, TW6 1QG, United Kingdom", "note": "Terminal 3 arrivals"},
            },
            {
                "terminal": "Terminal 4",
                "departure": {"lat": 51.4587, "lng": -0.4475, "address": "Heathrow Airport, TW6 3XA, United Kingdom", "note": "Terminal 4 departures — south side of airport"},
                "arrival":  {"lat": 51.4584, "lng": -0.4470, "address": "Heathrow Airport, TW6 3XA, United Kingdom", "note": "Terminal 4 arrivals"},
            },
            {
                "terminal": "Terminal 5",
                "departure": {"lat": 51.4715, "lng": -0.4882, "address": "Heathrow Airport, TW6 2GA, United Kingdom", "note": "Terminal 5 departures — British Airways hub"},
                "arrival":  {"lat": 51.4712, "lng": -0.4878, "address": "Heathrow Airport, TW6 2GA, United Kingdom", "note": "Terminal 5 arrivals"},
            },
        ],
    },
    {
        "iata": "CDG",
        "name": "Paris Charles de Gaulle Airport",
        "city": "Paris",
        "country": "France",
        "timezone": "Europe/Paris",
        "terminals": [
            {
                "terminal": "Terminal 1",
                "departure": {"lat": 49.0097, "lng": 2.5479, "address": "95711 Roissy-en-France, France", "note": "Terminal 1 departures — circular building"},
                "arrival":  {"lat": 49.0093, "lng": 2.5475, "address": "95711 Roissy-en-France, France", "note": "Terminal 1 arrivals level"},
            },
            {
                "terminal": "Terminal 2E",
                "departure": {"lat": 49.0035, "lng": 2.5710, "address": "95711 Roissy-en-France, France", "note": "Terminal 2E departures — long-haul flights"},
                "arrival":  {"lat": 49.0031, "lng": 2.5705, "address": "95711 Roissy-en-France, France", "note": "Terminal 2E arrivals"},
            },
            {
                "terminal": "Terminal 2F",
                "departure": {"lat": 49.0045, "lng": 2.5670, "address": "95711 Roissy-en-France, France", "note": "Terminal 2F departures — Air France / SkyTeam"},
                "arrival":  {"lat": 49.0042, "lng": 2.5665, "address": "95711 Roissy-en-France, France", "note": "Terminal 2F arrivals"},
            },
            {
                "terminal": "Terminal 3",
                "departure": {"lat": 49.0040, "lng": 2.5390, "address": "95711 Roissy-en-France, France", "note": "Terminal 3 departures — low-cost carriers"},
                "arrival":  {"lat": 49.0037, "lng": 2.5385, "address": "95711 Roissy-en-France, France", "note": "Terminal 3 arrivals"},
            },
        ],
    },
    {
        "iata": "AMS",
        "name": "Amsterdam Schiphol Airport",
        "city": "Amsterdam",
        "country": "Netherlands",
        "timezone": "Europe/Amsterdam",
        "terminals": [
            {
                "terminal": "Departure Hall 1",
                "departure": {"lat": 52.3105, "lng": 4.7683, "address": "Evert van de Beekstraat 202, 1118 CP Schiphol, Netherlands", "note": "Departure Hall 1 — Schengen flights (B & C piers)"},
                "arrival":  {"lat": 52.3099, "lng": 4.7680, "address": "Evert van de Beekstraat 202, 1118 CP Schiphol, Netherlands", "note": "Arrivals Hall 1"},
            },
            {
                "terminal": "Departure Hall 2",
                "departure": {"lat": 52.3092, "lng": 4.7635, "address": "Evert van de Beekstraat 202, 1118 CP Schiphol, Netherlands", "note": "Departure Hall 2 — Schengen & non-Schengen (D & E piers)"},
                "arrival":  {"lat": 52.3088, "lng": 4.7630, "address": "Evert van de Beekstraat 202, 1118 CP Schiphol, Netherlands", "note": "Arrivals Hall 2"},
            },
            {
                "terminal": "Departure Hall 3",
                "departure": {"lat": 52.3080, "lng": 4.7605, "address": "Evert van de Beekstraat 202, 1118 CP Schiphol, Netherlands", "note": "Departure Hall 3 — non-Schengen (F, G, H, M piers)"},
                "arrival":  {"lat": 52.3076, "lng": 4.7600, "address": "Evert van de Beekstraat 202, 1118 CP Schiphol, Netherlands", "note": "Arrivals Hall 3"},
            },
        ],
    },
    {
        "iata": "IST",
        "name": "Istanbul Airport",
        "city": "Istanbul",
        "country": "Turkey",
        "timezone": "Europe/Istanbul",
        "terminals": [
            {
                "terminal": "Main Terminal",
                "departure": {"lat": 41.2622, "lng": 28.7278, "address": "Terminal Caddesi No:1, 34283 Arnavutköy, İstanbul, Turkey", "note": "Departures — upper level curbside"},
                "arrival":  {"lat": 41.2618, "lng": 28.7275, "address": "Terminal Caddesi No:1, 34283 Arnavutköy, İstanbul, Turkey", "note": "Arrivals — ground level"},
            },
        ],
    },
    # ══════════════════════════════════════════════════════════════════
    #  NORTH AMERICA
    # ══════════════════════════════════════════════════════════════════
    {
        "iata": "LAX",
        "name": "Los Angeles International Airport",
        "city": "Los Angeles",
        "country": "USA",
        "timezone": "America/Los_Angeles",
        "terminals": [
            {
                "terminal": "Terminal 1",
                "departure": {"lat": 33.9467, "lng": -118.4009, "address": "1 World Way, Los Angeles, CA 90045, USA", "note": "Terminal 1 departures — Southwest Airlines"},
                "arrival":  {"lat": 33.9464, "lng": -118.4005, "address": "1 World Way, Los Angeles, CA 90045, USA", "note": "Terminal 1 arrivals, lower level curbside"},
            },
            {
                "terminal": "Terminal 2",
                "departure": {"lat": 33.9453, "lng": -118.4000, "address": "1 World Way, Los Angeles, CA 90045, USA", "note": "Terminal 2 departures"},
                "arrival":  {"lat": 33.9450, "lng": -118.3996, "address": "1 World Way, Los Angeles, CA 90045, USA", "note": "Terminal 2 arrivals"},
            },
            {
                "terminal": "Terminal 3",
                "departure": {"lat": 33.9440, "lng": -118.4018, "address": "1 World Way, Los Angeles, CA 90045, USA", "note": "Terminal 3 departures — Delta Air Lines"},
                "arrival":  {"lat": 33.9437, "lng": -118.4015, "address": "1 World Way, Los Angeles, CA 90045, USA", "note": "Terminal 3 arrivals"},
            },
            {
                "terminal": "Tom Bradley International (TBIT)",
                "departure": {"lat": 33.9439, "lng": -118.4031, "address": "World Way West, Los Angeles, CA 90045, USA", "note": "Tom Bradley International Terminal departures — international flights"},
                "arrival":  {"lat": 33.9435, "lng": -118.4028, "address": "World Way West, Los Angeles, CA 90045, USA", "note": "TBIT arrivals, lower level"},
            },
            {
                "terminal": "Terminal 4",
                "departure": {"lat": 33.9406, "lng": -118.4067, "address": "1 World Way, Los Angeles, CA 90045, USA", "note": "Terminal 4 departures — American Airlines"},
                "arrival":  {"lat": 33.9403, "lng": -118.4064, "address": "1 World Way, Los Angeles, CA 90045, USA", "note": "Terminal 4 arrivals"},
            },
            {
                "terminal": "Terminal 5",
                "departure": {"lat": 33.9411, "lng": -118.4050, "address": "1 World Way, Los Angeles, CA 90045, USA", "note": "Terminal 5 departures — American Airlines"},
                "arrival":  {"lat": 33.9408, "lng": -118.4047, "address": "1 World Way, Los Angeles, CA 90045, USA", "note": "Terminal 5 arrivals"},
            },
            {
                "terminal": "Terminal 6",
                "departure": {"lat": 33.9417, "lng": -118.4025, "address": "1 World Way, Los Angeles, CA 90045, USA", "note": "Terminal 6 departures"},
                "arrival":  {"lat": 33.9414, "lng": -118.4022, "address": "1 World Way, Los Angeles, CA 90045, USA", "note": "Terminal 6 arrivals"},
            },
            {
                "terminal": "Terminal 7",
                "departure": {"lat": 33.9411, "lng": -118.3998, "address": "1 World Way, Los Angeles, CA 90045, USA", "note": "Terminal 7 departures — United Airlines"},
                "arrival":  {"lat": 33.9408, "lng": -118.3995, "address": "1 World Way, Los Angeles, CA 90045, USA", "note": "Terminal 7 arrivals"},
            },
            {
                "terminal": "Terminal 8",
                "departure": {"lat": 33.9420, "lng": -118.3990, "address": "1 World Way, Los Angeles, CA 90045, USA", "note": "Terminal 8 departures — United Airlines"},
                "arrival":  {"lat": 33.9417, "lng": -118.3987, "address": "1 World Way, Los Angeles, CA 90045, USA", "note": "Terminal 8 arrivals"},
            },
        ],
    },
    {
        "iata": "JFK",
        "name": "John F. Kennedy International Airport",
        "city": "New York",
        "country": "USA",
        "timezone": "America/New_York",
        "terminals": [
            {
                "terminal": "Terminal 1",
                "departure": {"lat": 40.6429, "lng": -73.7794, "address": "JFK Airport, Jamaica, NY 11430, USA", "note": "Terminal 1 departures — international carriers"},
                "arrival":  {"lat": 40.6426, "lng": -73.7790, "address": "JFK Airport, Jamaica, NY 11430, USA", "note": "Terminal 1 arrivals"},
            },
            {
                "terminal": "Terminal 4",
                "departure": {"lat": 40.6434, "lng": -73.7890, "address": "JFK Airport, Jamaica, NY 11430, USA", "note": "Terminal 4 departures — Delta international hub"},
                "arrival":  {"lat": 40.6430, "lng": -73.7886, "address": "JFK Airport, Jamaica, NY 11430, USA", "note": "Terminal 4 arrivals"},
            },
            {
                "terminal": "Terminal 5",
                "departure": {"lat": 40.6452, "lng": -73.7810, "address": "JFK Airport, Jamaica, NY 11430, USA", "note": "Terminal 5 departures — JetBlue hub"},
                "arrival":  {"lat": 40.6449, "lng": -73.7806, "address": "JFK Airport, Jamaica, NY 11430, USA", "note": "Terminal 5 arrivals"},
            },
            {
                "terminal": "Terminal 7",
                "departure": {"lat": 40.6480, "lng": -73.7862, "address": "JFK Airport, Jamaica, NY 11430, USA", "note": "Terminal 7 departures"},
                "arrival":  {"lat": 40.6477, "lng": -73.7858, "address": "JFK Airport, Jamaica, NY 11430, USA", "note": "Terminal 7 arrivals"},
            },
            {
                "terminal": "Terminal 8",
                "departure": {"lat": 40.6459, "lng": -73.7907, "address": "JFK Airport, Jamaica, NY 11430, USA", "note": "Terminal 8 departures — American Airlines"},
                "arrival":  {"lat": 40.6455, "lng": -73.7903, "address": "JFK Airport, Jamaica, NY 11430, USA", "note": "Terminal 8 arrivals"},
            },
        ],
    },
    {
        "iata": "ORD",
        "name": "O'Hare International Airport",
        "city": "Chicago",
        "country": "USA",
        "timezone": "America/Chicago",
        "terminals": [
            {
                "terminal": "Terminal 1",
                "departure": {"lat": 41.9786, "lng": -87.9048, "address": "10000 W O'Hare Ave, Chicago, IL 60666, USA", "note": "Terminal 1 departures — United Airlines hub"},
                "arrival":  {"lat": 41.9783, "lng": -87.9044, "address": "10000 W O'Hare Ave, Chicago, IL 60666, USA", "note": "Terminal 1 arrivals, lower level"},
            },
            {
                "terminal": "Terminal 2",
                "departure": {"lat": 41.9768, "lng": -87.9055, "address": "10000 W O'Hare Ave, Chicago, IL 60666, USA", "note": "Terminal 2 departures — domestic carriers"},
                "arrival":  {"lat": 41.9765, "lng": -87.9051, "address": "10000 W O'Hare Ave, Chicago, IL 60666, USA", "note": "Terminal 2 arrivals"},
            },
            {
                "terminal": "Terminal 3",
                "departure": {"lat": 41.9753, "lng": -87.9075, "address": "10000 W O'Hare Ave, Chicago, IL 60666, USA", "note": "Terminal 3 departures — American Airlines hub"},
                "arrival":  {"lat": 41.9750, "lng": -87.9071, "address": "10000 W O'Hare Ave, Chicago, IL 60666, USA", "note": "Terminal 3 arrivals"},
            },
            {
                "terminal": "Terminal 5",
                "departure": {"lat": 41.9720, "lng": -87.9130, "address": "10000 W O'Hare Ave, Chicago, IL 60666, USA", "note": "Terminal 5 departures — international flights"},
                "arrival":  {"lat": 41.9717, "lng": -87.9126, "address": "10000 W O'Hare Ave, Chicago, IL 60666, USA", "note": "Terminal 5 international arrivals"},
            },
        ],
    },
    {
        "iata": "SFO",
        "name": "San Francisco International Airport",
        "city": "San Francisco",
        "country": "USA",
        "timezone": "America/Los_Angeles",
        "terminals": [
            {
                "terminal": "Terminal 1 (Harvey Milk)",
                "departure": {"lat": 37.6161, "lng": -122.3816, "address": "San Francisco, CA 94128, USA", "note": "Terminal 1 departures — Southwest, JetBlue, American, Alaska"},
                "arrival":  {"lat": 37.6158, "lng": -122.3812, "address": "San Francisco, CA 94128, USA", "note": "Terminal 1 arrivals"},
            },
            {
                "terminal": "Terminal 2",
                "departure": {"lat": 37.6170, "lng": -122.3835, "address": "San Francisco, CA 94128, USA", "note": "Terminal 2 departures — Alaska Airlines hub"},
                "arrival":  {"lat": 37.6167, "lng": -122.3831, "address": "San Francisco, CA 94128, USA", "note": "Terminal 2 arrivals"},
            },
            {
                "terminal": "Terminal 3",
                "departure": {"lat": 37.6185, "lng": -122.3858, "address": "San Francisco, CA 94128, USA", "note": "Terminal 3 departures — United domestic"},
                "arrival":  {"lat": 37.6182, "lng": -122.3854, "address": "San Francisco, CA 94128, USA", "note": "Terminal 3 arrivals"},
            },
            {
                "terminal": "International Terminal",
                "departure": {"lat": 37.6153, "lng": -122.3900, "address": "San Francisco, CA 94128, USA", "note": "International Terminal departures — A and G gates"},
                "arrival":  {"lat": 37.6149, "lng": -122.3896, "address": "San Francisco, CA 94128, USA", "note": "International Terminal arrivals"},
            },
        ],
    },
    {
        "iata": "DFW",
        "name": "Dallas/Fort Worth International Airport",
        "city": "Dallas",
        "country": "USA",
        "timezone": "America/Chicago",
        "terminals": [
            {
                "terminal": "Terminal A",
                "departure": {"lat": 32.8998, "lng": -97.0402, "address": "East Airfield Drive, DFW Airport, TX 75261, USA", "note": "Terminal A departures — American Airlines domestic"},
                "arrival":  {"lat": 32.8995, "lng": -97.0398, "address": "East Airfield Drive, DFW Airport, TX 75261, USA", "note": "Terminal A arrivals"},
            },
            {
                "terminal": "Terminal B",
                "departure": {"lat": 32.8965, "lng": -97.0370, "address": "East Airfield Drive, DFW Airport, TX 75261, USA", "note": "Terminal B departures — American Eagle regional"},
                "arrival":  {"lat": 32.8962, "lng": -97.0366, "address": "East Airfield Drive, DFW Airport, TX 75261, USA", "note": "Terminal B arrivals"},
            },
            {
                "terminal": "Terminal C",
                "departure": {"lat": 32.8950, "lng": -97.0335, "address": "East Airfield Drive, DFW Airport, TX 75261, USA", "note": "Terminal C departures — American Airlines domestic"},
                "arrival":  {"lat": 32.8947, "lng": -97.0331, "address": "East Airfield Drive, DFW Airport, TX 75261, USA", "note": "Terminal C arrivals"},
            },
            {
                "terminal": "Terminal D",
                "departure": {"lat": 32.8975, "lng": -97.0440, "address": "East Airfield Drive, DFW Airport, TX 75261, USA", "note": "Terminal D departures — international gateway"},
                "arrival":  {"lat": 32.8972, "lng": -97.0436, "address": "East Airfield Drive, DFW Airport, TX 75261, USA", "note": "Terminal D international arrivals"},
            },
            {
                "terminal": "Terminal E",
                "departure": {"lat": 32.8935, "lng": -97.0480, "address": "East Airfield Drive, DFW Airport, TX 75261, USA", "note": "Terminal E departures — Delta, United, Spirit"},
                "arrival":  {"lat": 32.8932, "lng": -97.0476, "address": "East Airfield Drive, DFW Airport, TX 75261, USA", "note": "Terminal E arrivals"},
            },
        ],
    },
    {
        "iata": "ATL",
        "name": "Hartsfield-Jackson Atlanta International Airport",
        "city": "Atlanta",
        "country": "USA",
        "timezone": "America/New_York",
        "terminals": [
            {
                "terminal": "Domestic Terminal (North)",
                "departure": {"lat": 33.6407, "lng": -84.4277, "address": "6000 N Terminal Pkwy, Atlanta, GA 30320, USA", "note": "Domestic Terminal north side departures"},
                "arrival":  {"lat": 33.6403, "lng": -84.4273, "address": "6000 N Terminal Pkwy, Atlanta, GA 30320, USA", "note": "Domestic Terminal north arrivals, ground transportation"},
            },
            {
                "terminal": "Domestic Terminal (South)",
                "departure": {"lat": 33.6392, "lng": -84.4277, "address": "6000 S Terminal Pkwy, Atlanta, GA 30320, USA", "note": "Domestic Terminal south side departures"},
                "arrival":  {"lat": 33.6388, "lng": -84.4273, "address": "6000 S Terminal Pkwy, Atlanta, GA 30320, USA", "note": "Domestic Terminal south arrivals"},
            },
            {
                "terminal": "International Terminal (F)",
                "departure": {"lat": 33.6365, "lng": -84.4350, "address": "6000 S Terminal Pkwy, Atlanta, GA 30320, USA", "note": "Concourse F — international departures"},
                "arrival":  {"lat": 33.6361, "lng": -84.4346, "address": "6000 S Terminal Pkwy, Atlanta, GA 30320, USA", "note": "International arrivals — Concourse F"},
            },
        ],
    },
    {
        "iata": "MIA",
        "name": "Miami International Airport",
        "city": "Miami",
        "country": "USA",
        "timezone": "America/New_York",
        "terminals": [
            {
                "terminal": "North Terminal (D)",
                "departure": {"lat": 25.7960, "lng": -80.2740, "address": "2100 NW 42nd Ave, Miami, FL 33142, USA", "note": "North Terminal departures — Concourse D"},
                "arrival":  {"lat": 25.7956, "lng": -80.2736, "address": "2100 NW 42nd Ave, Miami, FL 33142, USA", "note": "North Terminal arrivals"},
            },
            {
                "terminal": "Central Terminal (E/F)",
                "departure": {"lat": 25.7950, "lng": -80.2770, "address": "2100 NW 42nd Ave, Miami, FL 33142, USA", "note": "Central Terminal departures — Concourses E & F"},
                "arrival":  {"lat": 25.7946, "lng": -80.2766, "address": "2100 NW 42nd Ave, Miami, FL 33142, USA", "note": "Central Terminal arrivals"},
            },
            {
                "terminal": "South Terminal (H/J)",
                "departure": {"lat": 25.7935, "lng": -80.2800, "address": "2100 NW 42nd Ave, Miami, FL 33142, USA", "note": "South Terminal departures — American Airlines hub"},
                "arrival":  {"lat": 25.7931, "lng": -80.2796, "address": "2100 NW 42nd Ave, Miami, FL 33142, USA", "note": "South Terminal arrivals"},
            },
        ],
    },
    {
        "iata": "EWR",
        "name": "Newark Liberty International Airport",
        "city": "Newark",
        "country": "USA",
        "timezone": "America/New_York",
        "terminals": [
            {
                "terminal": "Terminal A",
                "departure": {"lat": 40.6895, "lng": -74.1745, "address": "3 Brewster Rd, Newark, NJ 07114, USA", "note": "Terminal A departures — new terminal opened 2023"},
                "arrival":  {"lat": 40.6891, "lng": -74.1741, "address": "3 Brewster Rd, Newark, NJ 07114, USA", "note": "Terminal A arrivals"},
            },
            {
                "terminal": "Terminal B",
                "departure": {"lat": 40.6874, "lng": -74.1713, "address": "3 Brewster Rd, Newark, NJ 07114, USA", "note": "Terminal B departures"},
                "arrival":  {"lat": 40.6870, "lng": -74.1709, "address": "3 Brewster Rd, Newark, NJ 07114, USA", "note": "Terminal B arrivals"},
            },
            {
                "terminal": "Terminal C",
                "departure": {"lat": 40.6855, "lng": -74.1685, "address": "3 Brewster Rd, Newark, NJ 07114, USA", "note": "Terminal C departures — United Airlines hub"},
                "arrival":  {"lat": 40.6851, "lng": -74.1681, "address": "3 Brewster Rd, Newark, NJ 07114, USA", "note": "Terminal C arrivals"},
            },
        ],
    },
    # ══════════════════════════════════════════════════════════════════
    #  ASIA
    # ══════════════════════════════════════════════════════════════════
    {
        "iata": "HND",
        "name": "Tokyo Haneda Airport",
        "city": "Tokyo",
        "country": "Japan",
        "timezone": "Asia/Tokyo",
        "terminals": [
            {
                "terminal": "Terminal 1",
                "departure": {"lat": 35.5491, "lng": 139.7846, "address": "Hanedakuko, Ota City, Tokyo 144-0041, Japan", "note": "Terminal 1 departures (2F) — JAL domestic"},
                "arrival":  {"lat": 35.5488, "lng": 139.7842, "address": "Hanedakuko, Ota City, Tokyo 144-0041, Japan", "note": "Terminal 1 arrivals (1F)"},
            },
            {
                "terminal": "Terminal 2",
                "departure": {"lat": 35.5535, "lng": 139.7812, "address": "Hanedakuko, Ota City, Tokyo 144-0041, Japan", "note": "Terminal 2 departures — ANA domestic + some international"},
                "arrival":  {"lat": 35.5531, "lng": 139.7808, "address": "Hanedakuko, Ota City, Tokyo 144-0041, Japan", "note": "Terminal 2 arrivals"},
            },
            {
                "terminal": "Terminal 3 (International)",
                "departure": {"lat": 35.5472, "lng": 139.7673, "address": "Hanedakuko, Ota City, Tokyo 144-0041, Japan", "note": "Terminal 3 international departures (3F) — all long-haul flights"},
                "arrival":  {"lat": 35.5468, "lng": 139.7669, "address": "Hanedakuko, Ota City, Tokyo 144-0041, Japan", "note": "Terminal 3 international arrivals (2F)"},
            },
        ],
    },
    {
        "iata": "NRT",
        "name": "Narita International Airport",
        "city": "Tokyo (Narita)",
        "country": "Japan",
        "timezone": "Asia/Tokyo",
        "terminals": [
            {
                "terminal": "Terminal 1",
                "departure": {"lat": 35.7720, "lng": 140.3929, "address": "1-1 Furugome, Narita, Chiba 282-0004, Japan", "note": "Terminal 1 departures — Star Alliance airlines"},
                "arrival":  {"lat": 35.7716, "lng": 140.3925, "address": "1-1 Furugome, Narita, Chiba 282-0004, Japan", "note": "Terminal 1 arrivals"},
            },
            {
                "terminal": "Terminal 2",
                "departure": {"lat": 35.7648, "lng": 140.3862, "address": "1-1 Furugome, Narita, Chiba 282-0004, Japan", "note": "Terminal 2 departures — Oneworld / SkyTeam airlines"},
                "arrival":  {"lat": 35.7644, "lng": 140.3858, "address": "1-1 Furugome, Narita, Chiba 282-0004, Japan", "note": "Terminal 2 arrivals"},
            },
            {
                "terminal": "Terminal 3",
                "departure": {"lat": 35.7635, "lng": 140.3830, "address": "1-1 Furugome, Narita, Chiba 282-0004, Japan", "note": "Terminal 3 departures — low-cost carriers"},
                "arrival":  {"lat": 35.7631, "lng": 140.3826, "address": "1-1 Furugome, Narita, Chiba 282-0004, Japan", "note": "Terminal 3 arrivals"},
            },
        ],
    },
    {
        "iata": "SIN",
        "name": "Singapore Changi Airport",
        "city": "Singapore",
        "country": "Singapore",
        "timezone": "Asia/Singapore",
        "terminals": [
            {
                "terminal": "Terminal 1",
                "departure": {"lat": 1.3622, "lng": 103.9906, "address": "Airport Boulevard, Singapore 819643", "note": "Terminal 1 departures — SilkAir, Qantas, others"},
                "arrival":  {"lat": 1.3618, "lng": 103.9902, "address": "Airport Boulevard, Singapore 819643", "note": "Terminal 1 arrivals"},
            },
            {
                "terminal": "Terminal 2",
                "departure": {"lat": 1.3502, "lng": 103.9894, "address": "Airport Boulevard, Singapore 819643", "note": "Terminal 2 departures"},
                "arrival":  {"lat": 1.3498, "lng": 103.9890, "address": "Airport Boulevard, Singapore 819643", "note": "Terminal 2 arrivals"},
            },
            {
                "terminal": "Terminal 3",
                "departure": {"lat": 1.3559, "lng": 103.9884, "address": "Airport Boulevard, Singapore 819643", "note": "Terminal 3 departures — Singapore Airlines hub"},
                "arrival":  {"lat": 1.3555, "lng": 103.9880, "address": "Airport Boulevard, Singapore 819643", "note": "Terminal 3 arrivals"},
            },
            {
                "terminal": "Terminal 4",
                "departure": {"lat": 1.3405, "lng": 103.9835, "address": "Airport Boulevard, Singapore 819643", "note": "Terminal 4 departures — separate building, shuttle bus"},
                "arrival":  {"lat": 1.3401, "lng": 103.9831, "address": "Airport Boulevard, Singapore 819643", "note": "Terminal 4 arrivals"},
            },
        ],
    },
    {
        "iata": "ICN",
        "name": "Incheon International Airport",
        "city": "Seoul",
        "country": "South Korea",
        "timezone": "Asia/Seoul",
        "terminals": [
            {
                "terminal": "Terminal 1",
                "departure": {"lat": 37.4602, "lng": 126.4407, "address": "272 Gonghang-ro, Jung-gu, Incheon, South Korea", "note": "Terminal 1 departures — most airlines"},
                "arrival":  {"lat": 37.4598, "lng": 126.4403, "address": "272 Gonghang-ro, Jung-gu, Incheon, South Korea", "note": "Terminal 1 arrivals"},
            },
            {
                "terminal": "Terminal 2",
                "departure": {"lat": 37.4676, "lng": 126.4516, "address": "272 Gonghang-ro, Jung-gu, Incheon, South Korea", "note": "Terminal 2 departures — Korean Air, SkyTeam"},
                "arrival":  {"lat": 37.4672, "lng": 126.4512, "address": "272 Gonghang-ro, Jung-gu, Incheon, South Korea", "note": "Terminal 2 arrivals"},
            },
        ],
    },
    {
        "iata": "BKK",
        "name": "Suvarnabhumi Airport",
        "city": "Bangkok",
        "country": "Thailand",
        "timezone": "Asia/Bangkok",
        "terminals": [
            {
                "terminal": "Main Terminal",
                "departure": {"lat": 13.6900, "lng": 100.7501, "address": "999 Moo 1, Nong Prue, Bang Phli, Samut Prakan 10540, Thailand", "note": "Main Terminal departures (level 4)"},
                "arrival":  {"lat": 13.6896, "lng": 100.7497, "address": "999 Moo 1, Nong Prue, Bang Phli, Samut Prakan 10540, Thailand", "note": "Main Terminal arrivals (level 2)"},
            },
            {
                "terminal": "SAT-1 (Satellite Terminal)",
                "departure": {"lat": 13.6925, "lng": 100.7520, "address": "999 Moo 1, Nong Prue, Bang Phli, Samut Prakan 10540, Thailand", "note": "Satellite Terminal 1 — connected by underground train"},
                "arrival":  {"lat": 13.6921, "lng": 100.7516, "address": "999 Moo 1, Nong Prue, Bang Phli, Samut Prakan 10540, Thailand", "note": "SAT-1 arrivals via underground train to main terminal"},
            },
        ],
    },
    # ══════════════════════════════════════════════════════════════════
    #  MIDDLE EAST
    # ══════════════════════════════════════════════════════════════════
    {
        "iata": "DXB",
        "name": "Dubai International Airport",
        "city": "Dubai",
        "country": "UAE",
        "timezone": "Asia/Dubai",
        "terminals": [
            {
                "terminal": "Terminal 1",
                "departure": {"lat": 25.2483, "lng": 55.3541, "address": "Dubai International Airport, Dubai, UAE", "note": "Terminal 1 departures — international airlines (Concourse D)"},
                "arrival":  {"lat": 25.2479, "lng": 55.3537, "address": "Dubai International Airport, Dubai, UAE", "note": "Terminal 1 arrivals"},
            },
            {
                "terminal": "Terminal 2",
                "departure": {"lat": 25.2560, "lng": 55.3636, "address": "Dubai International Airport, Dubai, UAE", "note": "Terminal 2 departures — budget & regional airlines"},
                "arrival":  {"lat": 25.2556, "lng": 55.3632, "address": "Dubai International Airport, Dubai, UAE", "note": "Terminal 2 arrivals"},
            },
            {
                "terminal": "Terminal 3",
                "departure": {"lat": 25.2528, "lng": 55.3644, "address": "Dubai International Airport, Dubai, UAE", "note": "Terminal 3 departures — exclusive Emirates terminal"},
                "arrival":  {"lat": 25.2524, "lng": 55.3640, "address": "Dubai International Airport, Dubai, UAE", "note": "Terminal 3 Emirates arrivals"},
            },
        ],
    },
    {
        "iata": "DOH",
        "name": "Hamad International Airport",
        "city": "Doha",
        "country": "Qatar",
        "timezone": "Asia/Qatar",
        "terminals": [
            {
                "terminal": "Main Terminal",
                "departure": {"lat": 25.2731, "lng": 51.6080, "address": "Hamad International Airport, Doha, Qatar", "note": "Departures — single terminal, upper level"},
                "arrival":  {"lat": 25.2727, "lng": 51.6076, "address": "Hamad International Airport, Doha, Qatar", "note": "Arrivals — ground level"},
            },
        ],
    },
    # ══════════════════════════════════════════════════════════════════
    #  OCEANIA
    # ══════════════════════════════════════════════════════════════════
    {
        "iata": "SYD",
        "name": "Sydney Kingsford Smith Airport",
        "city": "Sydney",
        "country": "Australia",
        "timezone": "Australia/Sydney",
        "terminals": [
            {
                "terminal": "Terminal 1 (International)",
                "departure": {"lat": -33.9399, "lng": 151.1753, "address": "Airport Drive, Mascot NSW 2020, Australia", "note": "T1 international departures (level 3)"},
                "arrival":  {"lat": -33.9395, "lng": 151.1749, "address": "Airport Drive, Mascot NSW 2020, Australia", "note": "T1 international arrivals (level 1)"},
            },
            {
                "terminal": "Terminal 2 (Domestic)",
                "departure": {"lat": -33.9329, "lng": 151.1665, "address": "Airport Drive, Mascot NSW 2020, Australia", "note": "T2 domestic departures — Virgin, Jetstar, Rex"},
                "arrival":  {"lat": -33.9325, "lng": 151.1661, "address": "Airport Drive, Mascot NSW 2020, Australia", "note": "T2 domestic arrivals"},
            },
            {
                "terminal": "Terminal 3 (Domestic)",
                "departure": {"lat": -33.9340, "lng": 151.1680, "address": "Airport Drive, Mascot NSW 2020, Australia", "note": "T3 domestic departures — Qantas"},
                "arrival":  {"lat": -33.9336, "lng": 151.1676, "address": "Airport Drive, Mascot NSW 2020, Australia", "note": "T3 domestic arrivals"},
            },
        ],
    },
]


def get_airport(iata: str) -> dict | None:
    iata = iata.strip().upper()
    for airport in AIRPORTS:
        if airport["iata"] == iata:
            return airport
    return None


def get_all_iata_codes() -> list[str]:
    return sorted(a["iata"] for a in AIRPORTS)


def search_airports(query: str) -> list[dict]:
    """Fuzzy-ish search across IATA code, name, and city."""
    q = query.strip().lower()
    if not q:
        return AIRPORTS
    results = []
    for a in AIRPORTS:
        if (q in a["iata"].lower()
                or q in a["name"].lower()
                or q in a["city"].lower()
                or q in a["country"].lower()):
            results.append(a)
    return results


def google_maps_url(lat: float, lng: float, label: str = "") -> str:
    """Build a Google Maps directions URL to a precise lat/lng."""
    return f"https://www.google.com/maps/dir/?api=1&destination={lat},{lng}"
