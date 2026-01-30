"""
Copy a password to the clipboard.
"""
from src.utils import storage
import pyperclip, sys

def build_cli(subparsers):
    get_subparser = subparsers.add_parser("get")
    get_subparser_group = get_subparser.add_mutually_exclusive_group(required=True)
    get_subparser_group.add_argument(
        "-n", "--name",
        dest="name", required=False, default=None,
        help="The name of the credential with the desired password."
    )
    get_subparser_group.add_argument(
        "--id",
        dest="id", required=False, default=None,
        help="The ID of the credential with the desired password."
    )

def get(cli_namespace) -> None:
    """
    Copy the password from the specified credential to the clipboard.
    The password can be specified by 'name' or 'id'.

    Do nothing if the credential doesn't exist or if the credentials list
    is empty.
    """
    name = cli_namespace.name
    id = int(cli_namespace.id)
    credentials = storage.read_vault()

    if name:
        for cred in credentials:
            if cred["name"] == name.lower():
                target = cred
                break
        else:
            print(f"No credential with name '{name}' found!")
            sys.exit()

    elif id:
        for cred in credentials:
            if cred["id"] == id:
                target = cred
                break
        else:
            print(f"No credential with ID {id} found!")
            sys.exit()

    pyperclip.copy(target["password"])
    print("Password copied to clipboard.")
