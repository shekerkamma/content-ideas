#!/usr/bin/env python3
"""Native Gemini video analysis using an existing host AI Studio credential."""
import argparse
import base64
import json
import mimetypes
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://generativelanguage.googleapis.com"
DEFAULT_MODEL = "gemini-pro-latest"  # alias; analysis.json records the returned model
PROMPT = "Analyze this video using both visuals and audio. Give a concise overview, timestamped key moments, visible interface actions, and practical recommendations. Separate observations from inference. If audio or visuals are unavailable, say so."


def _config_keys(path):
    """api-key values under the top-level `gemini-api-key:` list; stdlib only, so CI needs no PyYAML."""
    keys, inside = [], False
    for line in path.read_text(encoding='utf-8').splitlines():
        if re.match(r'^\S', line):
            inside = line.split('#', 1)[0].strip() == 'gemini-api-key:'
            continue
        match = inside and re.match(r'^\s*-?\s*api-key:\s*["\']?([^"\'\s#]+)', line)
        if match:
            keys.append(match.group(1))
    return keys


def credential(config=None):
    # Preserve the documented Pro-credit key; unrelated shell keys can differ.
    paths = [Path(config)] if config else [Path('/mnt/c/Users/sheke/.cli-proxy-api/config.yaml'), Path.home()/'.cli-proxy-api/config.yaml']
    for path in paths:
        if path.is_file():
            keys = _config_keys(path)
            if len(keys) > 1:
                raise ValueError('Multiple AI Studio credentials: select a host config with one entry.')
            if keys:
                return keys[0], str(path)
    if config:
        raise ValueError('Selected host configuration contains no Gemini API credential.')
    for name in ('GOOGLE_GENERATIVE_AI_API_KEY', 'GEMINI_API_KEY', 'GOOGLE_API_KEY'):
        if os.environ.get(name):
            return os.environ[name], 'environment:' + name
    raise ValueError('No existing AI Studio credential found in host configuration or environment.')


def request(key, path, payload=None, method=None, headers=None, raw=None):
    url = path if path.startswith('https://') else API + path
    if urllib.parse.urlparse(url).hostname != 'generativelanguage.googleapis.com':
        raise ValueError('Refusing to send the credential to an unexpected upload host.')
    data = raw if raw is not None else (json.dumps(payload).encode() if payload is not None else None)
    hdr = {'x-goog-api-key': key, 'Content-Type': 'application/json'}
    hdr.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=hdr, method=method)
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            body = response.read()
            return (json.loads(body) if body else {}), dict(response.headers)
    except urllib.error.HTTPError as exc:
        # Do not print upstream bodies, request URLs, headers or credentials.
        raise RuntimeError(f'Gemini request failed: HTTP {exc.code}. No fallback provider was used.') from None
    except urllib.error.URLError:
        raise RuntimeError('Gemini network request failed. No fallback provider was used.') from None


def video_part(source, force_upload=False):
    if source.startswith(('https://', 'http://')):
        host = urllib.parse.urlparse(source).hostname
        if host not in ('youtube.com', 'www.youtube.com', 'm.youtube.com', 'youtu.be'):
            raise ValueError('URL input must be a public YouTube video; download other sources to a local video first.')
        return {'fileData': {'fileUri': source}}, None
    path = Path(source).expanduser().resolve()
    if not path.is_file():
        raise ValueError('Input video file does not exist.')
    mime = mimetypes.guess_type(path.name)[0]
    if not mime or not mime.startswith('video/'):
        raise ValueError('Input must be a supported video file.')
    if not force_upload and path.stat().st_size <= 12 * 1024 * 1024:
        return {'inlineData': {'mimeType': mime, 'data': base64.b64encode(path.read_bytes()).decode()}}, None
    return None, (path, mime)


def upload(key, path, mime):
    data, headers = request(key, '/upload/v1beta/files', {'file': {'display_name': 'video-analysis'}}, headers={
        'X-Goog-Upload-Protocol': 'resumable', 'X-Goog-Upload-Command': 'start',
        'X-Goog-Upload-Header-Content-Length': str(path.stat().st_size), 'X-Goog-Upload-Header-Content-Type': mime})
    upload_url = next((v for k,v in headers.items() if k.lower() == 'x-goog-upload-url'), None)
    if not upload_url:
        raise RuntimeError('Gemini did not return a resumable upload URL.')
    data, _ = request(key, upload_url, raw=path.read_bytes(), headers={
        'Content-Type': mime, 'X-Goog-Upload-Offset': '0', 'X-Goog-Upload-Command': 'upload, finalize'})
    file = data['file']
    return file


