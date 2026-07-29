#!/usr/bin/env python3
"""Download official company-site visual assets discovered with You.com livecrawl."""

from __future__ import annotations

import hashlib
import json
import mimetypes
import subprocess
import urllib.request
from html import unescape
from pathlib import Path


RUN = Path(__file__).resolve().parent
ASSETS = RUN / "assets" / "company-sites"
MANIFEST = RUN / "research" / "visual-assets.json"

RECORDS = [
    {
        "company": "Axelera AI",
        "source_page": "https://axelera.ai/news/axelera-ai-secures-more-than-250-million-funding-on-global-ai-demand",
        "asset_url": "https://axelera.ai/hubfs/Axelera%20AI%20Fabrizio%20nad%20Evangelos%20CEO%20and%20CTO.webp",
        "filename": "axelera-ai.webp",
        "discovered_in": "axelera-official.json",
        "description": "Axelera AI leadership and branded company visual",
    },
    {
        "company": "Tenstorrent",
        "source_page": "https://tenstorrent.com/vision/tenstorrent-announces-availability-of-tt-ascalon",
        "asset_url": "https://cdn.sanity.io/images/jpb4ed5r/production/284af53a270cc95d8860818e282c54cf1e56321a-942x628.png",
        "filename": "tenstorrent-tt-ascalon.png",
        "discovered_in": "tenstorrent-official.json",
        "description": "Official Tenstorrent TT-Ascalon launch visual",
    },
    {
        "company": "NextSilicon",
        "source_page": "https://www.nextsilicon.com/press-releases/maverick-2-powers-hpc-ai-breakthroughs",
        "asset_url": "https://www.nextsilicon.com/assets/images/insights/nextsilicon-breakthrough/preview.jpg",
        "filename": "nextsilicon-maverick-2.jpg",
        "discovered_in": "nextsilicon-official.json",
        "description": "Official Maverick-2 launch visual",
    },
    {
        "company": "Fractile",
        "source_page": "https://www.fractile.ai/",
        "asset_url": "https://images.prismic.io/fractile-landing-page/aEg02bh8WN-LV75U_Thumbnail.jpg",
        "filename": "fractile-thumbnail.jpg",
        "discovered_in": "fractile-official.json",
        "description": "Official Fractile company visual",
    },
    {
        "company": "Etched",
        "source_page": "https://www.etched.com/",
        "asset_url": "https://cdn.sanity.io/images/rwbees58/production/9885cd08fc6fe49fff1d2b35a8f97447753ca9b0-1200x630.png?w=1200&h=630&fm=png&fit=max&auto=format",
        "filename": "etched-sohu.png",
        "discovered_in": "etched-visuals-livecrawl.json",
        "description": "Official Etched / Sohu website visual",
    },
    {
        "company": "d-Matrix",
        "source_page": "https://www.d-matrix.ai/d-matrix-corsair-ai-inference-platform-enters-full-production/",
        "asset_url": "https://www.d-matrix.ai/wp-content/uploads/2026/06/d-Matrix-founders-with-Corsair.jpg",
        "filename": "d-matrix-corsair.jpg",
        "discovered_in": "d-matrix-official.json",
        "description": "d-Matrix founders with Corsair hardware",
    },
    {
        "company": "Cornelis Networks",
        "source_page": "https://www.cornelisnetworks.com/stories/cornelis-cn5000-launches-rewiring-ai-and-hpc-networking-at-scale",
        "asset_url": "https://cdn.prod.website-files.com/66620f51fea4bdc8706c4491/683f2d65779d9728586c5cc7_Cornelisimage.png",
        "filename": "cornelis-cn5000.png",
        "discovered_in": "cornelis-visuals-livecrawl.json",
        "description": "Official Cornelis CN5000 launch visual",
    },
    {
        "company": "Lightmatter",
        "source_page": "https://lightmatter.co/blog/seeing-is-believing-a-technical-deep-dive-into-lightmatters-hardware/",
        "asset_url": "https://lightmatter.co/wp-content/uploads/2025/09/Copy-of-Temperature-ramp-plots.png",
        "filename": "lightmatter-hardware-proof.png",
        "discovered_in": "lightmatter-visuals-livecrawl.json",
        "description": "Official Lightmatter hardware validation visual",
    },
    {
        "company": "MatX",
        "source_page": "https://matx.com/",
        "asset_url": "https://matx.com/images/cover.png",
        "filename": "matx-cover.png",
        "discovered_in": "matx-official.json",
        "description": "Official MatX homepage product visual",
    },
    {
        "company": "Xsight Labs",
        "source_page": "https://xsightlabs.com/switches/x2",
        "asset_url": "https://you.com/favicon?domain=xsightlabs.com&size=256",
        "filename": "xsight-site-icon.png",
        "discovered_in": "xsight-visuals-livecrawl.json",
        "description": "Xsight Labs site icon returned with the official X2 livecrawl result",
    },
]


def download(url: str, destination: Path) -> tuple[str, str]:
    request = urllib.request.Request(
        unescape(url),
        headers={"User-Agent": "Mozilla/5.0 (compatible; strategy-deck-asset-ingestion/1.0)"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = response.read()
        content_type = response.headers.get_content_type()
    destination.write_bytes(payload)
    return content_type, hashlib.sha256(payload).hexdigest()


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    manifest = []
    for record in RECORDS:
        destination = ASSETS / record["filename"]
        content_type, digest = download(record["asset_url"], destination)
        final_path = destination
        if destination.suffix.lower() == ".pdf":
            rendered = ASSETS / record["rendered_filename"]
            subprocess.run(
                [
                    "pdftoppm",
                    "-f",
                    "1",
                    "-singlefile",
                    "-png",
                    "-r",
                    "160",
                    str(destination),
                    str(rendered.with_suffix("")),
                ],
                check=True,
            )
            final_path = rendered
        guessed = mimetypes.guess_type(final_path.name)[0] or content_type
        manifest.append(
            {
                **record,
                "local_path": str(final_path.relative_to(RUN)),
                "download_path": str(destination.relative_to(RUN)),
                "content_type": guessed,
                "sha256": digest,
                "retrieval": "You.com Level 2 livecrawl discovery followed by direct official-site download",
            }
        )
        print(f"{record['company']}: {final_path.name}")
    MANIFEST.write_text(json.dumps({"assets": manifest}, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {MANIFEST}")


if __name__ == "__main__":
    main()
