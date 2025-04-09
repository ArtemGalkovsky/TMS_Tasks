def try_convert_str2int(number_string: str) -> int | None:
    if number_string.isnumeric():
        return int(number_string)

    return None