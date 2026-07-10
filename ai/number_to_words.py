import re

DIGIT_WORDS = {
    "0": "zero",
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "niner"      # ICAO pronunciation
}


def convert_number(number):

    words = []

    for char in number:

        if char == ".":
            words.append("decimal")

        elif char.isdigit():
            words.append(DIGIT_WORDS[char])

        else:
            words.append(char)

    return " ".join(words)


def convert_numbers_to_words(text):

    pattern = r"\d+(\.\d+)?"



    def replace(match):
        return convert_number(match.group())

    return re.sub(pattern, replace, text)

if __name__ == "__main__":

    text = "Descend to 3300 feet. Contact tower on 118.3. QNH 1013."

    print(convert_numbers_to_words(text))