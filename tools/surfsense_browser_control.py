import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright


PROFILE_DIR = Path("/tmp/surfsense-chromium-profile")
STATE_FILE = Path("/tmp/surfsense_browser_state.json")


def save_state(page):
    STATE_FILE.write_text(
        json.dumps(
            {
                "url": page.url,
                "title": page.title(),
                "ts": time.time(),
            },
            indent=2,
        )
    )


def main():
    start_url = sys.argv[1] if len(sys.argv) > 1 else "https://console.cloud.google.com/apis/credentials"
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=False,
            viewport={"width": 1440, "height": 1000},
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--remote-debugging-port=9333",
            ],
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(start_url, wait_until="domcontentloaded", timeout=120000)
        save_state(page)
        print("BROWSER_READY", flush=True)
        print(page.url, flush=True)
        try:
            while True:
                save_state(page)
                time.sleep(2)
        except KeyboardInterrupt:
            context.close()


if __name__ == "__main__":
    main()
