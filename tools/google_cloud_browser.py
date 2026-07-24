import json
import os
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


STATE_FILE = Path("/tmp/google_cloud_browser_state.json")
SECRET_STATE_FILE = Path("/tmp/google_cloud_browser_secrets.json")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def pick_page(context, url_hint=None):
    pages = context.pages
    if url_hint:
        for page in pages:
            if url_hint in page.url:
                return page
    for page in pages:
        if "console.cloud.google.com" in page.url or "accounts.google.com" in page.url:
            return page
    return pages[0] if pages else context.new_page()


def snapshot(page):
    data = {
        "url": page.url,
        "title": page.title(),
        "ts": time.time(),
    }
    STATE_FILE.write_text(json.dumps(data, indent=2))
    print(json.dumps(data, indent=2), flush=True)


def dump_text(page):
    snapshot(page)
    try:
        text = page.locator("body").inner_text(timeout=5000)
    except Exception as exc:
        text = f"<could not read body: {exc}>"
    print(text[:12000], flush=True)


def update_env_file(assignments):
    env_path = Path.home() / "surfsense" / ".env"
    if not env_path.exists():
        env_path = Path(r"C:\Users\sheke\surfsense\.env")
    text = env_path.read_text()
    for key, value in assignments.items():
        pattern = re.compile(rf"^#?\s*{re.escape(key)}=.*$", re.M)
        line = f"{key}={value}"
        if pattern.search(text):
            text = pattern.sub(line, text, count=1)
        else:
            if not text.endswith("\n"):
                text += "\n"
            text += line + "\n"
    env_path.write_text(text)
    print(f"UPDATED_ENV={env_path}", flush=True)


def extract_google_api_key(page):
    candidates = []
    try:
        body = page.locator("body").inner_text(timeout=5000)
        candidates += re.findall(r"AIza[0-9A-Za-z_-]{20,}", body)
    except Exception:
        pass
    try:
        values = page.locator("input, textarea").evaluate_all(
            "(els) => els.map((e) => e.value || e.getAttribute('value') || '').filter(Boolean)"
        )
        for value in values:
            candidates += re.findall(r"AIza[0-9A-Za-z_-]{20,}", value)
    except Exception:
        pass
    return candidates[0] if candidates else None


def extract_oauth_values(page):
    chunks = []
    try:
        chunks.append(page.locator("body").inner_text(timeout=5000))
    except Exception:
        pass
    try:
        values = page.locator("input, textarea").evaluate_all(
            "(els) => els.map((e) => e.value || e.getAttribute('value') || '').filter(Boolean)"
        )
        chunks.extend(values)
    except Exception:
        pass
    text = "\n".join(chunks)
    id_match = re.search(r"(\d+-[0-9A-Za-z_-]+\.apps\.googleusercontent\.com)", text)
    secret_match = re.search(r"(GOCSPX-[0-9A-Za-z_-]+)", text)
    return (id_match.group(1) if id_match else None, secret_match.group(1) if secret_match else None)


def list_controls(page):
    controls = page.locator("input, textarea, button").evaluate_all(
        """(els) => els.map((e, i) => ({
            i,
            tag: e.tagName,
            type: e.getAttribute('type'),
            aria: e.getAttribute('aria-label'),
            text: (e.innerText || e.textContent || '').trim(),
            value: e.value || e.getAttribute('value') || '',
            placeholder: e.getAttribute('placeholder'),
            visible: !!(e.offsetWidth || e.offsetHeight || e.getClientRects().length)
        }))"""
    )
    print(json.dumps(controls, indent=2), flush=True)


def fill_first_empty_visible_input(page, value):
    inputs = page.locator("input")
    count = inputs.count()
    for i in range(count):
        loc = inputs.nth(i)
        try:
            if not loc.is_visible():
                continue
            input_type = (loc.get_attribute("type") or "").lower()
            aria = loc.get_attribute("aria-label") or ""
            current = loc.input_value(timeout=1000)
            if input_type == "search" or "search" in aria.lower():
                continue
            if current:
                continue
            loc.fill(value, timeout=5000)
            return True
        except Exception:
            continue
    return False


