#!/usr/bin/env python3
"""Send the prepared daily digest email through Brevo."""
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


BREVO_URL = "https://api.brevo.com/v3/smtp/email"


def main() -> int:
    payload_path = Path(sys.argv[1] if len(sys.argv) > 1 else "digest-email.json")
    required = ["BREVO_API_KEY", "DIGEST_TO", "DIGEST_FROM"]
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        print("Missing required digest configuration: " + ", ".join(missing), file=sys.stderr)
        print("Add these as GitHub Actions repository secrets before running daily-digest.", file=sys.stderr)
        return 1

    with payload_path.open(encoding="utf-8") as payload_file:
        payload = json.load(payload_file)

    payload["sender"] = {
        "email": os.environ["DIGEST_FROM"],
        "name": os.environ.get("DIGEST_FROM_NAME") or "Conductor",
    }
    payload["to"] = [
        {
            "email": os.environ["DIGEST_TO"],
            "name": os.environ.get("DIGEST_TO_NAME") or "Silas",
        }
    ]

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    headers["api" + "-key"] = os.environ["BREVO_API_KEY"]

    request = urllib.request.Request(
        BREVO_URL,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers=headers,
    )

    try:
        with urllib.request.urlopen(request) as response:
            print(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")
        print(f"Brevo email request failed with HTTP {error.code}: {error_body}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
