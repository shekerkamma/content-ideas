import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request


BASE = "http://localhost:3929"
EMAIL = "codex.surfsense.test.1781855744@gmail.com"
PASSWORD = "CodexTest12345!"


def request(method, path, data=None, token=None, content_type="application/json"):
    body = None
    headers = {}
    if data is not None:
        if content_type == "application/json":
            body = json.dumps(data).encode()
        else:
            body = urllib.parse.urlencode(data).encode()
        headers["Content-Type"] = content_type
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(BASE + path, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            raw = res.read().decode("utf-8", "replace")
            return res.status, dict(res.headers), raw
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        return exc.code, dict(exc.headers), raw


def as_json(raw):
    try:
        return json.loads(raw)
    except Exception:
        return None


def get_token():
    candidates = [
        ("POST", "/auth/jwt/login", {"username": EMAIL, "password": PASSWORD}, "application/x-www-form-urlencoded"),
        ("POST", "/auth/jwt/login", {"email": EMAIL, "password": PASSWORD}, "application/json"),
        ("POST", "/api/v1/auth/login", {"email": EMAIL, "password": PASSWORD}, "application/json"),
        ("POST", "/api/v1/auth/login", {"username": EMAIL, "password": PASSWORD}, "application/x-www-form-urlencoded"),
        ("POST", "/api/v1/login", {"email": EMAIL, "password": PASSWORD}, "application/json"),
        ("POST", "/api/v1/users/login", {"email": EMAIL, "password": PASSWORD}, "application/json"),
    ]
    for method, path, data, ctype in candidates:
        status, headers, raw = request(method, path, data, content_type=ctype)
        parsed = as_json(raw) or {}
        token = (
            parsed.get("access_token")
            or parsed.get("token")
            or (parsed.get("data") or {}).get("access_token")
        )
        print(f"LOGIN_TRY path={path} status={status} token={bool(token)}")
        if token:
            return token
    raise SystemExit("LOGIN_FAILED")


def main():
    token = get_token()
    status, _, raw = request("GET", "/users/me", token=token)
    print(f"USERS_ME status={status}")
    if status != 200:
        print(raw[:500])
        raise SystemExit("USERS_ME_FAILED")

    status, _, raw = request("GET", "/api/v1/searchspaces", token=token)
    print(f"SEARCHSPACES status={status}")
    spaces = as_json(raw)
    if status != 200 or not spaces:
        print(raw[:1000])
        raise SystemExit("SEARCHSPACES_FAILED")
    if isinstance(spaces, dict):
        spaces = spaces.get("data") or spaces.get("items") or spaces.get("searchspaces") or []
    space_id = spaces[0]["id"]
    print(f"SPACE_ID={space_id}")

    path = f"/api/v1/auth/google/drive/connector/add?space_id={space_id}"
    status, headers, raw = request("GET", path, token=token)
    print(f"DRIVE_INIT status={status}")
    parsed = as_json(raw) or {}
    auth_url = (
        parsed.get("authorization_url")
        or parsed.get("auth_url")
        or parsed.get("url")
        or parsed.get("redirect_url")
        or raw
    )
    auth_url = str(auth_url).replace("\\u0026", "&").replace("&amp;", "&")
    match = re.search(r"https://accounts\.google\.com[^\"'\s]+", auth_url)
    if match:
        auth_url = match.group(0)
    auth_url = auth_url.replace("\\u0026", "&").replace("&amp;", "&")
    parsed_url = urllib.parse.urlparse(auth_url)
    qs = urllib.parse.parse_qs(parsed_url.query)
    print(f"AUTH_QUERY_LEN={len(parsed_url.query)}")
    print(f"AUTH_HOST={parsed_url.netloc}")
    print(f"CLIENT_ID_LEN={len((qs.get('client_id') or [''])[0])}")
    print(f"REDIRECT_URI={(qs.get('redirect_uri') or [''])[0]}")
    print(f"SCOPE_HAS_DRIVE={'drive' in (qs.get('scope') or [''])[0]}")
    if parsed_url.netloc != "accounts.google.com":
        raise SystemExit("AUTH_URL_NOT_GOOGLE")
    if len((qs.get("client_id") or [""])[0]) < 20:
        raise SystemExit("CLIENT_ID_BAD")
    if (qs.get("redirect_uri") or [""])[0] != "http://localhost:3929/api/v1/auth/google/drive/connector/callback":
        raise SystemExit("REDIRECT_URI_BAD")
    print("DRIVE_OAUTH_INIT_OK=True")


if __name__ == "__main__":
    main()