def click_text(page, text, exact=False, timeout=8000):
    loc = page.get_by_text(text, exact=exact).first
    loc.wait_for(state="visible", timeout=timeout)
    loc.click(timeout=timeout)
    page.wait_for_timeout(1000)


def click_role(page, role, name, exact=False, timeout=8000):
    loc = page.get_by_role(role, name=name, exact=exact).first
    loc.wait_for(state="visible", timeout=timeout)
    loc.click(timeout=timeout)
    page.wait_for_timeout(1000)


def fill_by_label(page, label_regex, value, timeout=8000):
    loc = page.get_by_label(re.compile(label_regex, re.I)).first
    loc.wait_for(state="visible", timeout=timeout)
    loc.fill(value, timeout=timeout)
    page.wait_for_timeout(500)


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "state"
    cdp_url = os.getenv("CHROME_CDP_URL", "http://127.0.0.1:9222")
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(cdp_url)
        context = browser.contexts[0]
        page = pick_page(context)

        if command == "state":
            dump_text(page)
            return

        if command == "goto":
            url = sys.argv[2]
            page.goto(url, wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(3000)
            dump_text(page)
            return

        if command == "screenshot":
            path = sys.argv[2] if len(sys.argv) > 2 else "/tmp/google_cloud_browser.png"
            page.screenshot(path=path, full_page=True)
            print(path)
            return

        if command == "controls":
            snapshot(page)
            list_controls(page)
            return

        if command == "click":
            text = sys.argv[2]
            click_text(page, text)
            dump_text(page)
            return

        if command == "click-role":
            role = sys.argv[2]
            name = sys.argv[3]
            click_role(page, role, name)
            dump_text(page)
            return

        if command == "enable-drive":
            page.goto("https://console.cloud.google.com/apis/library/drive.googleapis.com", wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(5000)
            body = page.locator("body").inner_text(timeout=10000)
            print(body[:5000], flush=True)
            if re.search(r"\bEnable\b", body, re.I):
                try:
                    click_role(page, "button", re.compile("Enable", re.I), timeout=15000)
                except Exception:
                    click_text(page, "Enable", timeout=15000)
                page.wait_for_timeout(5000)
            dump_text(page)
            return

        if command == "create-api-key":
            page.goto("https://console.cloud.google.com/apis/credentials", wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(5000)
            # The Cloud Console frequently changes aria names; use text fallbacks.
            try:
                click_role(page, "button", re.compile("Create credentials", re.I), timeout=15000)
            except Exception:
                click_text(page, "Create credentials", timeout=15000)
            try:
                click_text(page, "API key", exact=True, timeout=15000)
            except Exception:
                click_role(page, "menuitem", re.compile("API key", re.I), timeout=15000)
            page.wait_for_timeout(5000)
            dump_text(page)
            return

        if command == "finish-api-key":
            try:
                fill_by_label(page, r"^Name", "SurfSense Google Picker")
            except Exception:
                # First visible text input on the create form is the name.
                page.locator("input").first.fill("SurfSense Google Picker", timeout=8000)
            try:
                click_role(page, "button", re.compile(r"^Create$", re.I), timeout=15000)
            except Exception:
                click_text(page, "Create", exact=True, timeout=15000)
            page.wait_for_timeout(8000)
            api_key = extract_google_api_key(page)
            if not api_key:
                dump_text(page)
                raise SystemExit("API_KEY_NOT_FOUND")
            SECRET_STATE_FILE.write_text(json.dumps({"GOOGLE_PICKER_API_KEY": api_key}, indent=2))
            update_env_file({"GOOGLE_PICKER_API_KEY": api_key})
            print(f"GOOGLE_PICKER_API_KEY_SET=True;LEN={len(api_key)}", flush=True)
            return

        if command == "configure-oauth-client":
            origin = "http://localhost:3929"
            redirect = "http://localhost:3929/api/v1/auth/google/drive/connector/callback"
            page.wait_for_load_state("domcontentloaded", timeout=30000)
            body = page.locator("body").inner_text(timeout=10000)

            add_buttons = page.get_by_role("button", name=re.compile(r"^Add URI$", re.I))

            if origin not in body:
                add_buttons.nth(0).click(timeout=10000)
                page.wait_for_timeout(1000)
                if not fill_first_empty_visible_input(page, origin):
                    raise SystemExit("ORIGIN_INPUT_NOT_FOUND")

            body = page.locator("body").inner_text(timeout=10000)
            if redirect not in body:
                add_buttons.nth(1).click(timeout=10000)
                page.wait_for_timeout(1000)
                if not fill_first_empty_visible_input(page, redirect):
                    raise SystemExit("REDIRECT_INPUT_NOT_FOUND")

            client_id = None
            try:
                body = page.locator("body").inner_text(timeout=10000)
                match = re.search(r"(\d+-[0-9A-Za-z_-]+\.apps\.googleusercontent\.com)", body)
                if match:
                    client_id = match.group(1)
            except Exception:
                pass
            if not client_id:
                match = re.search(r"/clients/([^/?]+)", page.url)
                if match:
                    client_id = match.group(1)

            try:
                click_role(page, "button", re.compile(r"^Save$", re.I), timeout=15000)
            except Exception:
                click_text(page, "Save", exact=True, timeout=15000)
            page.wait_for_timeout(8000)

            assignments = {
                "GOOGLE_DRIVE_REDIRECT_URI": redirect,
            }
            if client_id:
                assignments["GOOGLE_OAUTH_CLIENT_ID"] = client_id
            update_env_file(assignments)
            print(f"GOOGLE_OAUTH_CLIENT_ID_SET={bool(client_id)};LEN={len(client_id or '')}", flush=True)
            print("GOOGLE_DRIVE_REDIRECT_URI_SET=True", flush=True)
            return

        if command == "create-new-oauth-client":
            origin = "http://localhost:3929"
            redirect = "http://localhost:3929/api/v1/auth/google/drive/connector/callback"

            # Name input is the first visible non-search input on this form.
            inputs = page.locator("input")
            for i in range(inputs.count()):
                loc = inputs.nth(i)
                try:
                    if loc.is_visible() and (loc.get_attribute("type") or "").lower() != "search":
                        loc.fill("SurfSense Local", timeout=5000)
                        break
                except Exception:
                    continue

            add_buttons = page.get_by_role("button", name=re.compile(r"^Add URI$", re.I))
            add_buttons.nth(0).click(timeout=10000)
            page.wait_for_timeout(800)
            if not fill_first_empty_visible_input(page, origin):
                raise SystemExit("ORIGIN_INPUT_NOT_FOUND")

            add_buttons.nth(1).click(timeout=10000)
            page.wait_for_timeout(800)
            if not fill_first_empty_visible_input(page, redirect):
                raise SystemExit("REDIRECT_INPUT_NOT_FOUND")

            try:
                click_role(page, "button", re.compile(r"^Create$", re.I), timeout=15000)
            except Exception:
                click_text(page, "Create", exact=True, timeout=15000)
            page.wait_for_timeout(10000)

            client_id, client_secret = extract_oauth_values(page)
            if not client_id or not client_secret:
                dump_text(page)
                print(
                    f"OAUTH_VALUES_FOUND client_id={bool(client_id)} secret={bool(client_secret)}",
                    flush=True,
                )
                raise SystemExit("OAUTH_SECRET_NOT_FOUND")

            update_env_file(
                {
                    "GOOGLE_OAUTH_CLIENT_ID": client_id,
                    "GOOGLE_OAUTH_CLIENT_SECRET": client_secret,
                    "GOOGLE_DRIVE_REDIRECT_URI": redirect,
                }
            )
            print(f"GOOGLE_OAUTH_CLIENT_ID_SET=True;LEN={len(client_id)}", flush=True)
            print(f"GOOGLE_OAUTH_CLIENT_SECRET_SET=True;LEN={len(client_secret)}", flush=True)
            return

        print(f"unknown command: {command}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
