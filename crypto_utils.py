import hashlib
import secrets


def generate_salt() -> bytes:
    """A method to generate salt of 32 bytes

    Returns
    -------
    bytes
        A salt of 32 bytes
    """

    return secrets.token_bytes(32)


def hash_password(password: str, salt: bytes) -> bytes:
    """A method to hash a password using SHA256 with salt

    Parameters
    ----------
    password : str
        The password to hash

    salt : bytes
        The salt to include in the hash
    """

    # Set up the algorithm
    hash_object = hashlib.sha256()

    # Hash the password
    hash_object.update(password.encode('utf-8') + salt)
    return hash_object.digest()
