import re

PATTERNS = [

    r"\bAI\d{2,4}\b",
    r"\b6E\d{2,4}\b",
    r"\bSG\d{2,4}\b",
    r"\bUK\d{2,4}\b",
    r"\bIX\d{2,4}\b",
    r"\bI5\d{2,4}\b",

    r"\bAir India\s+\d{2,4}\b",
    r"\bIndiGo\s+\d{2,4}\b",
    r"\bSpiceJet\s+\d{2,4}\b",
    r"\bAkasa\s+\d{2,4}\b"

]

def detect_flights(text):

    flights = []

    for pattern in PATTERNS:

        flights.extend(
            re.findall(
                pattern,
                text,
                flags=re.IGNORECASE
            )
        )

    return list(set(flights))