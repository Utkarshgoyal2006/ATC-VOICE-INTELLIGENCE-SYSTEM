import re


def calculate_statistics(transcript, duration):

    words = transcript.split()

    total_words = len(words)

    word_count = total_words

    flight_count = len(
        re.findall(r"\b[A-Z]{2,3}\d{2,4}\b", transcript)
    )

    runway_count = len(
        re.findall(r"runway\s+\d{1,2}", transcript, re.IGNORECASE)
    )

    frequency_count = len(
        re.findall(r"\b1\d{2}\.\d\b", transcript)
    )

    altitude_count = len(
        re.findall(r"\bFL\s?\d+\b", transcript, re.IGNORECASE)
    )

    emergency_count = len(
        re.findall(
            r"mayday|pan pan|emergency",
            transcript,
            re.IGNORECASE
        )
    )

    duration_minutes = duration / 60

    if duration_minutes > 0:

        words_per_minute = round(
            total_words / duration_minutes
        )

    else:

        words_per_minute = 0

    return {

        "total_words": total_words,

        "flight_count": flight_count,

        "runway_count": runway_count,

        "frequency_count": frequency_count,

        "altitude_count": altitude_count,

        "emergency_count": emergency_count,

        "words_per_minute": words_per_minute

    }