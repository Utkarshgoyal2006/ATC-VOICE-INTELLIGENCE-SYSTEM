import re


def detect_flight_numbers(text):

    patterns = [

        r"\b[A-Z]{2}\d{2,4}\b",

        r"\b[A-Z]{3}\d{2,4}\b"

    ]

    flights = []

    for pattern in patterns:

        flights.extend(
            re.findall(pattern, text.upper())
        )

    return list(set(flights))


def detect_runway(text):

    pattern = r"(?:RUNWAY|RWY)\s*(\d{1,2}[LRC]?)"

    match = re.search(
        pattern,
        text.upper()
    )

    if match:

        return match.group(1)

    return None