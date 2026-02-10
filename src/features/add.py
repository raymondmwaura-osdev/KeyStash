"""
Add credentials to the vault.
"""
from getpass import getpass
from src.utils import storage
import secrets, string, random

def build_cli(subparsers):
    """
    Define the command-line interface options for the
    'add' command.
    """
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument(
        "-s", "--service",
        dest="service", required=True,
        help="Name of the service. Example: 'github.com'."
    )
    add_parser.add_argument(
        "-u", "--username",
        dest="username", required=False, default=None,
        help="Username associated with the account."
    )
    add_parser.add_argument(
        "-e", "--email",
        dest="email", required=False, default=None,
        help="Email associated with the account."
    )
    add_parser.add_argument(
        "-n", "--name",
        dest="name", required=False, default=None,
        help="Unique name for the credential."
    )

def add(service: str, username: str, email: str, name: str) -> None:
    """
    Add credential to the vault.

    This function takes the service, username, and email as
    parameters, prompts the user for the password, and generates
    the credential's unique ID. It also generates a strong password
    when the user doesn't provide one.
    """
    vault_contents = storage.read_vault()
    id = get_unique_id(vault_contents)
    password = get_password()
    candidate = {
        "service": service,
        "password": password,
        "username": username,
        "email": email,
        "id": id,
        "name": name.lower() if type(name) == str else name
    }

    print(f"Name: {name}")

    # Write to vault.
    vault_contents.append(candidate)
    storage.write_vault(vault_contents)
    print("Credential saved successfully!")

def get_password() -> str:
    """
    Get the password to store from the user or generate one.
    Return the password as a string.
    """
    print("Enter the password to store.")
    print("Leave blank to generate a random password.")
    password = getpass("Password: ")

    if not password:
        password = generate_password()
        print("Generated a strong password.")

    return password

def generate_password():
    """
    Generate and return a strong password.

    Properties:
        Length: 16 characters
        Characters: uppercase and lowercase letters, digits, symbols.
        Avoids the following symbols: `'"\\|<>
        Has at least one uppercase letter and one lowercase letter.
        Has at least 3 numbers.
    """
    password_length = 16
    symbols = "!@#$%^&*()-_=+[]{};:,.?/"
    characters = string.ascii_letters + string.digits + symbols

    while True:
        password = "".join(secrets.choice(characters) for _ in range(password_length))
        # Check password strength.
        if (any(char.isupper() for char in password)
        and any(char.islower() for char in password)
        and sum(char.isdigit() for char in password) >= 3):
            break

    return password

def get_unique_id(existing_credentials):
    """
    Generate a unique ID between 100 and 999 (inclusive) that is not already in use.
    
    Parameters:
    existing_credentials (list): A list of dictionaries, each containing an "ID" key
    
    Returns:
    int: A unique ID between 100 and 999
    
    Raises:
    ValueError: If all possible IDs are already taken
    """
    existing_ids = {record["id"] for record in existing_credentials}
    available_ids = set(range(100, 1000)) - existing_ids
    
    if not available_ids:
        raise ValueError("All IDs between 100 and 999 are already taken")
    
    return random.choice(list(available_ids))
