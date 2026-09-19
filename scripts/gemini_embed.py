#!/usr/bin/env python3
"""
gemini_embed.py — Cross-host multimodal embedding CLI for Claude Code, Codex, and DeepSeek Harness.
Uses models/gemini-embedding-2 via Google AI Studio API (3,072 dimensions).
Zero runtime pip dependencies (stdlib only).
"""
import os
import sys
import json
import math
import argparse
import base64
import urllib.request
import urllib.error

def get_api_key():
    key = os.environ.get("GOOGLE_GENERATIVE_AI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if key:
        return key

    # Check .claude/settings.local.json
    candidates = [
        os.path.expanduser("~/content-ideas/.claude/settings.local.json"),
        os.path.join(os.getcwd(), ".claude/settings.local.json"),
        os.path.expanduser("~/.config/content/.env")
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                if c.endswith(".json"):
                    with open(c) as f:
                        data = json.load(f)
                        k = data.get("env", {}).get("GOOGLE_GENERATIVE_AI_API_KEY")
                        if k:
                            return k
                elif c.endswith(".env"):
                    with open(c) as f:
                        for line in f:
                            if "GOOGLE_GENERATIVE_AI_API_KEY" in line or "GEMINI_API_KEY" in line:
                                return line.strip().split("=", 1)[1].strip("\"'")
            except Exception:
                pass
    return None

def get_mime_type(filepath):
    ext = filepath.split(".")[-1].lower()
    if ext == "png":
        return "image/png"
    elif ext in ("jpg", "jpeg"):
        return "image/jpeg"
    elif ext == "webp":
        return "image/webp"
    elif ext == "gif":
        return "image/gif"
    elif ext == "svg":
        return "image/svg+xml"
    return "application/octet-stream"

def embed(text=None, image_path=None, model="models/gemini-embedding-2", api_key=None):
    if not api_key:
        api_key = get_api_key()
    if not api_key:
        raise ValueError("GOOGLE_GENERATIVE_AI_API_KEY not found in environment or configuration files.")

    parts = []
    if text:
        parts.append({"text": text})
    if image_path:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        with open(image_path, "rb") as f:
            b64_data = base64.b64encode(f.read()).decode("utf-8")
        mime_type = get_mime_type(image_path)
        parts.append({
            "inlineData": {
                "mimeType": mime_type,
                "data": b64_data
            }
        })

    if not parts:
        raise ValueError("At least one of --text or --image must be specified.")

    url = f"https://generativelanguage.googleapis.com/v1beta/{model}:embedContent?key={api_key}"
    payload = {
        "model": model,
        "content": {
            "parts": parts
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["embedding"]["values"]
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        raise RuntimeError(f"Google API Error (HTTP {e.code}): {err_msg}")

def cosine_similarity(v1, v2):
    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a, b in zip(v1, v1)))
    mag2 = math.sqrt(sum(b * b for b, b in zip(v2, v2)))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)

def main():
    parser = argparse.ArgumentParser(
        description="Multimodal embedding CLI using Google Gemini Embedding 2 (3072 dims)."
    )
    parser.add_argument("--text", "-t", help="Text to embed")
    parser.add_argument("--image", "-i", help="Image file path to embed (PNG, JPEG, WebP, GIF)")
    parser.add_argument("--out", "-o", help="Output JSON file for the embedding vector")
    parser.add_argument("--compare-text", help="Secondary text to compute cosine similarity against")
    parser.add_argument("--compare-image", help="Secondary image to compute cosine similarity against")
    parser.add_argument("--model", default="models/gemini-embedding-2", help="Model name (default: models/gemini-embedding-2)")

    args = parser.parse_args()

    if not args.text and not args.image:
        parser.print_help()
        sys.exit(1)

    try:
        vec1 = embed(text=args.text, image_path=args.image, model=args.model)
        
        if args.out:
            with open(args.out, "w") as f:
                json.dump(vec1, f)
            print(f"✓ Saved {len(vec1)}-dimensional vector to {args.out}")
        else:
            print(f"✓ Generated {len(vec1)}-dimensional vector: [{vec1[0]:.6f}, {vec1[1]:.6f}, {vec1[2]:.6f}, ...]")

        # Comparison mode
        if args.compare_text or args.compare_image:
            vec2 = embed(text=args.compare_text, image_path=args.compare_image, model=args.model)
            sim = cosine_similarity(vec1, vec2)
            print(f"✓ Cosine Similarity: {sim:.4f}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
