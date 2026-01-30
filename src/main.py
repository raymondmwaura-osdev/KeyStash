from src.features import add, search, passwd, remove, get
from src.utils import constants, storage
from getpass import getpass
import argparse, sys, bcrypt

def main():
    parser = build_cli()
    cli_namespace = parser.parse_args()
    constants.MASTER_PASSWORD = verify_identity(cli_namespace.cmd)

    if cli_namespace.interactive_mode or not cli_namespace.cmd:
        run_command(cli_namespace)
        interactive_mode(parser)

    else:
        run_command(cli_namespace)

def build_cli():
    """
    Setup all CLI commands and options.

    Return the top level parser got by `argparse.ArgumentParser()`.
    """
    parser = argparse.ArgumentParser(prog="KeyStash")
    parser.add_argument("-i", "--interactive",
        dest="interactive_mode", action="store_true")

    subparsers = parser.add_subparsers(dest="cmd")

    build_cli_functions = [
        # Have all features listed here.
        add.build_cli,
        search.build_cli,
        passwd.build_cli,
        remove.build_cli,
        get.build_cli
    ]
    for build_cli in build_cli_functions:
        build_cli(subparsers)

    return parser

def interactive_mode(parser):
    """
    Continuously prompt the user for commands and execute them.
    """
    while True:
        command = input("(keystash) ").strip()

        if not command: continue
        elif command in ("exit", "quit"):
            sys.exit()

        try:
            cli_namespace = parser.parse_args(command.split(" "))
            run_command(cli_namespace)
        except SystemExit: # Prevent exiting when argparse gets an invalid command/switch.
            continue

def run_command(cli_namespace):
    """
    Run the command given by the user.
    """
    if cli_namespace.cmd == "add":
        add.add(
            service=cli_namespace.service,
            username=cli_namespace.username,
            email=cli_namespace.email,
            name=cli_namespace.name
        )

    elif cli_namespace.cmd == "search":
        search.search(
            service=cli_namespace.service,
            username=cli_namespace.username,
            email=cli_namespace.email
        )

    elif cli_namespace.cmd == "passwd":
        passwd.passwd()

    elif cli_namespace.cmd == "remove":
        remove.remove(int(cli_namespace.id))

    elif cli_namespace.cmd == "get":
        get.get(cli_namespace)

def verify_identity(cmd: None | str) -> str:
    """
    Verify user identity by prompting for the master password.

    Parameters:
        cmd:
            The cli command passed in by the user.

    Return the password if the user is verified, exit otherwise.
    Exit if the master password is not set and 'cmd' != "passwd".
    """
    if constants.HASH.exists():
        password_hash = constants.HASH.read_text().strip()
        for _ in range(3):
            password = getpass("Enter master password: ").strip()

            if bcrypt.checkpw(
                password.encode("utf-8"),
                password_hash.encode("utf-8")
            ):
                return password

            print("Incorrect master password!")

        sys.exit()

    elif cmd != "passwd": # Allow the user to use only 'passwd' when constants.HASH doesn't exist.
        print("Master password not set.")
        print("Use 'keystash passwd' to set the master password.")
        sys.exit()

if __name__ == "__main__":
    main()
