from src.utils import constants, storage
from datetime import date
import pathlib, json

class AddCredentials:
    def __init__(
        self,
        service: str,
        password: str,
        username: str,
        email: str
    ):
        vault_encrypted = True
        credentials = {
            "service": service,
            "password": password,
            "username": username,
            "email": email,
            "date": date.today().strftime("%Y-%m-%d")
        }

        if not constants.VAULT.exists():
            # Initialize VAULT with an empty list.
            vault_encrypted = False
            constants.VAULT.parent.mkdir(parents=True, exist_ok=True)
            constants.VAULT.write_text(
                json.dumps([])
            )

        vault_contents = storage.read_json(
            file=constants.VAULT,
            encrypted=vault_encrypted,
            master_password=constants.MASTER_PASSWORD
        )

        print(vault_contents)


def get_credentials(
    all_credentials: list[dict],
    service: str | None = None,
    password: str | None = None,
    username: str | None = None,
    email: str | None = None
) -> list[dict]:
    """
    Return all credentials from `all_credentials` that match
    all non-None provided fields.

    Parameters:
        all_credentials (list[dict]): A list of credential dictionaries.
        service (str, optional): Service name to match.
        password (str, optional): Password to match.
        username (str, optional): Username to match.
        email (str, optional): Email to match.

    Returns:
        list[dict]: A list of all credential dictionaries matching
        the given search criteria. Returns an empty list if no match is found.
    """
    filters = {
        "service": service,
        "password": password,
        "username": username,
        "email": email,
    }

    return [
        cred
        for cred in all_credentials
        if all(
            value is None or cred.get(field) == value
            for field, value in filters.items()
        )
    ]