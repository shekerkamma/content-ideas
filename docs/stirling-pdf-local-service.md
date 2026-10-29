# Stirling PDF as a local service

A self-hosted PDF operations service on `http://localhost:8090`, backing any
skill that needs to merge, split, OCR, redact, compress, or convert a PDF
without shipping the document to a third-party web tool. 259 REST endpoints,
60 tools in the UI, all of it on the machine.

Installed 2026-08-28 at `~/apps/stirling-pdf/` (outside the repo — it is a
machine-local service, not a repo artifact). Image pinned to
`stirlingtools/stirling-pdf:2.14.3-fat`, 2.27 GB.

```bash
~/apps/stirling-pdf/stirling {up|down|restart|logs|status|update|open}
python3 ~/apps/stirling-pdf/smoke_test.py     # 19-case functional suite
```

## Licensing: open-core, and the split is not where you would guess

Stirling-PDF's own README says "open-core". The root `LICENSE` is MIT **with
carve-outs**, and the carve-out directories exist on `main`:
`app/proprietary/`, `app/saas/`, and under `frontend/editor/src/` —
`proprietary`, `desktop`, `saas`, `cloud`, `portal`, `portal-saas`.

- **All 60 PDF tools are the MIT half.** None carries `requiresPremium` in
  `useTranslatedToolRegistry.tsx`.
- **The proprietary half is enterprise plumbing** — 980 Java files under
  `app/proprietary/`: `policy` (163), `security` (129), `storage` (55),
  `workflow` (37, multi-party signing), `mcp` (35 — their MCP server is
  proprietary), `accountlink`, `audit`, `billing`, `cluster`. Plus 365
  frontend files that are almost entirely auth, teams, and billing UI. The
  only PDF-specific proprietary code is `pdf/ua/`, 21 files of PDF/UA
  accessibility tagging.

`app/proprietary/LICENSE` is a "Stirling PDF User License": no production use,
no client-facing or commercial use, no distribution without a paid
subscription. Single-user local operation never reaches it. **Reselling or
hosting for an organization does** — so a claim that the MIT license permits
resale is wrong for those directories.

## Configuration, and why each deviation from upstream exists

`~/apps/stirling-pdf/docker-compose.yml` is adapted from upstream's
`docker/compose/docker-compose.fat.yml`, with four deliberate changes:

- **`127.0.0.1:8090:8080`**, not `0.0.0.0:8080`. Upstream binds every
  interface; this binds loopback only, so the service is not reachable from
  the LAN. Host port 8090 because **8080-8082 are held by the `qm-local-lab`
  stack** on this machine.
- **`SECURITY_ENABLELOGIN: "false"`** — the single-user path. Enabling login
  pulls in accounts and a database, which is the whole cost the self-host was
  meant to avoid.
- **Upstream's demo-site environment stripped** — `METRICS_ENABLED`,
  `SYSTEM_GOOGLEVISIBILITY`, `SHOW_SURVEY` all off.
- **Version tag pinned**, not `:latest`.

## Four host facts that cost a debug cycle each

- **Docker Desktop WSL integration lives in `settings-store.json`, PascalCase.**
  `%APPDATA%\Docker\settings-store.json`, keys `IntegratedWslDistros: ["<distro>"]`
  and `EnableIntegrationWithDefaultWslDistro`. The legacy `settings.json`
  alongside it uses camelCase and has been dead since 2025-02 — editing it does
  nothing. Restart Docker Desktop to apply. `IntegratedWslDistros` may be absent
  entirely rather than present-and-empty.
- **`MemoryMiB` in that file is inert on the WSL2 backend.** It reads 2048 here
  while `docker info` reports 16.6 GB, because WSL manages memory globally via
  `.wslconfig`. Do not restart Docker to "fix" a memory limit that is not
  applied.
- **Being in `/etc/group`'s `docker` line is not being in the group.** A login
  session that predates the group edit gets `permission denied` on
  `/var/run/docker.sock` while `getent group docker` lists the user. Bridge with
  `sg docker -c '<cmd>'` until the next fresh login; do not add a second group
  entry or chmod the socket.
- **First boot takes minutes and looks hung.** The fat image runs `chown -R`
  over its font tree, then starts Xvfb and unoserver, then Spring. 0.2% CPU at
  50 MB during the chown is normal. Health is `starting`, not `unhealthy`.

## API: the multipart part's Content-Type is load-bearing

**`/api/v1/convert/pdf/word` rejects `Content-Type: application/octet-stream`
on the file part with a bare HTTP 400, a zero-byte body, and nothing in the
server log.** It requires `application/pdf`. Every other endpoint tested
accepts `octet-stream`.

`curl -F` sets `application/pdf` from the `.pdf` extension, so the same request
succeeds from a shell and fails from a hand-rolled client — which reads as a
flaky endpoint and is not. Set the part's content type explicitly on every
request.

Two more API notes:

- **The OpenAPI spec is at `/v1/api-docs`**, not `/v3/api-docs`. The SPA serves
  `index.html` for unknown front-end paths, so a wrong path returns **200 HTML**
  rather than a 404. Check `content_type`, never the status code alone.
- **Endpoint enums are not validated loudly.** `ocr-pdf` accepts
  `ocrType` of `skip-text` / `force-ocr` / `Normal`; passing `Force` returns
  200 and silently does something else. See below.

## Verification discipline: an OCR test that certified nothing

The first OCR check here passed and was worthless, in two compounding ways:

1. It passed `ocrType=Force`, which is not in the endpoint's enum. The request
   returned 200 and fell through to another mode.
2. It ran against a PDF that **already had a text layer**, so `pdftotext`
   recovered text that was there before OCR ever ran.

A 200 plus a valid PDF plus extractable text — and no evidence Tesseract
executed. The rewritten test builds the negative control first:

```
render page -> PNG -> rebuild as image-only PDF
  -> assert zero extractable characters   <- the control
  -> OCR with force-ocr
  -> assert text returns and matches known words
```

Measured: 0 characters before, 334 after, 28 of 40 known long words matched.

`~/apps/stirling-pdf/smoke_test.py` holds the full 19-case suite. Every case
asserts on content — page counts, extracted text, encryption flags, file magic
— never on the status code.

**Four of its first-run failures were the test being wrong, not the tool.**
Worth reading before trusting a red result here:

| Reported failure | Actually |
|---|---|
| `rotate-pdf` | Worked. `pdfinfo` pads its columns; `"Page rot: 90"` does not substring-match `"Page rot:        90"`. |
| `add-password` | Worked — AES-256, `print:no` honored. `pdfinfo` without the password prints `Command Line Error: Incorrect password` and no `Encrypted:` line at all, so parsing for one finds nothing. |
| `add-watermark` | Worked. The watermark is drawn with a subsetted font carrying no `ToUnicode` map, so text extraction cannot see it. Confirmed by rendering the page and looking. |
| `convert pdf->docx` | Worked from `curl`. The client was sending `octet-stream` — see the Content-Type finding above. |

A red result from a check whose assertion was never itself tested is a
hypothesis, not a defect.

## Not covered

The suite drives the API, not the browser, so the UI is unexercised. Also
untested: the Automate pipeline builder, certificate signing, form editing, and
folder scanning.
