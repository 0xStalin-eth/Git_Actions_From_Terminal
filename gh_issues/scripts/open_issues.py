import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env", override=True)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")  # "owner/repo" or full GitHub URL


def parse_repo(value):
    # Accept "https://github.com/owner/repo" or "owner/repo"
    if value.startswith("http"):
        parts = value.rstrip("/").split("github.com/")[-1].split("/")
        return f"{parts[0]}/{parts[1]}"
    return value


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/open_issues.py <config/open_numbers.txt> [repo_url]")
        print("  python scripts/open_issues.py 1 2 3 4 5 [repo_url]")
        sys.exit(1)

    # Detect inline numbers vs file path: if the first arg is all digits, treat all
    # digit args as issue numbers and the last arg (if non-digit) as the repo.
    args = sys.argv[1:]
    if args[0].isdigit():
        digit_args = [a for a in args if a.isdigit()]
        non_digit_args = [a for a in args if not a.isdigit()]
        numbers = [int(a) for a in digit_args]
        repo = parse_repo(non_digit_args[0] if non_digit_args else GITHUB_REPO)
    else:
        with open(args[0]) as f:
            numbers = [int(line.strip()) for line in f if line.strip()]
        repo = parse_repo(args[1] if len(args) > 1 else GITHUB_REPO)

    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN is not set.")
        sys.exit(1)

    if not repo:
        print("Error: repo not provided. Pass it as argument or set GITHUB_REPO in .env")
        sys.exit(1)

    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
    )

    opened = 0
    failed = 0

    for number in numbers:
        url = f"https://api.github.com/repos/{repo}/issues/{number}"
        resp = session.patch(url, json={"state": "open"})
        if resp.status_code == 200:
            data = resp.json()
            print(f"[OK]   #{data['number']} reopened — {data['title']}")
            opened += 1
        else:
            msg = resp.json().get("message", resp.text)
            print(f"[FAIL] #{number}: {resp.status_code} {msg}")
            failed += 1

    print(f"\nDone. Opened: {opened}  Failed: {failed}")


if __name__ == "__main__":
    main()
