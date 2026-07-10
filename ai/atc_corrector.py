import re


ATC_CORRECTIONS = {

    "flower": "tower",
    "flour": "tower",
    "tour": "tower",

    "run way": "runway",

    "take of": "takeoff",
    "take off": "takeoff",

    "go arounds": "go around",

    "holding point": "holding point",

    "read back": "readback",

    "decimal point": "decimal",

    "flight label": "flight level",

    "flight labels": "flight levels",

    "taxi way": "taxiway",

    "may day": "mayday"

}


def correct_atc_text(text):

    corrected = text

    for wrong, right in ATC_CORRECTIONS.items():

        corrected = re.sub(

            rf"\b{re.escape(wrong)}\b",

            right,

            corrected,

            flags=re.IGNORECASE

        )

    return corrected