from src.utils import constants
from src.features.add import AddCredentials
import argparse, getpass

parser = argparse.ArgumentParser(prog="KeyStash")
subparsers = parser.add_subparsers(dest="cmd")

# ---------- add command ----------
add_parser = subparsers.add_parser("add")
add_parser.add_argument("-s", "--service", dest="service", required=True)
add_parser.add_argument("-p", "--password", dest="password", required=True)

username_group = add_parser.add_mutually_exclusive_group(required=True)
username_group.add_argument("-u", "--username", dest="username")
username_group.add_argument("--nousername", action="store_true", dest="no_username")

email_group = add_parser.add_mutually_exclusive_group(required=True)
email_group.add_argument("-e", "--email", dest="email")
email_group.add_argument("--noemail", action="store_true", dest="no_email")

args = parser.parse_args()
constants.MASTER_PASSWORD = getpass.getpass("Enter master password: "
    ).encode(encoding="utf-8")
if args.cmd == "add":
    AddCredentials(
        service=args.service,
        password=args.password,
        username=args.username,
        email=args.email
    )