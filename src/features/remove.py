"""
Remove a credential from the vault.
"""
from src.utils import storage
import sys

def build_cli(subparsers):
    remove_parser = subparsers.add_parser("remove")
    remove_parser_group = remove_parser.add_mutually_exclusive_group(required=True)
    remove_parser_group.add_argument(
        "-n", "--name",
        dest="name", required=False, default=None,
        help="'name' of the credential to remove. Use 'keystash search' to get it."
    )
    remove_parser_group.add_argument(
        "--id", dest="id", type=int,
        required=False, default=None,
        help="ID of the credential to remove. Use 'keystash search' to get it."
    )

def remove(cli_namespace) -> None:
    """
    Remove credential from the vault. The credential is specified by either
    'name' or 'id'. Do nothing if the credential doesn't exist.
    """
    name = cli_namespace.name
    id = cli_namespace.id
    credentials = storage.read_vault()

    if name:
        for cred in credentials:
            if cred["name"] == name.lower():
                target = cred
                break
        else:
            print(f"No credential with name '{name}' found.")
            sys.exit()

    elif id:
        for cred in credentials:
            if cred["id"] == id:
                target = cred
                break
        else:
            print(f"No credential with id {id} found!")
            sys.exit()

    print("Removing the following credential:")
    print()
    for key, value in target.items():
        if key == "password":
            continue

        print(f"{key.capitalize()}: {value}")
    
    for _ in range(3):
        confirmation = input("Confirm (y/n): ")
        if confirmation.lower() in ["y", "n"]:
            break
    else:
        print("Confirmation failed. Not removing credential.")
        sys.exit()

    if confirmation.lower() == "n":
        print("Not removing credential.")
        sys.exit()

    credentials.remove(target)
    storage.write_vault(credentials)
    print("Credential removed successfully.")

