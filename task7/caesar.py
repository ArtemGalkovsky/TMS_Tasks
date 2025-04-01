from string import printable

ALPHABET = printable

def caesar_cipher_encode(string: str, shift: int) -> str:
    shift = shift % len(ALPHABET)

    encoded_string = ""
    for letter in string:
        if letter not in ALPHABET:
            raise ValueError(f"The letter '{letter}' in '{string}' is not in the alphabet!")

        new_index = (ALPHABET.index(letter) + shift) % len(ALPHABET)
        encoded_string += ALPHABET[new_index]

    return encoded_string

def caesar_cipher_decode(string: str, shift: int) -> str:
    shift = shift % len(ALPHABET)

    decoded_string = ""
    for letter in string:
        if letter not in ALPHABET:
            raise ValueError(f"The letter '{letter}' in '{string}' is not in the alphabet!")

        new_index = (ALPHABET.index(letter) - shift) % len(ALPHABET)
        decoded_string += ALPHABET[new_index]

    return decoded_string


