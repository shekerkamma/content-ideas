import os

for key in [
    "GOOGLE_OAUTH_CLIENT_ID",
    "GOOGLE_OAUTH_CLIENT_SECRET",
    "GOOGLE_DRIVE_REDIRECT_URI",
    "GOOGLE_PICKER_API_KEY",
]:
    value = os.getenv(key) or ""
    print(f"{key}_SET={bool(value)};LEN={len(value)}")
