#!/usr/bin/env python3
"""Make CLIProxyAPI reachable at 127.0.0.1:8317 inside WSL.

CLIProxyAPI runs on Windows. Under WSL's NAT networking, Windows' 127.0.0.1 is not
WSL's, and the Windows default-gateway IP changes on every reboot. Configs copied
from Windows (Hermes: `base_url: http://127.0.0.1:8317/v1`) therefore fail from WSL
with a bare "Connection error".

This forwards WSL 127.0.0.1:<port> to <gateway>:<port>, re-resolving the gateway on
every connection so a reboot needs no restart. It binds loopback only, so nothing
outside this machine can reach it. Stdlib only. Run as the systemd user service
`cliproxy-forward.service` (see scripts/install-cliproxy-forward.sh).
"""
from __future__ import annotations

import asyncio
import os
import subprocess

PORT = int(os.environ.get("CLIPROXY_PORT", "8317"))
LISTEN = os.environ.get("CLIPROXY_FORWARD_LISTEN", "127.0.0.1")


def gateway() -> str:
    override = os.environ.get("CLIPROXY_HOST")
    if override:
        return override
    out = subprocess.run(["ip", "route"], capture_output=True, text=True, check=True).stdout
    for line in out.splitlines():
        if line.startswith("default"):
            return line.split()[2]
    raise RuntimeError("no default route")


async def pipe(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    try:
        while data := await reader.read(65536):
            writer.write(data)
            await writer.drain()
    except (ConnectionError, asyncio.CancelledError):
        pass
    finally:
        try:
            writer.close()
        except Exception:
            pass


async def handle(client_r: asyncio.StreamReader, client_w: asyncio.StreamWriter) -> None:
    try:
        up_r, up_w = await asyncio.wait_for(asyncio.open_connection(gateway(), PORT), timeout=10)
    except Exception as exc:  # upstream down: close, so the client sees a clean failure
        print(f"cliproxy-forward: upstream {PORT} unreachable: {exc}", flush=True)
        client_w.close()
        return
    await asyncio.gather(pipe(client_r, up_w), pipe(up_r, client_w))


async def main() -> None:
    server = await asyncio.start_server(handle, LISTEN, PORT)
    print(f"cliproxy-forward: {LISTEN}:{PORT} -> <gateway>:{PORT} (now {gateway()})", flush=True)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
