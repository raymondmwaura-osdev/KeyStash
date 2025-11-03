
from toolbox import crypto_utils
import pathlib, base64, json

def read_json(
    file: pathlib.Path,
    encrypted: bool = True,
    master_password: bytes = None
) -> list | dict:
    """
    Read and deserialize JSON data from a file, optionally decrypting the contents.

    This function reads the specified file and converts its contents back into
    a Python object (list or dictionary). If the file is encrypted, the function
    uses the provided master password to derive the decryption key and restore
    the original JSON data. The function expects encrypted files to follow the
    format produced by `write_json()`:

        <base64(salt)>:<base64(ciphertext)>

    Parameters:
        file (pathlib.Path): The path to the JSON file to read.
        encrypted (bool, optional): Indicates whether the file is encrypted.
            Defaults to True.
        master_password (bytes, optional): The master password used to derive
            the decryption key. Must be provided if `encrypted` is True; should
            be None otherwise.

    Returns:
        list | dict: The deserialized Python object (list or dictionary) loaded
        from the JSON data.

    Raises:
        ValueError: If `encrypted` is True but no master password is provided.

    Notes:
        - Encrypted files must have been written using the corresponding
          `write_json()` function with encryption enabled.
        - When reading unencrypted files, the content is read and parsed as
          plain JSON without any cryptographic processing.
    """
    contents = file.read_text()

    if encrypted and master_password:
        salt, encrypted_content = contents.split(":")

        # Convert to original base64 decoded bytes string and decrypt.
        salt = base64.b64decode(
            salt.encode("utf-8")
        )
        encrypted_content = base64.b64decode(
            encrypted_content.encode("utf-8")
        )
        contents = crypto_utils.decrypt(
            encrypted_content,
            master_password,
            salt
        ).decode("utf-8")

    elif encrypted and not master_password:
        raise ValueError("'master_password' is required when 'encrypted == True'.")

    return json.loads(contents)

def write_json(
    contents: list | dict,
    file: pathlib.Path,
    encrypt: bool = True,
    master_password: bytes = None
):
    """
    Serialize and write JSON data to a file, optionally encrypting the contents.

    This function converts the given Python object (a list or dictionary) into
    a JSON-formatted string and writes it to the specified file. If encryption
    is enabled, the JSON string is first encrypted using a key derived from the
    provided master password. The salt and ciphertext are Base64-encoded and
    written to the file as a single text record in the format:

        <base64(salt)>:<base64(ciphertext)>

    Parameters:
        contents (list | dict): The data to serialize as JSON.
        file (pathlib.Path): The path to the target JSON file.
        encrypt (bool, optional): Whether to encrypt the data before writing.
            Defaults to True.
        master_password (bytes, optional): The master password used to derive
            the encryption key when `encrypt` is True. Must be provided if
            encryption is enabled; should be None otherwise.

    Raises:
        ValueError: If `encrypt` is True but no master password is provided.

    Notes:
        - When encryption is disabled, the JSON text is written in plaintext.
        - When encryption is enabled, the resulting file is not valid JSON
          but a text-encoded cryptographic container that must be decrypted
          before parsing as JSON.
    """
    contents = json.dumps(contents)

    if encrypt and master_password:
        salt, encrypted_contents = crypto_utils.encrypt(contents.encode("utf-8"), master_password)

        # Make salt and encrypted data safe for writing to file.
        # This is done by base64 encoding then converting to string.
        salt = base64.b64encode(salt).decode("utf-8")
        encrypted_contents = base64.b64encode(encrypted_contents).decode("utf-8")

        final = f"{salt}:{encrypted_contents}"
        file.write_text(final)

    elif encrypt and not master_password:
        raise ValueError("'master_password' is required when 'encrypt == True'.")

    else:
        file.write_text(contents)
