"""
download_logos.py
==================
Downloads one flag image per national team, using the URL pattern found
via DevTools Inspect on a player row:

    https://api.fifa.com/api/v3/picture/flags-sq-3/{TEAM_CODE}

CONCEPT: why we don't need to scrape this per-player
Every player from the same country shares the exact same flag - so instead
of re-scraping/re-downloading the same French flag 20+ times (once per
French player), we just need each UNIQUE team code once. We already have
every real team code as keys in TEAM_CODE_TO_NAME (built and verified
against the real 291-player scrape in clean_data.py), so this script reuses
that directly rather than duplicating the list.

Run with:  python download_logos.py
"""

import os
import time
import requests

from clean_data import TEAM_CODE_TO_NAME


OUTPUT_DIR = "assets/flags"
URL_TEMPLATE = "https://api.fifa.com/api/v3/picture/flags-sq-3/{code}"

HEADERS = {
    # CONCEPT: same reasoning as the scraper - identifying as a normal
    # browser avoids being blocked outright by servers that reject
    # requests with no/unusual User-Agent headers.
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}

# CONCEPT: determining file extension from the response, not guessing
# Different image APIs serve different formats (PNG, JPEG, SVG, WebP).
# Rather than assuming one and risking a wrong file extension, we read the
# server's own Content-Type header and map it to the right extension.
CONTENT_TYPE_TO_EXTENSION = {
    "image/png": "png",
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/svg+xml": "svg",
    "image/webp": "webp",
}


def safe_filename(team_name: str) -> str:
    """
    CONCEPT: filesystem-safe filenames
    Team names can contain characters that are awkward or invalid in
    filenames (e.g. the apostrophe in "Côte d'Ivoire", or accented
    letters). This keeps letters/numbers/spaces/hyphens and replaces
    everything else with an underscore, so every file saves cleanly on
    any operating system.
    """
    safe = "".join(c if c.isalnum() or c in " -" else "_" for c in team_name)
    return safe.replace(" ", "_")


def download_all_logos():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    succeeded = []
    failed = []

    for code, team_name in TEAM_CODE_TO_NAME.items():
        url = URL_TEMPLATE.format(code=code)
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "").split(";")[0].strip()
            extension = CONTENT_TYPE_TO_EXTENSION.get(content_type)

            if not extension:
                print(f"  Skipped {team_name} ({code}) - unrecognized "
                      f"Content-Type: '{content_type}'")
                failed.append((code, team_name, f"unknown content-type: {content_type}"))
                continue

            filename = f"{safe_filename(team_name)}.{extension}"
            filepath = os.path.join(OUTPUT_DIR, filename)

            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"  Saved {team_name} ({code}) -> {filepath}")
            succeeded.append(team_name)

        except requests.exceptions.RequestException as e:
            print(f"  Failed {team_name} ({code}): {e}")
            failed.append((code, team_name, str(e)))

        # CONCEPT: being polite to the server
        # A small pause between requests avoids hammering FIFA's server
        # with 48+ rapid-fire requests in under a second.
        time.sleep(0.3)

    print(f"\nDone: {len(succeeded)} logos saved, {len(failed)} failed.")
    if failed:
        print("Failed teams:")
        for code, name, reason in failed:
            print(f"  - {name} ({code}): {reason}")


if __name__ == "__main__":
    download_all_logos()