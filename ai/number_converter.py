DIGITS = {
    "0": "zero",
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
}


def convert_numbers(text):

    words = []

    for token in text.split():

        if token.isdigit():

            converted = " ".join(DIGITS[d] for d in token)

            words.append(converted)

        else:

            words.append(token)

    return " ".join(words)