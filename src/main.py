#!/bin/python3

from features import add
import argparse

parser = argparse.ArgumentParser(prog="KeyStash")
subparsers = parser.add_subparsers(dest="cmd")

add_parser = subparsers.add_parser("add")
add_parser.add_argument("-s", "--service", dest="service")
add_parser.add_argument("-u", "--username", dest="username")
add_parser.add_argument("-p", "--password", dest="password")
add_parser.add_argument("-e", "--email", dest="email")

args = parser.parse_args()
if args.cmd = "add":
    add.add_password(
        service=args.service,
        username=args.username,
        password=args.password,
        email=args.email
    )