def analyze(source, out_dir, prompt=PROMPT, model=DEFAULT_MODEL, start=None, end=None, config=None, force_upload=False):
    if not re.fullmatch(r'gemini-[a-zA-Z0-9.-]+', model):
        raise ValueError('Invalid Gemini model identifier.')
    if start is not None and start < 0 or end is not None and end <= (start or 0):
        raise ValueError('Video offsets must be nonnegative and end must exceed start.')
    key, origin = credential(config)
    part, pending = video_part(source, force_upload)
    uploaded = None
    cleanup = 'not-needed'
    try:
        if pending:
            uploaded = upload(key, *pending)
            deadline = time.monotonic() + 300
            while uploaded.get('state') == 'PROCESSING':
                if time.monotonic() > deadline:
                    raise RuntimeError('Gemini video processing timed out.')
                time.sleep(3)
                uploaded, _ = request(key, '/v1beta/' + uploaded['name'])
            if uploaded.get('state') != 'ACTIVE':
                raise RuntimeError('Gemini failed to process the uploaded video.')
            part = {'fileData': {'fileUri': uploaded['uri'], 'mimeType': uploaded['mimeType']}}
        metadata = {}
        if start is not None:
            metadata['startOffset'] = f'{start}s'
        if end is not None:
            metadata['endOffset'] = f'{end}s'
        if metadata:
            part['videoMetadata'] = metadata
        response, _ = request(key, f'/v1beta/models/{model}:generateContent', {
            'contents': [{'role': 'user', 'parts': [part, {'text': prompt}]}],
            'generationConfig': {'maxOutputTokens': 4096}})
        text = '\n'.join(p.get('text', '') for c in response.get('candidates', []) for p in c.get('content', {}).get('parts', []) if not p.get('thought'))
        if not text.strip():
            raise RuntimeError('Gemini returned no analysis text.')
    finally:
        if uploaded:
            try:
                request(key, '/v1beta/' + uploaded['name'], method='DELETE')
                cleanup = 'deleted'
            except RuntimeError:
                cleanup = 'delete-failed'
                print('Warning: temporary Gemini upload deletion failed; service retention applies.', file=sys.stderr)
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    report = {'provider': 'Google Gemini API', 'endpoint': API, 'requestedModel': model,
        'returnedModel': response.get('modelVersion'), 'credentialSource': origin,
        'inputMode': 'uploaded-video' if pending else ('youtube-video' if 'fileData' in part else 'inline-video'),
        'source': source, 'startSeconds': start, 'endSeconds': end,
        'usage': response.get('usageMetadata'), 'temporaryUploadCleanup': cleanup, 'analysis': text}
    (out/'analysis.json').write_text(json.dumps(report, indent=2)+'\n')
    (out/'analysis.md').write_text(f'# Gemini video analysis\n\nModel: {report["returnedModel"] or model}\n\n{text}\n')
    return {k:v for k,v in report.items() if k != 'analysis'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', nargs='?')
    parser.add_argument('--out-dir')
    parser.add_argument('--prompt', default=PROMPT)
    parser.add_argument('--model', default=DEFAULT_MODEL)
    parser.add_argument('--start', type=float)
    parser.add_argument('--end', type=float)
    parser.add_argument('--host-config')
    parser.add_argument('--doctor', action='store_true')
    parser.add_argument('--upload', action='store_true', help='Use Files API even for a small local video')
    args = parser.parse_args()
    try:
        if args.doctor:
            key, origin = credential(args.host_config)
            models, _ = request(key, '/v1beta/models')
            present = any(m['name'] == 'models/' + args.model for m in models.get('models', []))
            print(json.dumps({'credentialSource': origin, 'credentialConfigured': True, 'model': args.model, 'modelListed': present}))
            return 0 if present else 1
        if not args.source or not args.out_dir:
            parser.error('source and --out-dir are required for analysis')
        print(json.dumps(analyze(args.source, args.out_dir, args.prompt, args.model, args.start, args.end, args.host_config, args.upload)))
        return 0
    except (ValueError, RuntimeError, OSError, ImportError):
        # OSError/parse errors may include sensitive source text. Keep failures safe.
        print('Video analysis failed. Check the input, host credential configuration, model access and network; no credential or upstream response was printed.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
