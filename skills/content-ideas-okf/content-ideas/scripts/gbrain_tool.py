#!/usr/bin/env python3
"""Thin CLI for using gbrain as a content-research pipeline stage."""

from __future__ import annotations

import argparse
from pathlib import Path

from lib import gbrain


def _cmd_recall_note(args):
    response = gbrain.recall(args.query, mode=args.mode)
    out_path = Path(args.out)
    gbrain.write_recall_note(
        out_path,
        title=args.title,
        query_text=args.query,
        response_text=response,
        slug=args.slug,
    )
    print(out_path)


def _cmd_write_back(args):
    body = Path(args.file).read_text(encoding="utf-8")
    gbrain.write_page(args.slug, body)
    print(args.slug)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    recall_note = sub.add_parser("recall-note", help="run a gbrain recall and write a markdown note")
    recall_note.add_argument("--query", required=True, help="semantic recall query")
    recall_note.add_argument("--title", required=True, help="note title")
    recall_note.add_argument("--out", required=True, help="output markdown path")
    recall_note.add_argument("--slug", default="", help="optional recalled page slug")
    recall_note.add_argument("--mode", default="query", choices=["query", "search"])
    recall_note.set_defaults(func=_cmd_recall_note)

    write_back = sub.add_parser("write-back", help="write a markdown artifact back into gbrain")
    write_back.add_argument("--slug", required=True, help="target gbrain page slug")
    write_back.add_argument("--file", required=True, help="markdown file to upload")
    write_back.set_defaults(func=_cmd_write_back)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
