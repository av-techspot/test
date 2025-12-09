#!/usr/bin/env python3
"""Email domain validator via DNS MX records."""

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable, List, Tuple

import dns.resolver

# Simple email regex for validation; not exhaustive but good enough for basic checks.
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate email domains by checking DNS MX records."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-e",
        "--emails",
        nargs="+",
        help="Email addresses to validate (space-separated).",
    )
    group.add_argument(
        "-f",
        "--file",
        type=Path,
        help="Path to a text file with one email per line.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="DNS query timeout in seconds (default: 5.0).",
    )
    return parser.parse_args()


def load_emails(args: argparse.Namespace) -> List[str]:
    if args.emails:
        return args.emails
    assert args.file, "File path must be provided when using --file."
    if not args.file.exists():
        sys.exit(f"File not found: {args.file}")
    with args.file.open("r", encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


def extract_domain(email: str) -> Tuple[bool, str]:
    """Return (is_valid, domain)."""
    if not EMAIL_REGEX.match(email):
        return False, ""
    return True, email.split("@", 1)[1]


def check_mx(domain: str, timeout: float) -> str:
    """Return Russian status string for the given domain."""
    resolver = dns.resolver.Resolver()
    resolver.timeout = timeout
    resolver.lifetime = timeout
    try:
        answers = resolver.resolve(domain, "MX")
        if answers:
            return "домен валиден"
        return "MX-записи отсутствуют или некорректны"
    except dns.resolver.NXDOMAIN:
        return "домен отсутствует"
    except dns.resolver.NoAnswer:
        return "MX-записи отсутствуют или некорректны"
    except dns.resolver.Timeout:
        return "MX-записи отсутствуют или некорректны"
    except Exception:
        return "MX-записи отсутствуют или некорректны"


def validate_emails(emails: Iterable[str], timeout: float) -> None:
    for raw_email in emails:
        email = raw_email.strip()
        is_valid, domain = extract_domain(email)
        if not is_valid:
            status = "MX-записи отсутствуют или некорректны"
        else:
            status = check_mx(domain, timeout)
        print(f"{email} - {status}")


def main() -> None:
    args = parse_args()
    emails = load_emails(args)
    if not emails:
        sys.exit("No emails provided.")
    validate_emails(emails, args.timeout)


if __name__ == "__main__":
    main()

