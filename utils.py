import uuid


def generate_uuid() -> str:
    """A method to generate a unique UUID

    Returns
    -------
    str
        The unique UUID
    """

    return str(uuid.uuid4())
