#!/usr/bin/env python3
"""Pull the contribution calendar into contrib.json.

Auth note: the calendar only includes private contributions when the token
belongs to the user (a PAT with read:user). The workflow falls back to the
repository GITHUB_TOKEN, which still works but reports public activity only —
so if the numbers look small, the GH_PAT secret is missing.
"""

import json
import os
import sys
import urllib.request

QUERY = """
query($login: String!) {
  user(login: $login) {
    login
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          firstDay
          contributionDays { date contributionCount weekday }
        }
      }
    }
  }
}
"""

def main():
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("GH_TOKEN is not set")
    login = os.environ.get("GH_LOGIN", "M1hairu")

    payload = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "m1x-signal-renderer",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.loads(r.read())

    if "errors" in body:
        sys.exit(f"GraphQL error: {body['errors']}")

    user = body["data"]["user"]
    if not user:
        sys.exit(f"no such user: {login}")

    # normalise to the shape the renderer expects
    out = {"data": {"viewer": user}}
    dest = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "contrib.json")
    with open(dest, "w") as f:
        json.dump(out, f)

    total = user["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    print(f"{login}: {total} contributions -> {dest}")


if __name__ == "__main__":
    main()
