#!/usr/bin/env python3
"""Check daily digest environment configuration without printing values."""
import os
import sys


def main() -> int:
    should_send = os.environ.get("SHOULD_SEND_EMAIL", "false").lower() == "true"
    required = ["BREVO_API_KEY", "DIGEST_TO", "DIGEST_FROM"]
    optional = ["DIGEST_TO_NAME", "DIGEST_FROM_NAME"]
    missing = [name for name in required if not os.environ.get(name)]
    configured_optional = [name for name in optional if os.environ.get(name)]

    if configured_optional:
        print("Optional digest configuration present: " + ", ".join(configured_optional))
    else:
        print("Optional digest configuration present: none")

    if missing:
        print("Missing required digest configuration: " + ", ".join(missing), file=sys.stderr)
        if should_send:
            print("Add missing values as GitHub Actions repository secrets or variables before running daily-digest.", file=sys.stderr)
            return 1
        print("Email send disabled for this run; missing send configuration does not fail the dry run.")
    else:
        print("Required digest configuration present: " + ", ".join(required))

    if should_send:
        print("Email send enabled for this run.")
    else:
        print("Email send disabled for this run. Inspect daily-digest-artifacts before enabling send_email.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
