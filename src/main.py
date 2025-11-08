from features import add
import argparse

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
if args.cmd == "add":
    add.add_password(
        service=args.service,
        password=args.password,
        username=args.username,
        email=args.email
    )