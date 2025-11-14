from src.utils import constants, storage
from datetime import date
import pathlib, json, sys

class AddCredentials:
    def __init__(
        self,
        service: str,
        password: str,
        username: str,
        email: str
    ):
        vault_encrypted = True
        self.credentials = {
            "service": service,
            "password": password,
            "username": username,
            "email": email,
            "date": date.today().strftime("%Y-%m-%d")
        }

        if not constants.VAULT.exists():
            # Initialize VAULT with an empty list (not encrypted).
            vault_encrypted = False
            constants.VAULT.parent.mkdir(parents=True, exist_ok=True)
            constants.VAULT.write_text(
                json.dumps([])
            )

        self.vault_contents = storage.read_json(
            file=constants.VAULT,
            encrypted=vault_encrypted,
            master_password=constants.MASTER_PASSWORD
        )

        # Scan the vault for duplicates.
        duplicate_scans = [
            self.check_exact_duplicate
        ]
        if any(
            scan()
            for scan in duplicate_scans
        ):
            sys.exit()

        print("No duplicates found.")

    def check_exact_duplicate(self) -> bool:
        """Check if the vault contains an exact duplicate of the
        credentials to save."""
        duplicate_credentials = filter_credentials(
            self.vault_contents,
            service=self.credentials["service"],
            password=self.credentials["password"],
            username=self.credentials["username"],
            email=self.credentials["email"]
        )

        if len(duplicate_credentials) == 0:
            return False

        print("Identical credentials already exist. No changes made.")
        return True

def filter_credentials(
    credentials: list[dict],
    service: str | None = None,
    password: str | None = None,
    username: str | None = None,
    email: str | None = None
    ) -> list[dict]:
    """
    Return all credentials from `credentials` that match
    all non-None provided fields.

    Parameters:
        credentials (list[dict]): A list of credential dictionaries.
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
        for cred in credentials
        if all(
            value is None or cred.get(field) == value
            for field, value in filters.items()
        )
    ]
