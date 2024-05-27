import uuid


def generate_uuid() -> str:
    """A method to generate a unique UUID

    Returns
    -------
    str
        The unique UUID
    """

    return str(uuid.uuid4())


def validate_input(value: str, min_length: int = 1, max_length: int = 64, allow_numbers: bool = True,
                   allow_special: bool = True) -> bool:
    """
    A standardized input validation method.
    :param value: The input we are validating.
    :param min_length: The minimum amount of characters REQUIRED.
    :param max_length: The maximum amount of characters ALLOWED.
    :param allow_numbers: Whether we can use numbers.
    :param allow_special: Whether we can use special characters.
    :return: Whether the input is valid.
    """

    # Check for MIN_LENGTH
    if len(value) < min_length:
        return False

    # Check for MAX_LENGTH
    if len(value) > max_length:
        return False

    # Check for ALLOW_NUMBERS
    if any(character.isdigit() for character in value) and not allow_numbers:
        return False

    # Check for ALLOW_SPECIAL
    if any(not character.isalnum() and character != '_' for character in value) and not allow_special:
        return False

    # S'all good, man
    return True
